# Project Agent Instructions

1. **Experimental Integrity:** Do not hallucinate quantum advantage. Compare QSVM and SVM fairly using the identical PCA-reduced feature set.
2. **Architecture Boundaries:** The Next.js frontend handles UI only. The FastAPI backend handles all ML/QML logic. Do not mix dependencies.
3. **Frontend Autonomy:** Agents working on Next.js have full authority over aesthetics, color palettes, and component design, provided they strictly consume the REST API contract.
4. **Backend Strictness:** Agents working on FastAPI must write pure, testable functions for the pipeline. State is global and loaded at startup.
5. **Data Leakage:** Ensure strict separation of training and testing data before fitting PCA.
6. **Resource Tracking:** Track and return quantum simulation resource costs (qubits, circuit depth, runtime) via the API payload.
