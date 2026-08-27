# PROJECT CONTEXT

## 1. Project Identity

- **Project Name:** Anatomy-Grounded Hybrid Quantum AI for Early Disease Detection
- **Project Type:** SIH 2026 Software problem solution + research-oriented AI/QML prototype
- **Domain:** Quantum Machine Learning, Medical Imaging, AI-assisted early disease detection, Chest X-ray analysis
- **Target SIH Problem Statement:** SIH26139 — “Hybrid Quantum Machine Learning Platform for Early Disease Detection”
- **Sponsor:** Egreen Quanta
- **Track:** Software
- **Theme:** MedTech / BioTech / HealthTech
- **Team:** Six-member student team with combined AIML, cybersecurity, full-stack, LLM, research, frontend/UI, and presentation capabilities.
- **Current Stage:** Pre-internal-selection prototype and pitch preparation
- **Current Objective:** Clear the internal SIH selection round by demonstrating a credible, research-backed concept, a modular proof-of-work prototype, strong technical potential, and a compelling future research roadmap.
- **Long-term Objective:** Develop the selected SIH solution into a rigorous research programme and potentially a publishable paper, while preparing a competitive Grand Finale solution.

**Source status:** SIH26139, its title, Software track, sponsor and theme are confirmed by the uploaded SIH 2026 problem-statement catalogue. fileciteturn6file13

---

## 2. Executive Summary

The team intends to address SIH26139 through a **modular hybrid quantum-classical AI platform for early disease detection**, using **tuberculosis (TB) detection from chest X-rays (CXR)** as the first proof-of-work demonstrator.

The central research direction is not to assume that quantum machine learning is inherently superior. Instead, the project will investigate whether **anatomically grounded representations — specifically lung-restricted CXR representations — can make low-qubit hybrid QML more useful under limited-data, cross-dataset/domain-shift, calibration, and resource constraints**.

The current proposed pipeline is:

**CXR → preprocessing/quality check → lung segmentation → feature representation → dimensionality reduction → matched classical and quantum models → prediction → explanation/uncertainty → benchmark/reporting UI**

The immediate SIH objective is to demonstrate that this architecture is technically executable and has credible research potential. The internal pitch should present the project as an **evidence-driven research platform and proof of work**, not as a completed clinically validated product.

The long-term research objective is to determine which aspects of the architecture produce scientifically meaningful results. Potential research dimensions include segmentation effects, low-data learning behaviour, external validation, calibration/uncertainty, lesion-aware representations, quantum circuit/feature-map ablations, explanation quality, and resource-accounted benchmarking.

The supplied research dossier argues that generic “QML for TB” is not itself novel; the stronger opportunity is the controlled evaluation of anatomical grounding, low-qubit QML, robustness, calibration and fair classical comparison. fileciteturn5file0

---

## 3. Problem

### Problem Statement

The team is targeting:

> **SIH26139 — Hybrid Quantum Machine Learning Platform for Early Disease Detection**

The uploaded SIH catalogue confirms the PS as a Software problem sponsored by Egreen Quanta in the MedTech / BioTech / HealthTech theme. fileciteturn6file13

### Problem Context

For the initial demonstrator, the project focuses on TB screening from chest X-rays.

Research supplied during discovery establishes that:

- Classical deep-learning approaches have been extensively investigated for TB detection from CXR.
- Lung segmentation has been used to focus models on anatomically relevant regions.
- QML in healthcare and medical imaging remains an emerging area with inconsistent evidence of superiority over classical approaches.
- The relevant open opportunity is not simply “QML detects TB”, but whether carefully constrained representations and rigorous evaluation reveal useful properties of QML.
- Cross-dataset robustness, low-data behaviour, uncertainty/calibration, resource accounting, and clinically meaningful explanation remain insufficiently characterized in the relevant literature.

The supplied 2020 TB paper reported that classification using segmented lungs outperformed whole-X-ray classification in its experiments, making segmentation a meaningful baseline/experimental variable rather than a new claim. fileciteturn3file1

### Who Experiences the Problem

**Confirmed / research-backed at a broad level:**
- Healthcare systems and screening workflows can face limitations involving specialist availability, imaging variability, diagnostic workload and model trust.
- Low-resource settings are particularly relevant to TB screening in the supplied research.

**Not yet confirmed for this exact SIH deployment:**
- Specific hospital workflows
- Specific end-user organizations
- Exact clinical deployment environment
- Exact disease modality required by Egreen Quanta

### Current Alternatives / Existing Approaches

Established alternatives include:

- classical deep CNN/transfer-learning approaches;
- whole-CXR classification;
- segmentation-guided CXR classification;
- conventional explainability methods such as Grad-CAM/Score-CAM;
- emerging QML approaches using reduced image-derived features.

The supplied research explicitly warns that a simple “segmentation → deep features → QML classifier → explanation” pipeline is not demonstrably novel by itself. fileciteturn5file0

### Identified Opportunity

The current opportunity is to investigate the combination of:

**anatomical grounding + low-dimensional feature representation + hybrid quantum-classical learning + fair classical comparison + robustness/reliability evaluation**

without presupposing the direction of the final result.

---

## 4. Product / System Vision

## CURRENT TARGET

A research-oriented software platform that demonstrates:

1. CXR ingestion.
2. Preprocessing and quality checking.
3. Lung segmentation.
4. Whole-CXR and lung-only representations.
5. Deep feature extraction.
6. Dimensionality reduction into a small QML-compatible feature space.
7. Classical baseline prediction.
8. Quantum-kernel/QSVM prediction.
9. Comparison of classical and quantum outputs.
10. Basic visual explanation.
11. Benchmark/result visualization.
12. A clear non-clinical research disclaimer.

The immediate demonstrator should use **TB screening** as the initial task.

