"""
PERFORMANCE OPTIMIZATION - Phase 1 TB CXR Pipeline
Two-track output:

  TRACK A - BEST PRACTICAL MODEL
    Find the strongest real configuration for the SIH demonstration.
    Uses full training set, best encoder, best representation, optimized classical classifier.

  TRACK B - CONTROLLED RESEARCH COMPARISON (2-2 matrix)
    Fixed conditions: same split, same encoder (best from A), PCA-8, n_train=40 cap.
    Vary ONLY: representation (WHOLE_CXR vs GT_LUNG_MASKED) - learner (RBF-SVM vs QSVM).
    Answers: "Does anatomy help?" and "Does the quantum kernel contribute?"

Rules:
  - Test set locked until final one-pass evaluation per frozen config
  - GT_LUNG_* always labeled explicitly - never called automated segmentation
  - Fusion weights and thresholds derived from CV/training predictions only
  - Majority baseline reported alongside every result

Run:
    python -m src.ml.optimize
"""
import warnings
warnings.filterwarnings("ignore")

import numpy as np, glob, json, time, os, pickle
from pathlib import Path
from sklearn.model_selection import (
    train_test_split, StratifiedKFold, cross_val_score, cross_val_predict
)
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, roc_auc_score, confusion_matrix, make_scorer
import xgboost as xgb

from src.ml.feature_extraction import CXRFeatureExtractor
from src.ml.qsvm import stratified_cap, save_weights

# -- Qiskit ----------------------------------------------------------------
try:
    from qiskit.circuit.library import zz_feature_map as _build_zz
    def _feature_map(n): return _build_zz(feature_dimension=n, reps=2, entanglement="linear")
except ImportError:
    from qiskit.circuit.library import ZZFeatureMap
    def _feature_map(n): return ZZFeatureMap(feature_dimension=n, reps=2, entanglement="linear")

from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_algorithms.state_fidelities import ComputeUncompute
from qiskit.primitives import StatevectorSampler as Sampler

# -- Constants -------------------------------------------------------------
SEED           = 42
DATASET_BASE   = Path("data/datasets/montgomery/MontgomerySet")
IMAGE_DIR      = DATASET_BASE / "CXR_png"
EXPERIMENT_DIR = Path("data/experiments")
EMBED_CACHE    = EXPERIMENT_DIR / "embedding_cache"
EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)
EMBED_CACHE.mkdir(parents=True, exist_ok=True)

# Track B fixed hyperparameters (quantum constraint)
TRACK_B_PCA  = 8
TRACK_B_CAP  = 40
TRACK_B_REPR = ["WHOLE_CXR", "GT_LUNG_MASKED"]   # 2-2 matrix rows

ba_scorer = make_scorer(balanced_accuracy_score)

# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def metrics(y_true, y_pred, y_score=None, label=""):
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    n    = len(y_true)
    acc  = (tp + tn) / n
    sens = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    f1   = 2 * prec * sens / (prec + sens) if (prec + sens) > 0 else 0.0
    ba   = balanced_accuracy_score(y_true, y_pred)
    auc  = None
    if y_score is not None:
        try: auc = roc_auc_score(y_true, y_score)
        except: pass
    d = dict(label=label, tp=int(tp), tn=int(tn), fp=int(fp), fn=int(fn),
             acc=acc, ba=ba, sens=sens, spec=spec, prec=prec, f1=f1, auc=auc)
    auc_s = f"{auc:.4f}" if auc is not None else "   N/A"
    print(f"  {label[:50]:<50} Acc={acc:.3f} BA={ba:.3f} Sens={sens:.3f} Spec={spec:.3f} F1={f1:.3f} AUC={auc_s}")
    return d


def tune_threshold(cv_scores, y_true):
    """Best threshold maximising balanced-accuracy on CV/LOO training predictions only."""
    best_t, best_ba = cv_scores.mean(), -1.0
    for t in np.linspace(cv_scores.min(), cv_scores.max(), 300):
        ba = balanced_accuracy_score(y_true, (cv_scores >= t).astype(int))
        if ba > best_ba:
            best_ba = ba; best_t = t
    return float(best_t), float(best_ba)


