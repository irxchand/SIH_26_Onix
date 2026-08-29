import { Study, PredictionResults, EvidenceItem } from "../types/workstation";

export const mockStudies: Study[] = [
  {
    id: "XR-2026-00421",
    patientId: "PT-8802",
    patientName: "Mariam Holden",
    age: 55,
    sex: "F",
    modality: "CHEST X-RAY (PA)",
    acquisitionDate: "29 AUG 2026 04:12",
    status: "READY",
    imageUrl: "/mock_xray_normal.jpg",
    examDesc: "Chest X-ray",
    issuesCount: 2,
    birads: "2",
    referringPhysician: "BORGES, Emilio",
    history: "Heart attack, stroke on left side of brain",
    comments: "Patient frequently complains of headaches, nausea, chest pains",
    attending: "BORGES, Emilio",
  },
  {
    id: "XR-2026-00512",
    patientId: "PT-9410",
    patientName: "Emmanuel Mack",
    age: 62,
    sex: "M",
    modality: "CHEST X-RAY (PA)",
    acquisitionDate: "29 AUG 2026 03:30",
    status: "COMPLETE",
    imageUrl: "/mock_xray_anomaly.jpg",
    examDesc: "Abdominal X-ray",
    issuesCount: 0,
    birads: "1",
    referringPhysician: "SMITH, John",
    history: "None",
    comments: "Routine checkup",
    attending: "SMITH, John",
  },
  {
    id: "XR-2026-00513",
    patientId: "PT-2091",
    patientName: "Ricardo Horton",
    age: 48,
    sex: "M",
    modality: "CHEST X-RAY (AP)",
    acquisitionDate: "29 AUG 2026 02:15",
    status: "REVIEW",
    imageUrl: "/mock_xray_anomaly2.jpg",
    examDesc: "Venography",
    issuesCount: 1,
    birads: "3",
    referringPhysician: "DAVIS, Alan",
    history: "High blood pressure",
    comments: "Patient reports dizziness",
    attending: "DAVIS, Alan",
  },
  {
    id: "XR-2026-00514",
    patientId: "PT-1102",
    patientName: "Sarah Davis",
    age: 29,
    sex: "F",
    modality: "CHEST X-RAY (PA)",
    acquisitionDate: "28 AUG 2026 19:40",
    status: "READY",
    imageUrl: "/mock_xray_normal2.jpg",
    examDesc: "Chest X-ray",
    issuesCount: 0,
    birads: "1",
    referringPhysician: "RODRIGUEZ, Maria",
    history: "None",
    comments: "No significant findings",
    attending: "RODRIGUEZ, Maria",
  }
];

export const mockPredictions: Record<string, PredictionResults> = {
  "XR-2026-00421": {
    classical_svm_confidence: 0.82,
    quantum_svm_confidence: 0.89,
    prediction: "Healthy",
    inference_time_seconds: 0.485,
    is_mock: true,
    qubits: 8,
    circuit_depth: 24,
    runtime: 0.485,
    image_width: 1200,
    image_height: 896
  },
  "XR-2026-00512": {
    classical_svm_confidence: 0.94,
    quantum_svm_confidence: 0.97,
    prediction: "Anomaly Detected",
    inference_time_seconds: 0.512,
    is_mock: true,
    qubits: 8,
    circuit_depth: 24,
    runtime: 0.512,
    image_width: 1200,
    image_height: 896
  },
  "XR-2026-00513": {
    classical_svm_confidence: 0.78,
    quantum_svm_confidence: 0.85,
    prediction: "Anomaly Detected",
    inference_time_seconds: 0.420,
    is_mock: true,
    qubits: 8,
    circuit_depth: 24,
    runtime: 0.420,
    image_width: 1200,
    image_height: 896
  },
  "XR-2026-00514": {
    classical_svm_confidence: 0.96,
    quantum_svm_confidence: 0.98,
    prediction: "Healthy",
    inference_time_seconds: 0.455,
    is_mock: true,
    qubits: 8,
    circuit_depth: 24,
    runtime: 0.455,
    image_width: 1200,
    image_height: 896
  }
};

export const mockEvidence: Record<string, EvidenceItem[]> = {
  "XR-2026-00512": [
    {
      id: "E-01",
      region: "RIGHT LOWER LUNG LOBE",
      confidence: 0.87,
      signal: "Abnormal density/feature pattern detected in right lower zone",
      xPercent: 38,
      yPercent: 68,
    }
  ],
  "XR-2026-00513": [
    {
      id: "E-02",
      region: "LEFT HILAR REGION",
      confidence: 0.79,
      signal: "Opacification / localized density anomaly surrounding left hilar root",
      xPercent: 62,
      yPercent: 48,
    }
  ]
};