## LONG-TERM VISION

A generalizable early-disease-detection research platform in which:

- segmentation models can be replaced;
- feature encoders can be replaced;
- classical models can be replaced;
- quantum models can be replaced;
- explanation/uncertainty modules can be replaced;
- disease/task modules can be changed;
- new datasets can be plugged in;
- controlled experiments can be reproduced automatically.

Potential future extensions include:
- TB lesion-aware modelling;
- cross-dataset validation;
- pneumonia;
- uncertainty/calibration;
- neuro-symbolic reasoning;
- additional disease modalities;
- real/hardware-informed QML evaluation;
- low-resource deployment.

These are **future directions, not current implementation requirements**.

---

## 5. Target Users / Stakeholders

### Primary Current Stakeholder

**SIH internal evaluators / selection judges**

Goal:
- understand the problem quickly;
- see evidence that the team understands the domain;
- assess whether the architecture is credible;
- see proof that the team can execute;
- judge innovation and future potential.

### SIH Problem Sponsor

**Egreen Quanta**

Confirmed sponsor from the SIH catalogue. fileciteturn6file13

Research supplied during discovery indicates that Egreen Quanta publicly discusses applied QML/QNN and quantum-computing work. The supplied Perplexity dossier characterizes this as evidence of sponsor alignment, but also warns not to overstate company capabilities from a project-listing page. fileciteturn5file0

### Future Research Stakeholders

**Researchers / academic collaborators**

Potential goals:
- rigorously test the QML hypothesis;
- establish reproducible results;
- publish a paper.

**Potential clinical/domain experts**

Future role:
- clinical interpretation;
- validation of explanations;
- assessment of practical relevance.

No specific clinical collaborator has been confirmed yet.

### End Users of a Potential Future System

A future clinical screening/decision-support workflow may involve healthcare professionals, but this is **not currently validated or fixed**.

---

## 6. Core Use Cases

### Use Case 1 — CXR Research Screening Demonstration

**Actor:** Evaluator / researcher

**Objective:** Submit a CXR and observe the end-to-end research pipeline.

**Flow:**
CXR upload → preprocessing → lung segmentation → feature extraction → classical/quantum prediction → evidence visualization.

**Outcome:** A reproducible research prediction and visualization.

---

### Use Case 2 — Classical vs Quantum Benchmark

**Actor:** Researcher

**Objective:** Compare a classical model and QML model under matched feature conditions.

**Flow:**
Same representation → same dimensionality reduction → classical model vs quantum model → common evaluation.

**Outcome:** Comparative metrics and resource statistics.

---

### Use Case 3 — Whole-CXR vs Lung-Only Ablation

**Actor:** Researcher

**Objective:** Test the effect of anatomical restriction.

**Flow:**
Whole CXR → model

and

Lung-only CXR → model

**Outcome:** Evidence about whether anatomical grounding changes performance.

---

### Use Case 4 — Internal SIH Demonstration

**Actor:** SIH evaluator

**Objective:** See a clear, stable proof of execution.

**Flow:**
Representative known-good demonstration image → full pipeline → clean visualization → benchmark evidence.

**Outcome:** Confidence that the team can execute the larger research roadmap.

---

### Use Case 5 — Personal CXR Demonstration

**Actor:** Team member

**Objective:** Demonstrate that the UI can process a real JPEG CXR.

**Flow:** Personal CXR → model inference.

**Restrictions:** This image is demonstration-only and must not be included in training, validation, scientific statistics, or medical claims.

**Outcome:** A relatable demonstration of the interface, explicitly labelled as research-only.

---

## 7. Current Scope

### MUST HAVE

- SIH26139-aligned hybrid classical/QML direction.
- TB CXR initial demonstrator.
- Working preprocessing pipeline.
- Working lung segmentation inference.
- Whole-CXR and lung-only representations.
- Deep feature extraction.
- Small-dimensional feature reduction.
- Classical baseline.
- Qiskit-based quantum kernel/QSVM proof-of-work.
- Fair comparison using the same reduced feature space.
- At least one real benchmark on available research data.
- Basic visual explanation.
- Simple working interface.
- Reproducible stored experiment results.
- Clear non-clinical safety language.
- Architecture suitable for later replacement of modules.

### SHOULD HAVE

- VQC backup experiment.
- Low-data comparison.
- One source-separated/external validation experiment.
- Confidence intervals/bootstrapping where feasible.
- Shot-based/noisy simulation.
- Resource and runtime comparison.
- Improved calibration/uncertainty handling.

### COULD HAVE

- Lesion-aware TBX11K representation.
- More advanced XAI.
- Neuro-symbolic reasoning.
- Additional disease task.
- Hardware execution test.
- Automatically generated report.
- Additional modern encoders.

### DEFERRED

- Final paper contribution.
- Final quantum architecture choice.
- Final segmentation architecture.
- Final disease scope beyond the TB demonstrator.
- Clinical validation methodology.
- Real quantum hardware evaluation.
- Full uncertainty methodology.
- Neuro-symbolic reasoning implementation.

### OUT OF SCOPE FOR CURRENT 3–4 DAY PROTOTYPE

- Digital twin.
- IoT sensor network.
- EHR integration.
- Federated learning.
- Blockchain.
- Genomics/multimodal clinical fusion.
- Full hospital deployment.
- Autonomous diagnosis.
- Large custom segmentation model.
- Large quantum circuits.
- Quanvolutional architecture.
- Broad multi-disease platform beyond what is necessary for the first proof-of-work.

### CURRENT MVP / FIRST USEFUL VERSION

The first useful version is:

> **CXR → preprocessing → lung segmentation → whole/lung-only branches → pretrained feature extraction → PCA → matched RBF-SVM and Qiskit QSVM → benchmark results → explanation visualization → simple UI.**