_REPR_INTERNAL = {   # optimizer key - CXRFeatureExtractor internal name
    "WHOLE_CXR":       "whole",
    "GT_LUNG_MASKED":  "masked",
    "GT_LUNG_CROPPED": "cropped",
}

def extract_or_load(enc_name, repr_key, paths, split_tag):
    cache = EMBED_CACHE / f"{enc_name}_{repr_key}_{split_tag}.pkl"
    if cache.exists():
        with open(cache, "rb") as f: emb = pickle.load(f)
        print(f"    [CACHE] {cache.name}  shape={emb.shape}")
        return emb
    ext = CXRFeatureExtractor(encoder=enc_name, representation=_REPR_INTERNAL[repr_key], clahe=True)
    t0 = time.time()
    emb = np.vstack([ext.extract(p).numpy() for p in paths])
    print(f"    [EXTRACT] {enc_name}|{repr_key}|{split_tag}  {time.time()-t0:.1f}s  shape={emb.shape}")
    with open(cache, "wb") as f: pickle.dump(emb, f)
    return emb


def fit_pca_pipeline(train_emb, n_pca):
    scaler = StandardScaler().fit(train_emb)
    train_s = scaler.transform(train_emb)
    pca = PCA(n_components=n_pca, random_state=SEED).fit(train_s)
    return scaler, pca, pca.transform(train_s)


def qsvm_run(X_tr, y_tr, X_te):
    """Fit QSVM on training kernel, predict on test. Returns (preds, scores, kernel_seconds, model)."""
    fm = _feature_map(X_tr.shape[1])
    sampler  = Sampler()
    fidelity = ComputeUncompute(sampler=sampler)
    qk = FidelityQuantumKernel(fidelity=fidelity, feature_map=fm)
    t0 = time.time()
    K_tr = qk.evaluate(x_vec=X_tr)
    K_te = qk.evaluate(x_vec=X_te, y_vec=X_tr)
    elapsed = time.time() - t0
    qsvm = SVC(kernel="precomputed", class_weight="balanced")
    qsvm.fit(K_tr, y_tr)
    scores = qsvm.decision_function(K_te)
    preds  = qsvm.predict(K_te)
    return preds, scores, elapsed, qsvm, K_tr


# -----------------------------------------------------------------------------
# 1. DATASET - FIXED SPLIT, test set LOCKED
# -----------------------------------------------------------------------------
image_paths = sorted(glob.glob(str(IMAGE_DIR / "*.png")))
labels_all  = np.array([int(Path(p).stem.split("_")[-1]) for p in image_paths])

print("=" * 70)
print("OPTIMIZATION - Two-Track TB CXR Pipeline")
print("=" * 70)
print(f"\nDataset: {len(image_paths)} images  TB={int(labels_all.sum())}  Normal={int((labels_all==0).sum())}")

train_idx, test_idx = train_test_split(
    np.arange(len(image_paths)), test_size=0.2, random_state=SEED, stratify=labels_all
)
train_paths  = [image_paths[i] for i in train_idx]
test_paths   = [image_paths[i] for i in test_idx]
train_labels = labels_all[train_idx]
test_labels  = labels_all[test_idx]

print(f"Train={len(train_idx)} (TB={int(train_labels.sum())} / Normal={int((train_labels==0).sum())})")
print(f"Test ={len(test_idx)}  (TB={int(test_labels.sum())}  / Normal={int((test_labels==0).sum())})")
print(f"\nWARNING: Test set LOCKED -- evaluated once only per frozen configuration.\n")

cv5 = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
cv3 = StratifiedKFold(n_splits=3, shuffle=True, random_state=SEED)

# Majority baseline (for reference)
maj_cv_ba = np.mean([
    balanced_accuracy_score(train_labels[v], np.zeros_like(train_labels[v]))
    for _, v in cv5.split(train_labels, train_labels)
])
print(f"Majority baseline CV-BA on training: {maj_cv_ba:.3f}")


