# 🧑‍💻 E3 - Frontend Engineer (Deep Execution & Validation Guide)

## 1. Core Philosophy & Role Definition
As the Frontend Engineer, you are responsible for the entire user experience. You must translate the raw JSON outputs of E1 and E2 into a medical-grade, premium UI that will wow the SIH hackathon judges. 

**The inherent problem you are solving:** Quantum computing concepts are extremely abstract. If you just display a number saying "QSVM Confidence: 85%", the judges will not be impressed. You must visually prove the value of the prototype through dynamic comparisons (Classical vs Quantum charts) and visual interpretability (overlaying Grad-CAM heatmaps onto the X-Rays).

Your AI Agent is highly capable of scaffolding React, but it often defaults to bland, generic Tailwind styles or forgets to handle asynchronous loading states smoothly. You must provide strict aesthetic direction.

---

## 2. Phase 1: Static UI Shell Validation

### The Objective
Establish the Next.js foundation, enforce type-safety with the backend's API schema, and build the drag-and-drop upload widget.

### What to Manually Check & Validate
1. **Responsiveness & Feel:** 
   - *Detail Check:* Run the app (`npm run dev`). Drag a file over the `UploadWidget`. Does the border highlight smoothly? If the agent used basic HTML file inputs without `framer-motion` states, it will feel cheap. 
   - *Action:* Instruct the agent to add `framer-motion` variants (e.g., `whileHover`, `whileTap`) to the dropzone.
2. **Type Safety:**
   - *Detail Check:* Open `src/types/index.ts`. Compare it line-by-line with the backend `PredictionResponse` schema. If the agent hallucinated fields like `patient_name` (which we aren't tracking), delete them. The types must match the API exactly.

### Agent Prompts (Phase 1)
**Initialization Prompt:**
> "Agent, I am E3, the Frontend Engineer. Load your system directives from `E3_Frontend_Engineer_AGENT_PROMPT.md`. We are executing Phase 1. Scaffold the Next.js app with Tailwind and Framer Motion. Define the exact TypeScript interfaces for the API. Build the `UploadWidget` component with a highly polished drag-and-drop experience. Do not proceed to Phase 2 until I review the UI."

**Correction Prompt (If UI looks generic):**
> "The UI looks like a standard Bootstrap template. I need a premium, medical-grade aesthetic. Switch the color palette to deep slate blues (e.g., `bg-slate-900`) with glassmorphism effects (`backdrop-blur`, `bg-white/10`) for the upload widget cards. Make the borders subtle and rounded."

---

## 3. Phase 2: Dynamic Charts & State Validation

### The Objective
Build the results dashboard using mock data, proving out the chart libraries before the backend is finished.

### What to Manually Check & Validate
1. **Chart Aesthetics:**
   - *Detail Check:* The agent will use `recharts` to build a `BarChart` comparing Classical vs Quantum confidence. 
   - *Validation:* If the bars are flat and have no tooltips, the data is unreadable. Ensure the agent configures `<Tooltip />`, `<Legend />`, and uses distinct, premium colors (e.g., Classical = Gray/Blue, Quantum = Vibrant Cyan/Purple).
2. **Loading States:**
   - *Detail Check:* Look at `src/app/page.tsx`. There must be a clear transition state when `isPending` is true. If the screen just freezes after upload, the user experience is broken.

### Agent Prompts (Phase 2)
**Execution Prompt:**
> "Agent, proceed to Phase 2. Build `MetricsDashboard.tsx` using `recharts`. Create a visually striking BarChart comparing SVM vs QSVM confidence. Use vibrant colors for the Quantum metrics to make them stand out. Implement the state logic in `page.tsx` with a premium `framer-motion` loading spinner that displays while waiting for the fake data."

---

## 4. Phase 3: API Integration & Polish Validation

### The Objective
Connect the frontend `fetch` request to E2's FastAPI server, handle the multipart form upload, and overlay the resulting Grad-CAM heatmap over the base image.

### What to Manually Check & Validate
1. **Network Integration:**
   - *Detail Check:* Open the browser network tab. When you upload a file, it must send a `multipart/form-data` request to `http://localhost:8000/api/v1/predict`. If the agent tried to send JSON, the FastAPI server will crash.
2. **Heatmap CSS Overlay:**
   - *Detail Check:* The backend returns URLs for `segmentation_mask_url` and `gradcam_heatmap_url`. The agent must render the original image, and position the heatmap image exactly over it.
   - *Validation:* Inspect the CSS. The parent container must be `relative`. The heatmap image must be `absolute inset-0`, with `opacity-50` and `mix-blend-multiply` (or similar) so the underlying bone structure is still visible beneath the heat.

### Agent Prompts (Phase 3)
**Execution Prompt:**
> "Agent, proceed to Phase 3. Write `src/lib/api.ts` to `fetch` the FastAPI backend using `FormData`. Wire this into the upload widget. Create `HeatmapViewer.tsx` that absolutely positions the `gradcam_heatmap_url` over the base X-Ray image with `opacity-60` and `mix-blend-overlay` so the doctor can see both the heat and the bone structure. Add smooth page transitions."