The supplied Perplexity dossier explicitly recommends this as the strongest immediate proof-of-work direction. fileciteturn5file0

---

## 8. Success Criteria

### Technical Success

The internal prototype succeeds if the team can demonstrate, with real code and real outputs:

- CXR ingestion;
- lung segmentation;
- feature extraction;
- classical inference;
- QML inference;
- comparative evaluation;
- basic explanation;
- functioning end-to-end UI.

No numerical performance target has been approved.

### Product / Demonstration Success

The internal round succeeds if:

- the demo is reliable;
- the architecture is understandable;
- the research gap is credible;
- the proof-of-work visibly exists;
- the team can explain why the architecture is relevant to SIH26139;
- the presentation communicates research potential without unsupported claims.

### Research Success

The longer-term research succeeds if it produces a defensible empirical answer to one or more of:

- whether anatomical grounding improves QML behaviour;
- whether QML behaves differently under limited-data regimes;
- whether it generalizes better or worse across datasets;
- whether it offers any meaningful resource or robustness trade-off;
- whether explanations/uncertainty can be made trustworthy.

A negative result is acceptable and potentially publishable if the evaluation is rigorous and reproducible. fileciteturn6file8

### Publication Success

No paper has been guaranteed.

Potential publication contribution is expected to emerge from experimental evidence rather than from a predetermined claim.

---

## 9. Constraints

### Time

**Confirmed:** the immediate SIH internal prototype window is approximately **27–30 August**.

The immediate priority is the **internal SIH selection**, followed by reaching the next SIH selection stage, and only then expanding the system substantially for research and Grand Finale work.

### Team

**Confirmed:** six-person team.

Capabilities described by the human:
- research;
- LLM;
- frontend;
- AI/ML;
- cybersecurity;
- full-stack;
- broad generalist capability;
- presentation/PPT capability.

The exact assignment of people to engineering roles is still an Antigravity planning decision.

### Compute / Infrastructure

**Confirmed:**
- Qiskit available;
- college lab available;
- Mac M5 available.

Exact GPU specifications and lab compute availability have not yet been verified.

### Quantum Hardware

**Confirmed:** Qiskit is available.

**Not confirmed:** actual quantum hardware access suitable for this project.

The current direction therefore assumes simulator-first execution.

### Data

Initial research candidates:
- Shenzhen TB;
- Montgomery TB;
- TBX11K for later research scale.

The supplied research dossier recommends Shenzhen/Montgomery for rapid proof-of-work and TBX11K for later scale. fileciteturn5file0

### Personal Medical Image

A personal CXR JPEG exists.

It is not to be used as training or scientific validation evidence. It may be used only as a private/representative UI demonstration with an explicit research-only disclaimer.

### Academic Constraint

The project needs to support a future research paper.

The architecture therefore must remain modular and experimentally reproducible.

---

## 10. Research Foundation

## Finding 1 — TB CXR classification is already established

### Finding
Classical TB CXR classification has extensive prior work.

### Source
The supplied 2020 paper reviews multiple prior CNN/transfer-learning TB detection approaches and reports strong performance from deep models. fileciteturn6file5turn6file12

### Relevance
A new project cannot reasonably claim that simply classifying TB from CXR is novel.

### Consequence
TB classification must be used as a baseline/domain while novelty is pursued elsewhere.

### Confidence
HIGH

---

## Finding 2 — Lung segmentation can affect TB classification

### Finding
The supplied 2020 study compared whole CXR and segmented lung images and found segmented-lung classification performed better in its experiments. It reported DenseNet201 performance of 98.6% accuracy on segmented lung images compared with 96.47% for the best whole-image result in its study. fileciteturn3file1

### Relevance
Segmentation is a legitimate experimental variable and motivates testing anatomical restriction.

### Consequence
The project should retain both whole-CXR and lung-only conditions.

### Confidence
HIGH for the reported study; not a generalized claim that segmentation always improves all datasets/models.

---

## Finding 3 — The generic “QML + TB” claim is not sufficiently novel

### Finding
The supplied Perplexity dossier states that generic TB detection with QML already has some evidence/studies and therefore is not, by itself, a sufficient novelty claim. fileciteturn5file0

### Relevance
The project must not pitch “we are the first to use QML for TB.”

### Consequence
Novelty must be tied to controlled experimental questions such as segmentation effects, external validation, low-data behaviour, calibration, robustness or resource accounting.

### Confidence
MEDIUM-HIGH; should be revalidated against the final literature review before any paper novelty claim.

---

## Finding 4 — QML medical evidence is still immature/inconsistent

### Finding
The supplied research reports that QML in digital health has not consistently demonstrated superiority over classical methods and that realistic/noisy/hardware-aware evaluation is limited. fileciteturn5file0

### Relevance
This creates a legitimate scientific reason to benchmark rather than assume benefit.

### Consequence
The system must include strong classical controls and should record resource cost.

### Confidence
MEDIUM-HIGH based on the supplied systematic-review summary; exact review details should be verified before publication.

---

## Finding 5 — External generalization is important

### Finding
The supplied research identifies cross-dataset/source generalization as a weakly characterized dimension in QML medical imaging. fileciteturn5file0

### Relevance
A model that works only on one source may not be meaningful.

### Consequence
Source-separated testing such as Shenzhen → Montgomery should become a post-selection experiment.

### Confidence
MEDIUM-HIGH

---

## Finding 6 — Low-data behaviour is an attractive research question

### Finding
The supplied dossier identifies low-data learning curves as a candidate research direction and notes that claims about QML's small-data usefulness are common but insufficiently supported by rigorous matched medical-image evidence. fileciteturn5file0

### Relevance
This offers a research question better suited to the QML hypothesis than headline accuracy alone.