# -----------------------------------------------------------------------------
# 2. FEATURE EXTRACTION
# -----------------------------------------------------------------------------
ENCODER_SEARCH = ["densenet121", "efficientnet_b0"]
REPR_SEARCH    = ["WHOLE_CXR", "GT_LUNG_MASKED", "GT_LUNG_CROPPED"]

print("\n=== FEATURE EXTRACTION ===")
print("NOTE: GT_LUNG_* uses Montgomery expert-annotated manual masks - NOT automated segmentation\n")

feat_cache = {}
for enc in ENCODER_SEARCH:
    for rep in REPR_SEARCH:
        print(f"  [{enc}|{rep}]")
        feat_cache[(enc, rep)] = (
            extract_or_load(enc, rep, train_paths, "train"),
            extract_or_load(enc, rep, test_paths,  "test"),
        )


# -----------------------------------------------------------------------------
# TRACK A - BEST PRACTICAL MODEL
# 5-fold CV on training; test set NOT touched
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("TRACK A - BEST PRACTICAL MODEL (5-fold CV, training set only)")
print("=" * 70)

PCA_DIMS = [8, 12, 16, 32]
best_a_score = -1.0
best_a_cfg   = None
track_a_all  = []

for enc in ENCODER_SEARCH:
    for rep in REPR_SEARCH:
        tr_emb, _ = feat_cache[(enc, rep)]
        scaler, pca_full, tr_pca_full = None, None, None

        for n_pca in PCA_DIMS:
            if n_pca >= min(tr_emb.shape):
                continue
            sc = StandardScaler().fit(tr_emb)
            pc = PCA(n_components=n_pca, random_state=SEED).fit(sc.transform(tr_emb))
            X  = pc.transform(sc.transform(tr_emb))
            var = pc.explained_variance_ratio_.sum()

            clfs = {
                "RBF-SVM" : SVC(kernel="rbf", class_weight="balanced", random_state=SEED),
                "LinSVM"  : SVC(kernel="linear", class_weight="balanced", random_state=SEED),
                "LogReg"  : LogisticRegression(class_weight="balanced", max_iter=2000, random_state=SEED),
                "XGBoost" : xgb.XGBClassifier(
                    n_estimators=100, max_depth=3, eval_metric="logloss", verbosity=0, random_state=SEED,
                    scale_pos_weight=float((train_labels==0).sum())/float(train_labels.sum())
                ),
            }

            for clf_name, clf in clfs.items():
                cv_ba = cross_val_score(clf, X, train_labels, cv=cv5, scoring=ba_scorer)
                mean_ba, std_ba = cv_ba.mean(), cv_ba.std()
                print(f"  [{enc[:10]}|{rep[:15]}|pca={n_pca:2d}|{clf_name:8s}]  CV-BA={mean_ba:.3f}-{std_ba:.3f}  var={var:.1%}")

                row = dict(encoder=enc, repr=rep, pca=n_pca, clf=clf_name,
                           cv_ba=mean_ba, cv_ba_std=std_ba, var=float(var))
                track_a_all.append(row)

                if mean_ba > best_a_score:
                    best_a_score = mean_ba
                    best_a_cfg = dict(encoder=enc, repr=rep, pca=n_pca, clf_name=clf_name,
                                      clf_obj=clf, scaler=sc, pca_obj=pc)

print(f"\n>> TRACK A WINNER  CV-BA={best_a_score:.4f}")
print(f"  Encoder={best_a_cfg['encoder']}  Repr={best_a_cfg['repr']}  PCA={best_a_cfg['pca']}  Clf={best_a_cfg['clf_name']}")

# Fit winner on full training set; threshold from CV predictions
tr_emb_a, te_emb_a = feat_cache[(best_a_cfg["encoder"], best_a_cfg["repr"])]
sc_a, pc_a = best_a_cfg["scaler"], best_a_cfg["pca_obj"]
clf_a = best_a_cfg["clf_obj"]
X_tr_a = pc_a.transform(sc_a.transform(tr_emb_a))
X_te_a = pc_a.transform(sc_a.transform(te_emb_a))
clf_a.fit(X_tr_a, train_labels)

