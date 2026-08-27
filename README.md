# SIH 2026 — SIH26139

## What is this project?
This is a research-oriented prototype for SIH26139: **Hybrid Quantum Machine Learning Platform for Early Disease Detection** (Sponsored by Egreen Quanta). The initial demonstrator is focused on Tuberculosis (TB) detection from Chest X-rays (CXR).

## Current Goal
The immediate 27–30 August target is to build a working proof-of-work with credible results, a strong architecture, and a strong SIH presentation for internal selection. The deeper research and paper publication will come after this internal-selection phase.

## Current Idea
We are investigating whether anatomically grounded, low-dimensional representations can make low-qubit hybrid QML useful under limited-data and resource constraints. 

The high-level pipeline is:
`CXR → preprocessing → lung segmentation → feature extraction → classical vs quantum ML → comparison → explanation`

**Note:** This is a hypothesis. Do NOT present quantum advantage as an established result. Do NOT present TB as necessarily the final disease scope. Do NOT present future research features as current implementation requirements.

## Team Structure
We are a 6-person AI-Native team consisting of:
* Quantum / QML
* AIML / CV
* Full Stack
* Generalist
* PPT / Story
* PPT / Visuals

## Important Rule Before You Start
**Do not immediately start writing code.** Read the repository, understand the project context, load your exact role-specific agent prompt, and strictly follow the Git workflow. Never fabricate benchmark results or claim "quantum advantage" without mathematical proof.

## Repository Structure
- `PROJECT_CONTEXT.md` - The foundational vision, scope, and technical roadmap.
- `AGENTS.md` - Core instructions for AI engineering and architecture boundaries.
- `.project/` - Contains the CI/CD planning documents, tracker, and the `team_guides/` directory.
- `.project/team_guides/` - Contains your specific role folder (e.g., `E1_Quantum_ML_Lead/`) with your Human Guide and AI Agent Prompt.
- `docs/` - Contains the 00-07 system architecture documents, engineering ledgers, and testing plans.
- `docs/reference_materials/` - Contains the PDF research papers and AI logs that form our hypothesis.
- `src/` - The source code directory (Currently empty prior to Phase 1 execution).
- `tests/` - The directory for pytest scripts and data-leakage checks (Currently empty prior to Phase 1 execution).

*(Note: Data, Models, workflows, templates, and AI skills directories are not currently defined in the repository).*

## Important Documents
Before you do anything, read these documents in this exact order:
1. `PROJECT_CONTEXT.md` (To understand the problem statement and our unique solution).
2. `AGENTS.md` (To understand the rules of AI-assisted engineering).
3. `docs/04_architecture.md` and `docs/06_interfaces.md` (To understand how the system fits together).
4. `.project/team_guides/MASTER_ONBOARDING.md` (To understand the 3-phase execution plan).
5. `.project/team_guides/<Your_Role>/<Your_Role>_HUMAN_GUIDE.md` (To understand what you are building).
6. `docs/reference_materials/` (To understand the scientific research gap before doing external research).

## Getting Started
1. Install Git and `uv` (for Python environment management).
2. Clone the repository: `git clone https://github.com/irxchand/SIH_26_Onix.git`
3. Enter the directory: `cd "SIH_26_Onix"`
4. Open the project in your IDE (Antigravity).
5. (Python environment initialization and dependencies will be handled by the DevOps Lead in Phase 1; there is no runnable code yet).

## Using Antigravity
Follow this beginner workflow:

### Step 1
Open the repository in Antigravity.
### Step 2
Let Antigravity inspect the repository.
### Step 3
Tell it to read `PROJECT_CONTEXT.md` and the relevant project documentation.
### Step 4
Ask it to produce a project understanding summary before asking it to modify anything.
### Step 5
Give it the role-specific prompt.
### Step 6
Ask it to work only within that role.
### Step 7
Review changes before committing.

Antigravity should NOT immediately start coding just because you ask a broad question.

## How to Prompt Antigravity
Give users a simple generic pattern such as:

> “First read PROJECT_CONTEXT.md, AGENTS.md, the relevant project documents and the relevant raw research material. Do not modify anything yet. Explain your understanding of the current task, assumptions, dependencies and risks. Then wait for approval.”

Each team member will then receive a more specific role prompt found in their `.project/team_guides/` folder.

## How to Work With the Existing Research
The repository already contains research material. Team members should:
- read local material first;
- use external research only to fill gaps or verify claims;
- avoid repeating generic research;
- return evidence-backed findings;
- distinguish confirmed facts, hypotheses, recommendations and open questions.

## Git Workflow
Currently, no formal branching strategy is defined in the repository. 
**Recommendation:** 
Create a branch for your role (e.g., `git checkout -b feature/quantum-ml`), commit your work frequently, and merge via Pull Request once the Integration/DevOps Lead verifies your tests pass. Do not push directly to `main`.

## What NOT To Do
* Do not create a separate project copy.
* Do not independently redesign the core architecture.
* Do not overwrite project context without approval.
* Do not fabricate benchmark results.
* Do not fabricate quantum advantage.
* Do not use personal medical data as scientific evidence.
* Do not add random features because they sound impressive.
* Do not spend hours repeating research already present in the repository.
* Do not start implementation before understanding the relevant project context.

## FAQ
* **What do I read first?** `PROJECT_CONTEXT.md` and `.project/team_guides/MASTER_ONBOARDING.md`.
* **Which AI should I use?** Antigravity IDE (Gemini/Claude).
* **How do I ask Antigravity to understand the project?** Use the generic prompt listed in "How to Prompt Antigravity".
* **What if I don't understand a document?** Ask Antigravity to explain it in simple terms based on the project context.
* **Where do I find my role?** `.project/team_guides/`.
* **Where do I find the research?** `docs/reference_materials/`.
* **Can I change the architecture?** No. Do not change the architecture without explicit approval from the team.
* **Can I create a new folder?** Stick to the repository structure defined in the Master Onboarding.
* **How do I know whether something is already solved?** Read the `.project/tracker.md` or ask the DevOps Lead.
* **Who do I ask before making a major project decision?** The human team or the `PROJECT_CONTEXT.md` source of truth.