### Consequence
The research plan should include 10/25/50/75/100% training-size comparisons when feasible.

### Confidence
MEDIUM

---

## Finding 7 — Explanation is more complicated than a heatmap

### Finding
The supplied neuro-symbolic research distinguishes post-hoc saliency (“where the model looked”) from clinically meaningful reasoning about why a finding supports a diagnosis. fileciteturn3file0

### Relevance
Grad-CAM can be useful for the prototype, but should not be presented as complete clinical reasoning.

### Consequence
The prototype may use visual explanation, while stronger concept/rule-based explanation remains future work.

### Confidence
HIGH

---

## Finding 8 — Lesion-aware research is promising but data-limited

### Finding
TBX11K provides TB-area bounding-box annotations, while classic TB datasets provide much smaller lung-level segmentation resources. The research gap analysis notes that dense lesion-level annotation is comparatively scarce. fileciteturn3file2

### Relevance
Lesion-aware QML may provide another research direction.

### Consequence
Treat lesion ROI modelling as a post-selection research extension rather than an immediate requirement.

### Confidence
MEDIUM-HIGH

---

## Finding 9 — Resource accounting matters

### Finding
The supplied dossier emphasizes quantum encoding cost, circuit size/depth, shots, simulation/runtime cost and fair matched classical comparisons. fileciteturn5file0

### Relevance
A QML result without resource accounting is difficult to interpret.

### Consequence
The experiment framework should retain qubits, depth, shots/evaluations and runtime where possible.

### Confidence
HIGH as a methodological recommendation; exact quantitative thresholds remain open.

---

## Finding 10 — Current SIH catalogue confirms problem identity, not all detailed requirements

### Finding
The supplied SIH PDF confirms SIH26139 as a Software PS sponsored by Egreen Quanta with the title “Hybrid Quantum Machine Learning Platform for Early Disease Detection.” fileciteturn6file13

### Relevance
The project can confidently align to hybrid QML and early disease detection at the concept level.

### Consequence
Detailed SIH requirement claims should be verified against the authenticated full PS before final submission. The supplied Perplexity dossier specifically warns that the publicly indexed material may not expose all detailed requirements. fileciteturn5file0

### Confidence
HIGH for the catalogue facts; MEDIUM/LOW for any unverified detailed requirement.

---

## 11. Research Gaps / Open Questions

### KNOWN

The literature already contains:
- classical TB CXR classification;
- segmentation-guided TB detection;
- QML medical-imaging research;
- some pulmonary/TB QML exploration;
- common saliency/XAI approaches.

### UNKNOWN / INSUFFICIENTLY ESTABLISHED

The project still needs evidence regarding:

1. Whether lung segmentation specifically improves low-qubit QML.
2. Whether anatomically restricted embeddings improve cross-source generalization.
3. Whether QML behaves differently from matched classical models under reduced training data.
4. Whether any observed QML gains survive repeated experiments and confidence intervals.
5. Whether QML has a useful calibration/uncertainty profile.
6. Whether resource cost is justified by any performance/robustness benefit.
7. Whether lesion-aware representations improve QML behaviour.
8. Whether quantum models can produce useful, honest explanations beyond model-score output.

### PRIMARY CURRENT HYPOTHESIS

> **Lung-field restriction may produce a more stable and relevant low-dimensional representation for hybrid quantum-classical learning, potentially improving generalization and/or low-data behaviour relative to matched classical approaches.**

This is a **HYPOTHESIS**, not an established result.

### Candidate Research Question

> **Does lung segmentation improve the external generalization, calibration, and low-data performance of low-qubit quantum-kernel TB classifiers based on fixed CXR embeddings, relative to matched classical classifiers?**

This is the current leading candidate; it is not yet an approved final paper title/question.

---

## 12. Human-Approved Decisions

### Decision 1

**CONTEXT:** SIH 2026 includes a Software PS SIH26139 for Hybrid Quantum Machine Learning Platform for Early Disease Detection.

**WHY:** It aligns with the team's technical capabilities and research interest.

**ALTERNATIVES CONSIDERED:** Other SIH Software PSs, including cybersecurity options.

**SELECTED OPTION:** Pursue SIH26139 seriously.

**RATIONALE:** Existing team research direction and QML interest create a potentially strong starting position.

**TRADE-OFFS:** Requires specialized QML research and carries greater experimental uncertainty than conventional ML.

**STATUS:** APPROVED

---

### Decision 2

**CONTEXT:** A research direction around TB CXR, segmentation and QML is available.

**WHY:** It offers a concrete, demonstrable medical-imaging use case and a researchable experimental structure.

**ALTERNATIVES CONSIDERED:** Starting with a broader disease platform or another application.

**SELECTED OPTION:** Use TB CXR as the initial demonstrator.

**RATIONALE:** Public datasets and existing segmentation/classification literature make rapid proof-of-work feasible.

**TRADE-OFFS:** TB itself cannot be treated as novel; research novelty must come from the experimental question.

**STATUS:** APPROVED

---

### Decision 3

**CONTEXT:** SIH internal selection is the immediate priority.

**WHY:** The team has only a short prototype/presentation window.

**SELECTED OPTION:** Build a credible proof-of-work and pitch first; conduct deeper research after progressing.

**RATIONALE:** The paper is a longer-term objective and cannot be responsibly completed in the immediate window.

**TRADE-OFFS:** Some components will initially be preliminary rather than fully validated.

**STATUS:** APPROVED

---

### Decision 4

**CONTEXT:** The architecture must survive changing research conclusions.

**SELECTED OPTION:** Use a modular architecture where segmentation, encoders, classical models, quantum models and explainability modules can be replaced independently.

**STATUS:** APPROVED

---

### Decision 5