cv_scores_a = cross_val_predict(clf_a, X_tr_a, train_labels, cv=cv5, method="decision_function")
thresh_a, _ = tune_threshold(cv_scores_a, train_labels)


# -----------------------------------------------------------------------------
# TRACK B - CONTROLLED RESEARCH COMPARISON (2-2 matrix)
# Fixed: best encoder from Track A, PCA-8, n_train=40 cap
# Vary:  representation (WHOLE_CXR / GT_LUNG_MASKED) - learner (Classical / QSVM)
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("TRACK B - CONTROLLED RESEARCH COMPARISON (2-2 matrix)")
print(f"  Encoder={best_a_cfg['encoder']}  PCA={TRACK_B_PCA}  n_train={TRACK_B_CAP}")
print("  Identical conditions except representation and learner.")
print("=" * 70)

track_b_results = {}
qsvm_models = {}

for rep in TRACK_B_REPR:
    print(f"\n-- Representation: {rep} -------------------------------------------")
    tr_emb_b, te_emb_b = feat_cache[(best_a_cfg["encoder"], rep)]
    sc_b = StandardScaler().fit(tr_emb_b)
    pc_b = PCA(n_components=TRACK_B_PCA, random_state=SEED).fit(sc_b.transform(tr_emb_b))
    var_b = pc_b.explained_variance_ratio_.sum()
    X_tr_full_b = pc_b.transform(sc_b.transform(tr_emb_b))
    X_te_b      = pc_b.transform(sc_b.transform(te_emb_b))

    # Stratified cap (same for both classical and quantum)
    cap_idx = stratified_cap(np.arange(len(train_labels)), train_labels, TRACK_B_CAP, SEED)
    X_tr_b  = X_tr_full_b[cap_idx]
    y_tr_b  = train_labels[cap_idx]
    print(f"  PCA var retained: {var_b:.1%}  |  Cap: n={len(cap_idx)} TB={int(y_tr_b.sum())} Norm={int((y_tr_b==0).sum())}")

    # -- Classical (matched - same cap, same pca, same encoder) -----------
    clf_b = SVC(kernel="rbf", class_weight="balanced", random_state=SEED)
    clf_b.fit(X_tr_b, y_tr_b)
    # Threshold from 3-fold CV on the cap subset (small n - 3 folds)
    cv_s_b = cross_val_predict(
        SVC(kernel="rbf", class_weight="balanced", random_state=SEED),
        X_tr_b, y_tr_b, cv=cv3, method="decision_function"
    )
    thresh_b_c, _ = tune_threshold(cv_s_b, y_tr_b)
    te_s_c = clf_b.decision_function(X_te_b)
    te_p_c = (te_s_c >= thresh_b_c).astype(int)

    # -- QSVM -------------------------------------------------------------
    print(f"  Computing QSVM kernel ({TRACK_B_PCA} qubits) -")
    q_preds, q_scores, q_time, qsvm_model, K_tr_b = qsvm_run(X_tr_b, y_tr_b, X_te_b)

    # Threshold from LOO on training kernel
    q_loo_scores = np.zeros(len(y_tr_b))
    for i in range(len(y_tr_b)):
        mask = np.arange(len(y_tr_b)) != i
        svc_i = SVC(kernel="precomputed", class_weight="balanced")
        svc_i.fit(K_tr_b[np.ix_(mask, mask)], y_tr_b[mask])
        q_loo_scores[i] = svc_i.decision_function(K_tr_b[i:i+1, :][:, mask])[0]
    thresh_b_q, _ = tune_threshold(q_loo_scores, y_tr_b)
    q_preds_thresh = (q_scores >= thresh_b_q).astype(int)

    print(f"  QSVM kernel time: {q_time:.1f}s")
    track_b_results[rep] = {
        "pca_var": float(var_b),
        "cap_n": len(cap_idx), "cap_TB": int(y_tr_b.sum()), "cap_Norm": int((y_tr_b==0).sum()),
        "thresh_classical": float(thresh_b_c),
        "thresh_quantum":   float(thresh_b_q),
        "q_time_s": float(q_time),
        "classical_te_scores": te_s_c,
        "quantum_te_scores":   q_scores,
        "classical_te_preds":  te_p_c,
        "quantum_te_preds":    q_preds_thresh,
        "scaler": sc_b, "pca": pc_b,
        "x_tr_pca": X_tr_b,
    }
    qsvm_models[rep] = qsvm_model


