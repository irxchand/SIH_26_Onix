"""
Quick smoke test -- run while backend is up on localhost:8000.

Usage:  python tests/quick_smoke.py
"""
import requests, json, sys, os

# Force UTF-8 on Windows
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

BASE = "http://localhost:8000"
PASS, FAIL = 0, 0

def check(label: str, ok: bool, detail: str = ""):
    global PASS, FAIL
    tag = "[PASS]" if ok else "[FAIL]"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    print(f"  {tag} {label}" + (f"  -- {detail}" if detail else ""))

print("=" * 60)
print("SMOKE TEST -- SIH 26 Backend")
print("=" * 60)

# --- 1. Health ---
print("\n[1] Health")
r = requests.get(f"{BASE}/api/v1/health")
check("GET /health returns 200", r.status_code == 200)

# --- 2. Queue ---
print("\n[2] Queue")
r = requests.get(f"{BASE}/api/v1/queue")
check("GET /queue returns 200", r.status_code == 200)
studies = r.json().get("studies", [])
check("Queue has studies", len(studies) > 0, f"count={len(studies)}")
study_id = studies[0]["id"] if studies else None

# --- 3. Quantum Circuit ASCII ---
print("\n[3] Quantum Circuit ASCII")
r = requests.get(f"{BASE}/api/v1/quantum/circuit/ascii")
check("GET /quantum/circuit/ascii returns 200", r.status_code == 200)
data = r.json()
has_ascii = bool(data.get("ascii"))
has_qasm = bool(data.get("qasm"))
check("Response contains 'ascii' field", has_ascii, f"len={len(data.get('ascii',''))}")
check("Response contains 'qasm' field", has_qasm)
check("ASCII contains qubit lines (q0, q1...)", "q0" in data.get("ascii", "").lower() or "q(0)" in data.get("ascii", ""))
if has_ascii:
    # Print first 3 lines as preview
    lines = data["ascii"].split("\n")[:3]
    for l in lines:
        print(f"        {l}")

# --- 4. Predict (Grad-CAM coords) ---
if study_id:
    print(f"\n[4] Predict  (study={study_id})")
    r = requests.get(f"{BASE}/api/v1/studies/{study_id}/predict")
    check("GET /predict returns 200", r.status_code == 200, f"took {r.elapsed.total_seconds():.1f}s")
    pred = r.json()
    check("Has 'prediction' field", "prediction" in pred, pred.get("prediction"))
    check("Has 'evidence' list", isinstance(pred.get("evidence"), list))
    ev = pred.get("evidence", [])
    if ev:
        e0 = ev[0]
        check("Evidence[0] has xPercent", "xPercent" in e0, f"x={e0.get('xPercent')}")
        check("Evidence[0] has yPercent", "yPercent" in e0, f"y={e0.get('yPercent')}")
        # Verify coords are NOT the old hardcoded random range (32-42, 45-60)
        x, y = e0.get("xPercent", 0), e0.get("yPercent", 0)
        looks_random = (32 <= x <= 42) and (45 <= y <= 60)
        check("Coords don't look like old random range", not looks_random,
              f"x={x:.1f} y={y:.1f}" + (" WARNING: suspiciously in old range" if looks_random else ""))
    check("execution_stage is QSVM_EVALUATION", pred.get("execution_stage") == "QSVM_EVALUATION")

    # --- 5. Evidence Notes ---
    print(f"\n[5] Evidence Notes  (study={study_id})")
    note_payload = {
        "id": "E-01",
        "note": "Smoke test note",
        "xPercent": 50.0,
        "yPercent": 50.0
    }
    r = requests.post(f"{BASE}/api/v1/studies/{study_id}/evidence-notes",
                       json=note_payload)
    check("POST /evidence-notes returns 200", r.status_code == 200)
    resp = r.json()
    check("Returns evidence with matching id", resp.get("evidence", {}).get("id") == "E-01")

    # Post again — should upsert, not duplicate
    note_payload["note"] = "Updated smoke note"
    r2 = requests.post(f"{BASE}/api/v1/studies/{study_id}/evidence-notes",
                        json=note_payload)
    check("Upsert returns 200", r2.status_code == 200)

    # --- 6. Accept / Reject ---
    print(f"\n[6] Accept/Reject  (study={study_id})")
    r = requests.post(f"{BASE}/api/v1/studies/{study_id}/status",
                       json={"status": "ACCEPTED"})
    check("POST /status ACCEPTED returns 200", r.status_code == 200)
    # Verify queue reflects it
    r = requests.get(f"{BASE}/api/v1/queue")
    statuses = {s["id"]: s["status"] for s in r.json().get("studies", [])}
    check("Study status updated to ACCEPTED", statuses.get(study_id) == "ACCEPTED",
          statuses.get(study_id, "NOT FOUND"))

else:
    print("\nWARNING: Skipping predict/notes/accept tests -- no studies in queue.")

# --- Summary ---
print("\n" + "=" * 60)
total = PASS + FAIL
print(f"RESULT: {PASS}/{total} passed" + (f", {FAIL} FAILED!" if FAIL else " ALL GOOD"))
print("=" * 60)
sys.exit(1 if FAIL else 0)