**CONTEXT:** Quantum benefit is not yet established.

**SELECTED OPTION:** Treat quantum advantage as a hypothesis to test, not a claim.

**STATUS:** APPROVED

---

### Decision 6

**CONTEXT:** Internal demo reliability matters.

**SELECTED OPTION:** A representative, reproducible demo path may use cached/precomputed outputs from real experiments, but no fabricated scientific values may be presented.

**STATUS:** APPROVED / SUBJECT TO HONEST RESULT LABELING

---

### Decision 7

**CONTEXT:** Personal CXR is available.

**SELECTED OPTION:** It may be used for a relatable demonstration only, never for training or reported validation, and never as a personal medical diagnosis.

**STATUS:** APPROVED

---

## 13. Initial Technical Direction

### CONFIRMED

- Qiskit is available.
- TB CXR is the initial demonstrator.
- Modularity is a core architectural requirement.
- The platform should compare classical and quantum approaches.
- The system should support a proof-of-work demo.

### RECOMMENDED

- Lung segmentation before feature extraction.
- Frozen pretrained CNN embeddings initially.
- PCA to a small feature dimension.
- Quantum kernel/QSVM as primary QML method.
- RBF-SVM on identical reduced features as the matched classical comparator.
- Streamlit or similarly lightweight UI for rapid prototyping.

These were proposed during discovery and supported by the supplied Perplexity analysis, but the exact implementation choices remain **RECOMMENDATIONS**, not immutable human-approved requirements. fileciteturn5file0

### TENTATIVE

- DenseNet-121 as initial encoder.
- 4–8 quantum features/qubits.
- Shallow VQC as backup.
- Grad-CAM for initial classical visual explanation.
- Shenzhen/Montgomery for immediate demonstrator.
- TBX11K for later scale.

### OPEN

- Exact segmentation implementation.
- Exact encoder.
- Exact quantum feature map.
- Exact Qiskit version and APIs.
- Real hardware feasibility.
- Final calibration/uncertainty method.
- Final dataset mix.
- Final paper contribution.

---

## 14. Known System Boundaries

### Known/Intended Inputs

- Chest X-ray images.
- Research dataset metadata.
- Configuration for model/experiment selection.

### Known/Intended Outputs

- Model prediction/score.
- Benchmark metrics.
- Segmentation visualization.
- Basic explanation.
- Resource/experiment metadata.

### External Dependencies

- Qiskit.
- PyTorch/related ML ecosystem.
- Public research datasets.
- Potentially pretrained model weights.
- Local/college compute.

### Not Yet Defined

- EHR APIs.
- Hospital systems.
- Clinical device interfaces.
- Quantum hardware APIs beyond possible future use.
- Production cloud infrastructure.

---

## 15. Risks

### Risk 1 — QML does not outperform classical models

**Why It Matters:** Could weaken a simplistic “quantum is better” pitch.

**Evidence:** Existing QML healthcare literature does not consistently establish superiority. fileciteturn5file0

**Potential Impact:** Medium/high for a naive pitch; lower for a research-oriented pitch.

**Current Mitigation:** Position the project as a controlled investigation and include matched classical baselines.

**Remaining Uncertainty:** Which metrics or conditions may favour QML remain unknown.

---

### Risk 2 — Claimed novelty already exists

**Why It Matters:** “QML + TB” and “segmentation + TB” are not sufficient novelty claims.

**Evidence:** Supplied literature and Perplexity dossier. fileciteturn3file1turn5file0

**Potential Impact:** High for paper novelty.

**Current Mitigation:** Use a gap matrix and verify exact intersections before final research claims.

**Remaining Uncertainty:** Final literature coverage is not yet exhaustive.

---

### Risk 3 — Dataset limitations

**Why It Matters:** Small TB datasets and source differences can distort conclusions.

**Evidence:** Research dossier notes limited TB datasets and source/domain differences. fileciteturn3file2turn5file0

**Potential Impact:** High for research validity.

**Current Mitigation:** Patient/source-aware splitting and later external validation.

**Remaining Uncertainty:** Exact metadata/availability and licensing must be rechecked when implementing.

---

### Risk 4 — Data leakage

**Why It Matters:** Could create artificially high performance.

**Evidence:** Standard medical-imaging methodological concern; explicitly identified in the supplied experiment protocol.

**Potential Impact:** High.

**Current Mitigation:** Patient-level splitting where possible; fit preprocessing/PCA only on training data.

**Remaining Uncertainty:** Dataset-specific metadata availability.

---

### Risk 5 — Quantum simulation cost

**Why It Matters:** Quantum kernels and repeated circuit evaluation can become expensive.

**Evidence:** Supplied QML research emphasizes encoding and simulation costs. fileciteturn5file0

**Potential Impact:** Medium/high.

**Current Mitigation:** Small feature dimension and small-qubit QSVM; simulator-first.

**Remaining Uncertainty:** Exact runtime under selected dataset size.

---

### Risk 6 — Over-scoping

**Why It Matters:** The team could attempt segmentation + QML + explainability + IoT + digital twin + neuro-symbolic AI simultaneously.

**Evidence:** Earlier discovery discussion deliberately rejected this approach.

**Potential Impact:** Very high for internal deadline.

**Current Mitigation:** Explicit non-goals and staged roadmap.

**Remaining Uncertainty:** Team discipline during implementation.

---

### Risk 7 — Clinical overclaiming

**Why It Matters:** A research prototype is not a medical diagnostic device.

**Evidence:** Research materials emphasize clinical validation, uncertainty and regulatory issues.

**Potential Impact:** High reputational and scientific risk.

**Current Mitigation:** Use screening/research terminology. Do not provide personal diagnosis.

**Remaining Uncertainty:** Future regulatory pathway if project progresses beyond research.

---