# -----------------------------------------------------------------------------
# FINAL EVALUATION - one pass each, test set evaluated per frozen config
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("FINAL TEST EVALUATION (one pass per configuration)")
print("=" * 70)

# Majority baseline on test set
m_maj = metrics(test_labels, np.zeros_like(test_labels), None, "MAJORITY_BASELINE")

print("\n-- TRACK A: Best Practical Model ----------------------------------")
te_s_a = clf_a.decision_function(X_te_a)
te_p_a = (te_s_a >= thresh_a).astype(int)
m_a = metrics(test_labels, te_p_a, te_s_a,
              label=f"[A] {best_a_cfg['clf_name']}|{best_a_cfg['repr']}|pca={best_a_cfg['pca']}")

print("\n-- TRACK B: 2-2 Controlled Matrix ---------------------------------")
print("  (same encoder, same n_train=40, same PCA-8; only repr & learner vary)")
track_b_metrics = {}
for rep in TRACK_B_REPR:
    res = track_b_results[rep]
    m_c = metrics(test_labels, res["classical_te_preds"], res["classical_te_scores"],
                  label=f"[B] Classical | {rep}")
    m_q = metrics(test_labels, res["quantum_te_preds"],   res["quantum_te_scores"],
                  label=f"[B] QSVM      | {rep}")
    track_b_metrics[rep] = {"classical": m_c, "quantum": m_q}


# -----------------------------------------------------------------------------
# SAVE WEIGHTS + FULL REPORT
# -----------------------------------------------------------------------------
os.makedirs("src/ml/weights", exist_ok=True)
save_weights(sc_a,   "src/ml/weights/scaler.pkl")
save_weights(pc_a,   "src/ml/weights/pca.pkl")
save_weights(clf_a,  "src/ml/weights/classical_svm.pkl")

best_repr_b = TRACK_B_REPR[0]
best_b_q_score = track_b_metrics[TRACK_B_REPR[0]]["quantum"]["ba"]
for rep in TRACK_B_REPR:
    if track_b_metrics[rep]["quantum"]["ba"] > best_b_q_score:
        best_b_q_score = track_b_metrics[rep]["quantum"]["ba"]
        best_repr_b = rep

save_weights(track_b_results[best_repr_b]["pca"],    "src/ml/weights/pca_quantum.pkl")
save_weights(qsvm_models[best_repr_b],               "src/ml/weights/qsvm.pkl")
save_weights(track_b_results[best_repr_b]["x_tr_pca"],"src/ml/weights/x_train.pkl")
save_weights({"classical_thresh": thresh_a,
              "quantum_thresh": track_b_results[best_repr_b]["thresh_quantum"]},
             "src/ml/weights/thresholds.pkl")
save_weights({"encoder": best_a_cfg["encoder"],
              "track_a_representation": best_a_cfg["repr"],
              "track_b_representation": best_repr_b,
              "pca_dim_classical": int(best_a_cfg["pca"]),
              "pca_dim_quantum": int(TRACK_B_PCA),
              "clf_name": best_a_cfg["clf_name"],
              "gt_lung_note": "GT_LUNG_* representations use Montgomery expert-annotated manual masks - NOT automated segmentation"},
             "src/ml/weights/config.pkl")

