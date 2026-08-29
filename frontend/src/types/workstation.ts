export interface Study {
  id: string;
  patientId: string;
  patientName: string;
  age: number;
  sex: "M" | "F";
  modality: string;
  acquisitionDate: string;
  status: "READY" | "ANALYZING" | "COMPLETE" | "REVIEW";
  imageUrl: string;
  examDesc?: string;
  issuesCount?: number;
  birads?: string;
  referringPhysician?: string;
  history?: string;
  comments?: string;
  attending?: string;
}

export type ToolMode = "SCAN" | "MEASURE" | "ANNOTATE" | "SEGMENT" | "EVIDENCE" | "QUANTUM" | "IMAGE";

export interface PipelineStage {
  id: string;
  name: string;
  status: "QUEUED" | "PROCESSING" | "COMPLETE";
}

export interface AnatomicalRegion {
  name: string;
  path: string; // SVG path command for rendering overlays
  confidence: number;
}

export interface MeasurementPoint {
  x: number;
  y: number;
}

export interface Measurement {
  p1: MeasurementPoint;
  p2: MeasurementPoint;
  distancePx: number;
}

export type ChecklistStatus = "pending" | "completed";

export interface ChecklistStep {
  id: string;
  label: string;
  status: ChecklistStatus;
  point?: MeasurementPoint;
}

export interface IssueAnnotation {
  id: string;
  xPercent: number;
  yPercent: number;
  measurementStr: string;
  classification: string;
  note: string;
}

export interface EvidenceItem {
  id: string;
  region: string;
  confidence: number;
  signal: string;
  xPercent: number; // For anchored positioning
  yPercent: number;
}

export interface PredictionResults {
  classical_svm_confidence: number;
  quantum_svm_confidence: number;
  prediction: string;
  inference_time_seconds: number;
  is_mock: boolean;
}