## 16. Assumptions

### ASSUMPTION
Qiskit simulator access is sufficient for the immediate proof-of-work.

**WHY:** Hardware access has not been confirmed.

**EVIDENCE:** Qiskit availability is confirmed; hardware availability is not.

**VALIDATED?** NO

**CONSEQUENCE IF WRONG:** QML implementation path must be adjusted.

---

### ASSUMPTION
A pretrained lung segmentation solution can be obtained and used quickly.

**WHY:** Four-day window makes training from scratch inappropriate.

**EVIDENCE:** Research and implementation recommendations.

**VALIDATED?** NO

**CONSEQUENCE IF WRONG:** Prototype scope must be reduced or segmentation implementation changed.

---

### ASSUMPTION
Shenzhen/Montgomery can be accessed quickly enough for the internal prototype.

**WHY:** Recommended by the supplied dossier.

**EVIDENCE:** Public research datasets described in the supplied research.

**VALIDATED?** NO

**CONSEQUENCE IF WRONG:** Use another verified research dataset for proof-of-work.

---

### ASSUMPTION
The public SIH catalogue is sufficient to understand the high-level scope.

**WHY:** Detailed authenticated PS content was not present in the supplied catalogue.

**EVIDENCE:** Perplexity explicitly warned of this limitation. fileciteturn5file0

**VALIDATED?** NO

**CONSEQUENCE IF WRONG:** Architecture/pitch may need modification after full PS verification.

---

### ASSUMPTION
The architecture can later be generalized beyond TB.

**WHY:** SIH title is disease-agnostic.

**EVIDENCE:** PS title and modular design.

**VALIDATED?** NO

**CONSEQUENCE IF WRONG:** TB may need to remain the primary domain.

---

## 17. Open Questions

### Question
What is the authenticated, complete official SIH26139 detailed description and evaluation rubric?

**WHY IT MATTERS:** Could materially alter requirements.

**WHAT IT AFFECTS:** Pitch, architecture, prototype scope.

**BLOCKING?** YES before final external claims.

**OWNER:** HUMAN

---

### Question
Does an existing paper already perform the exact whole-CXR vs lung-only + matched classical vs QSVM + external TB validation experiment?

**WHY IT MATTERS:** Determines paper novelty.

**WHAT IT AFFECTS:** Research gap.

**BLOCKING?** YES for final novelty claim; NO for initial prototype.

**OWNER:** AGENT / FUTURE RESEARCH

---

### Question
Which quantum method produces the strongest practical baseline: QSVM, VQC or another hybrid method?

**BLOCKING?** NO for immediate MVP; QSVM is current recommendation.

**OWNER:** AGENT

---

### Question
Which encoder and segmentation model provide the best accuracy/compute trade-off?

**BLOCKING?** NO

**OWNER:** AGENT

---

### Question
Can actual quantum hardware be accessed?

**BLOCKING?** NO for immediate simulator proof-of-work; potentially important later.

**OWNER:** HUMAN

---

### Question
Which final experimental result will become the paper's central contribution?

**BLOCKING?** NO now; YES before paper writing.

**OWNER:** FUTURE RESEARCH

---

## 18. Deferred Decisions

### Final Quantum Architecture

**WHY DEFERRED:** Evidence has not yet been generated.

**REVISIT WHEN:** Initial QSVM/VQC experiments exist.

**EVIDENCE REQUIRED:** Comparative performance + resource data.

---

### Final Paper Research Question

**WHY DEFERRED:** Current question is a leading hypothesis, not proven gap.

**REVISIT WHEN:** Comprehensive literature matrix + initial experiments exist.

**EVIDENCE REQUIRED:** Verified literature gap and empirical feasibility.

---

### Multi-disease Scope

**WHY DEFERRED:** TB is sufficient for first proof.

**REVISIT WHEN:** TB module is stable.

**EVIDENCE REQUIRED:** Dataset availability and SIH relevance.

---

### Neuro-symbolic Layer

**WHY DEFERRED:** High scope/cost relative to initial SIH objective.

**REVISIT WHEN:** Core segmentation/QML benchmark is stable.

**EVIDENCE REQUIRED:** Clear explanation gap and sufficient domain knowledge.

---

### Real Hardware Evaluation

**WHY DEFERRED:** Hardware access/cost not established.

**REVISIT WHEN:** Simulator experiments justify it.

**EVIDENCE REQUIRED:** Access + meaningful hardware comparison plan.

---

## 19. Explicit Non-Goals

The following must not silently become current requirements:

- “Quantum advantage” as a predetermined objective.
- Clinical-grade diagnosis.
- Replacing radiologists.
- Autonomous medical decisions.
- Treating the personal CXR as clinical evidence.
- Claiming first-ever novelty without verification.
- Digital twin implementation.
- IoT deployment.
- Federated learning.
- Blockchain.
- Genomic multimodal fusion.
- Full EHR integration.
- Hospital deployment.
- Large-scale custom segmentation training during the internal prototype period.
- Quanvolutional architectures during the MVP.
- Large quantum circuits.
- Building many redundant CNN baselines merely for model count.
- Adding an LLM chatbot simply because an LLM-capable team member exists.

---

## 20. Existing Work

### 1. Research Gap Analysis Document

**EXISTS:** Yes

**STATUS:** Preliminary literature/research-gap synthesis.

**RELEVANCE:** High.

**KNOWN LIMITATIONS:** It is a synthesis, not proof that every gap claim is exhaustive or permanently novel. fileciteturn6file14

---

### 2. Explainable Neuro-Symbolic AI Research Document

**EXISTS:** Yes

**STATUS:** Literature/research roadmap.

**RELEVANCE:** High for future explanation/neuro-symbolic direction.