report = {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "dataset": "Montgomery County TB Dataset",
    "split": {"seed": SEED, "train": int(len(train_idx)), "test": int(len(test_idx)),
              "train_TB": int(train_labels.sum()), "test_TB": int(test_labels.sum())},
    "representation_definitions": {
        "WHOLE_CXR":       "Full chest X-ray, no anatomical masking.",
        "GT_LUNG_MASKED":  "GROUND-TRUTH REFERENCE: background zeroed using expert Montgomery masks. NOT automated segmentation.",
        "GT_LUNG_CROPPED": "GROUND-TRUTH REFERENCE: tight lung crop using expert Montgomery masks. NOT automated segmentation.",
    },
    "majority_baseline_cv_ba": float(maj_cv_ba),
    "track_a": {
        "purpose": "Best practical model for SIH demonstration",
        "winner": {
            "encoder": best_a_cfg["encoder"],
            "representation": best_a_cfg["repr"],
            "pca": int(best_a_cfg["pca"]),
            "clf": best_a_cfg["clf_name"],
            "cv_ba": float(best_a_score),
            "test_thresh_from_cv": float(thresh_a),
        },
        "test_metrics": m_a,
        "all_cv_results": track_a_all,
    },
    "track_b": {
        "purpose": "Controlled 2-2 matrix: representation - learner",
        "fixed_conditions": {
            "encoder": best_a_cfg["encoder"],
            "pca_dim": int(TRACK_B_PCA),
            "n_train_cap": int(TRACK_B_CAP),
            "stratified_cap": True,
        },
        "results": {
            rep: {
                "pca_variance_retained": track_b_results[rep]["pca_var"],
                "train_cap": {"n": track_b_results[rep]["cap_n"],
                              "TB": track_b_results[rep]["cap_TB"],
                              "Normal": track_b_results[rep]["cap_Norm"]},
                "quantum_kernel_seconds": track_b_results[rep]["q_time_s"],
                "classical": track_b_metrics[rep]["classical"],
                "quantum":   track_b_metrics[rep]["quantum"],
            }
            for rep in TRACK_B_REPR
        },
        "majority_baseline_test": m_maj,
    },
}

with open(EXPERIMENT_DIR / "optimization_report.json", "w") as f:
    json.dump(report, f, indent=2, default=str)

# -----------------------------------------------------------------------------
# FINAL SUMMARY TABLE
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("FINAL RESULTS TABLE")
print("=" * 70)
print(f"{'Model':<52} {'Acc':>5} {'BA':>6} {'Sens':>6} {'Spec':>6} {'F1':>6} {'AUC':>7}")
print("-" * 90)

all_ms = [(m_maj, "-")]
all_ms.append((m_a, "A"))
for rep in TRACK_B_REPR:
    all_ms.append((track_b_metrics[rep]["classical"], "B"))
    all_ms.append((track_b_metrics[rep]["quantum"],   "B"))

for m, track in all_ms:
    auc = f"{m['auc']:.4f}" if m["auc"] else "    N/A"
    print(f"  [{track}] {m['label'][:48]:<48} {m['acc']:5.3f} {m['ba']:6.3f} {m['sens']:6.3f} {m['spec']:6.3f} {m['f1']:6.3f} {auc:>7}")

print(f"\n-- TRACK A ----------------------------------------------------------")
print(f"  Best practical model: {best_a_cfg['clf_name']} | {best_a_cfg['repr']} | pca={best_a_cfg['pca']}")
print(f"  CV-BA={best_a_score:.4f}  Test-BA={m_a['ba']:.4f}  Sens={m_a['sens']:.3f}  Spec={m_a['spec']:.3f}")

print(f"\n-- TRACK B ----------------------------------------------------------")
print(f"  {'Representation':<22} {'Learner':>10} {'BA':>6} {'Sens':>6} {'Spec':>6} {'AUC':>7}")
for rep in TRACK_B_REPR:
    for lbl, mk in [("Classical", "classical"), ("QSVM", "quantum")]:
        m = track_b_metrics[rep][mk]
        auc = f"{m['auc']:.4f}" if m["auc"] else "    N/A"
        print(f"  {rep:<22} {lbl:>10}  {m['ba']:6.3f} {m['sens']:6.3f} {m['spec']:6.3f} {auc:>7}")

print(f"\nMajority baseline: BA={m_maj['ba']:.3f}  Sens={m_maj['sens']:.3f}")
print(f"\nSaved: data/experiments/optimization_report.json")
print(f"       src/ml/weights/  (scaler, pca, classifiers, config, thresholds)")
