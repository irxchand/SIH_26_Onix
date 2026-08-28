import { Study, PredictionResults, EvidenceItem } from "../types/workstation";

export const mockStudies: Study[] = [
  {
    id: "XR-2026-00421",
    patientId: "PT-8802",
    patientName: "John Doe",
    age: 42,
    sex: "M",
    modality: "CHEST X-RAY (PA)",
    acquisitionDate: "29 AUG 2026 04:12",
    status: "READY",
    imageUrl: "/mock_xray_normal.jpg", // Users can test upload or select from these
  },
  {
    id: "XR-2026-00512",
    patientId: "PT-9410",
    patientName: "Alice Smith",
    age: 38,
    sex: "F",
    modality: "CHEST X-RAY (PA)",
    acquisitionDate: "29 AUG 2026 03:30",
    status: "COMPLETE",
    imageUrl: "/mock_xray_anomaly.jpg",
  },
  {
    id: "XR-2026-00513",
    patientId: "PT-2091",
    patientName: "Robert Johnson",
    age: 55,
    sex: "M",
    modality: "CHEST X-RAY (AP)",
    acquisitionDate: "29 AUG 2026 02:15",
    status: "REVIEW",
    imageUrl: "/mock_xray_anomaly2.jpg",
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
  }
];

export const mockPredictions: Record<string, PredictionResults> = {
  "XR-2026-00421": {
    classical_svm_confidence: 0.12,
    quantum_svm_confidence: 0.08,
    prediction: "Healthy",
    inference_time_seconds: 0.380,
    is_mock: true,
  },
  "XR-2026-00512": {
    classical_svm_confidence: 0.87,
    quantum_svm_confidence: 0.92,
    prediction: "Anomaly Detected",
    inference_time_seconds: 0.485,
    is_mock: true,
  },
  "XR-2026-00513": {
    classical_svm_confidence: 0.74,
    quantum_svm_confidence: 0.79,
    prediction: "Anomaly Detected",
    inference_time_seconds: 0.521,
    is_mock: true,
  },
  "XR-2026-00514": {
    classical_svm_confidence: 0.09,
    quantum_svm_confidence: 0.05,
    prediction: "Healthy",
    inference_time_seconds: 0.315,
    is_mock: true,
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