**KNOWN LIMITATIONS:** It describes a broad research agenda, not an implemented project. fileciteturn6file6

---

### 3. 2020 TB Segmentation/CNN Paper

**EXISTS:** Yes

**STATUS:** Established peer-reviewed reference.

**RELEVANCE:** High for segmentation motivation and baseline understanding.

**KNOWN LIMITATIONS:** Old relative to 2026 state of the art; cannot alone establish current novelty or current best performance. fileciteturn6file5

---

### 4. Perplexity SIH26139 Research Dossier

**EXISTS:** Yes

**STATUS:** Discovery research output.

**RELEVANCE:** Very high for current strategic direction, candidate gaps, datasets, model choices and experiment design.

**KNOWN LIMITATIONS:** Must be independently verified before becoming final scientific claims. fileciteturn5file0

---

### 5. SIH 2026 Problem-Statement Catalogue

**EXISTS:** Yes

**STATUS:** Current project source.

**RELEVANCE:** Confirms SIH26139 identity and classification.

**KNOWN LIMITATIONS:** Uploaded catalogue may not include the full authenticated detailed PS description. fileciteturn6file13

---

### 6. Personal CXR JPEG

**EXISTS:** Yes

**STATUS:** Available for potential demo only.

**RELEVANCE:** UI demonstration.

**KNOWN LIMITATIONS:** Not scientific evidence; must not be used for training/validation or medical claims.

---

## 21. Important Engineering Considerations

### Modularity

The architecture must permit replacing:

- segmentation;
- feature encoder;
- dimensionality reduction;
- classical classifier;
- quantum classifier;
- explanation method;
- uncertainty method;
- disease/task.

This is an important project requirement established during discovery.

### Reproducibility

Experiments should record configuration, seed, dataset, representation, model parameters, quantum settings, metrics and runtime.

### Fair Benchmarking

The strongest comparison uses identical reduced features for RBF-SVM and QSVM so that the downstream learning method is the principal difference.

### Leakage Control

Patient-level splitting should be used where metadata permits; scaler/PCA/model selection must be fit using training data only.

### Reliability

The UI must communicate whether a value is:
- measured;
- preliminary;
- demonstrative;
- planned.

### Explainability

Do not present Grad-CAM as proof of causal or clinical reasoning.

### Healthcare Safety

Use screening/research terminology. Do not provide personal diagnosis.

### Performance

Small-dimensional quantum representations are preferred for MVP feasibility.

### Maintainability

Avoid hard-coding model choices into UI or pipeline logic.

### Scope Control

The prototype should prioritize an end-to-end working path over breadth of features.

---

## 22. Future Direction

**FUTURE / NOT CURRENT SCOPE**

Potential research sequence:

1. Whole CXR vs segmented lung.
2. Classical vs QSVM.
3. Low-data learning curves.
4. Cross-dataset/source-separated evaluation.
5. PCA/feature-map/circuit-depth ablations.
6. Calibration and uncertainty.
7. TBX11K lesion-aware experiments.
8. Explanation quality evaluation.
9. Noisy/real-hardware-informed execution.
10. Possible pneumonia extension.
11. Possible neuro-symbolic reasoning.
12. Final paper based on the strongest empirically supported finding.

The exact order may change based on evidence.

The research paper should report **what experiments show**, not what the initial pitch hoped they would show.

---

## 23. Antigravity Handoff Notes

### What Antigravity Must Understand

This is both:

1. an **SIH Software prototype**, and
2. a **potential research platform**.

The immediate goal is to clear the internal selection round.

The longer-term goal is to turn the platform into a rigorous research programme and potentially a paper.

The central research idea is **not “quantum is better.”**

It is:

> **Investigate whether anatomical grounding and low-dimensional representations create conditions under which low-qubit hybrid QML provides measurable benefits or meaningful trade-offs relative to matched classical models.**

---

### What Antigravity Must Preserve

- SIH26139 target.
- TB CXR as initial demonstrator.
- Modular design.
- Whole-vs-segmented comparison.
- Classical-vs-quantum comparison.
- Research integrity.
- Reproducibility.
- Ability to expand after internal selection.
- Clear distinction between measured results and future hypotheses.
- Non-clinical framing.

---

### What Antigravity Must NOT Assume

Do not assume:

- quantum advantage exists;
- the exact final research gap is already proven;
- the supplied literature review is exhaustive;
- TB is the only eventual disease;
- segmentation is necessarily the best preprocessing method;
- QSVM is the final research winner;
- Grad-CAM is sufficient clinical explainability;
- the prototype is clinically deployable;
- the personal CXR proves or disproves any disease;
- any dataset license permits unrestricted commercial/clinical use;
- real quantum hardware is available;
- SIH's detailed authenticated evaluation requirements are fully represented by the uploaded catalogue.

---

### What Antigravity Must Investigate

Before finalizing the Project SOT:

1. Full authenticated SIH26139 requirements.
2. Current Qiskit environment/version.
3. Available compute/GPU.
4. Dataset access and current licensing.
5. Pretrained segmentation options.
6. Best practical initial encoder.
7. Qiskit quantum-kernel/QSVM implementation path.
8. Reproducible whole-vs-lung benchmark.
9. Exact novelty landscape before any “first” claim.
10. Whether external validation is feasible within available datasets/resources.

---

### What Antigravity Must Not Build Yet

Do not build as part of the immediate MVP:

- digital twin;
- IoT;
- federated learning;
- blockchain;
- genomics;
- EHR integration;
- hospital deployment;
- full neuro-symbolic reasoning system;
- multi-disease platform;
- large custom quantum architecture;
- quanvolution.

---

### Important Research It Should Read

1. **Reliable Tuberculosis Detection Using Chest X-Ray With Deep Learning, Segmentation and Visualization** — establishes segmentation/classical TB background and provides a historical benchmark. fileciteturn3file1
2. **Research Gap Analysis: AI-Enabled Diagnosis of Pneumonia and Tuberculosis** — summarizes candidate gaps across QML, segmentation, explainability, uncertainty and deployment. fileciteturn3file2
3. **Explainable Neuro-Symbolic AI for Pneumonia and Tuberculosis Diagnosis** — useful for future trustworthy explanation/neuro-symbolic work. fileciteturn3file0
4. **Perplexity SIH26139 Research Dossier** — current strategic synthesis and candidate experimental programme; verify claims before formal publication. fileciteturn5file0

---

### Important Existing Work It Should Inspect

- Research-gap document.
- Neuro-symbolic research document.
- 2020 TB segmentation paper.
- SIH 2026 problem-statement catalogue.
- Perplexity research dossier.
- Personal CXR only for demo integration if the human explicitly provides/approves its use.

---

### Important Human Decisions Already Made

- Pursue SIH26139.
- Software-only.
- TB CXR as initial demonstrator.
- Internal selection is the immediate priority.
- Build proof-of-work before deep paper research.
- Architecture must remain modular.
- Classical and quantum models must be compared.
- Quantum advantage must not be assumed.
- Personal CXR can be a demonstration case only.
- Scope must remain controlled during the 27–30 August prototype window.

---

## 24. Recommended Project Classification

**PROVISIONAL — ANTIGRAVITY WILL CONFIRM DURING PROJECT INITIALIZATION**

### Classification: Research / AI System

The project is more than a conventional hackathon prototype because:

- the team explicitly intends to conduct research and potentially publish;
- the central system is an experimental AI/QML platform;
- scientific benchmarking and reproducibility are important;
- the final research contribution is not yet known;
- medical AI creates higher validation/safety requirements.

For the **immediate SIH internal round**, implementation should nevertheless be treated operationally as a **Prototype / Hackathon increment** inside the larger Research / AI System classification.

---

## 25. Context Integrity Summary

### CONFIRMED FACTS

- SIH26139 is a Software problem titled **“Hybrid Quantum Machine Learning Platform for Early Disease Detection”** and is attributed to Egreen Quanta in the uploaded SIH catalogue. fileciteturn6file13
- The team has six members.
- The team has AIML, cybersecurity, full-stack, LLM, research, frontend and presentation capability.
- Qiskit, college lab resources and a Mac M5 are available.
- TB CXR is the initial chosen demonstrator.
- The immediate SIH internal deadline is the priority.
- A personal CXR JPEG exists for potential demonstration.
- The architecture should be modular.
- A future research paper is a major objective.

### HUMAN-APPROVED DECISIONS

- Pursue SIH26139.
- Use TB CXR as the initial proof-of-work.
- Build the SIH proof-of-work before conducting the full research programme.
- Compare classical and quantum approaches.
- Preserve replaceable modules.
- Do not assume quantum advantage.
- Use the personal CXR only as a demonstration, never as scientific evidence or a personal diagnosis.
- Keep the immediate scope narrow.

### RESEARCH-BACKED FINDINGS

- Classical TB CXR detection is well established.
- Segmentation has demonstrated value in at least the supplied 2020 TB study. fileciteturn3file1
- QML medical evidence is still inconsistent/immature.
- Generic QML-for-TB is insufficient as a novelty claim.
- Cross-dataset validation, low-data evaluation, calibration, resource accounting, and trustworthy explanations are promising research directions.
- The supplied research identifies fragmentation across QML, segmentation, explanation and deployment. fileciteturn3file2
- TBX11K provides a larger TB research dataset with TB-region bounding-box annotations, while Shenzhen/Montgomery are smaller classic TB datasets. fileciteturn5file0

### ASSUMPTIONS

- Simulator-first QML is sufficient for the immediate prototype.
- Suitable segmentation inference can be obtained quickly.
- Relevant public datasets can be accessed within the project schedule.
- Modular architecture can support later disease/model changes.

### HYPOTHESES

- Anatomical grounding may improve QML behaviour.
- The effect may be strongest under low-data or domain-shift conditions.
- A low-qubit quantum model may be competitive with matched classical approaches under some conditions.

### OPEN QUESTIONS

- Exact authenticated SIH26139 detailed requirements.
- Exact final research gap.
- Final QML method.
- Best segmentation/encoder combination.
- Hardware access.
- Final dataset protocol.
- Which empirical result will become the paper's main contribution.

### DEFERRED DECISIONS

- Final paper question/title.
- Final quantum architecture.
- Neuro-symbolic extension.
- Multi-disease scope.
- Real-hardware evaluation.
- Clinical validation approach.

### OUT OF SCOPE

- Digital twin.
- IoT.
- Federated learning.
- Blockchain.
- EHR integration.
- Genomics.
- Hospital deployment.
- Autonomous diagnosis.
- Large-scale quantum architecture.
- Quanvolutional MVP.
- Unnecessary feature breadth before the core benchmark works.

### MAJOR RISKS

- QML does not outperform classical models.
- Existing work invalidates a naive novelty claim.
- Dataset limitations or leakage undermine results.
- Quantum simulation becomes computationally expensive.
- Prototype becomes over-scoped.
- Medical claims exceed the evidence.

### FINAL PROJECT POSITION

The project should be understood as:

> **A modular, research-oriented hybrid quantum-classical early-disease-detection platform, initially demonstrated through anatomy-grounded TB screening on chest X-rays, designed to experimentally test whether anatomical restriction, low-dimensional representations and hybrid QML provide measurable benefits or meaningful trade-offs against strong classical baselines.**

The SIH prototype is the **first proof-of-work**.

The eventual paper is **not predetermined**.

The research experiments determine what the paper ultimately claims.
