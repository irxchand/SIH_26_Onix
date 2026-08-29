"use client";

import React, { useState, useEffect, useCallback } from "react";
import LeftToolRail from "@/components/LeftToolRail";
import XrayCanvas from "@/components/XrayCanvas";
import RightIntelligence from "@/components/RightIntelligence";
import QuantumCircuitView from "@/components/QuantumCircuitView";
import RadiologyQueue from "@/components/RadiologyQueue";
import { Study, ToolMode, PredictionResults, EvidenceItem, ChecklistStep } from "../types/workstation";
import { mockPredictions, mockEvidence } from "../mock/studies";

const API_BASE = "http://localhost:8000";

const PIPELINE_STAGES = [
  "IMAGE INGESTION",
  "ANATOMICAL SEGMENTATION",
  "FEATURE EXTRACTION",
  "PCA COMPRESSION",
  "CLASSICAL INFERENCE",
  "QUANTUM ENCODING",
  "QSVM KERNEL EVALUATION",
  "CONSENSUS CONVERGENCE"
];

export default function Home() {
  const [selectedStudy, setSelectedStudy] = useState<Study | null>(null);
  const [activeMode, setActiveMode] = useState<ToolMode>("SCAN");
  const [brightness, setBrightness] = useState(100);
  const [contrast, setContrast] = useState(100);
  const [sharpness, setSharpness] = useState(100);

  // Debounce calibration saves
  useEffect(() => {
    if (!selectedStudy) return;
    const timer = setTimeout(() => {
      fetch(`${API_BASE}/api/v1/studies/${selectedStudy.id}/calibrate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ brightness, contrast, sharpness })
      }).catch(console.error);
    }, 500);
    return () => clearTimeout(timer);
  }, [brightness, contrast, sharpness, selectedStudy]);

  // Viewport transforms
  const [zoomLevel, setZoomLevel] = useState(1);
  const [isFullscreen, setIsFullscreen] = useState(false);

  // Analysis states
  const [loading, setLoading] = useState(false);
  const [activeStageIdx, setActiveStageIdx] = useState(-1);
  const [results, setResults] = useState<PredictionResults | null>(null);
  const [evidence, setEvidence] = useState<EvidenceItem[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Switch between patient list queue and workspace console
  const [viewMode, setViewMode] = useState<"QUEUE" | "WORKSPACE">("QUEUE");

  // Custom study uploads
  const [studies, setStudies] = useState<Study[]>([]);
  const [queueLoading, setQueueLoading] = useState(true);

  // Fetch studies from backend on mount
  const fetchQueue = useCallback(async () => {
    setQueueLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/queue`);
      if (!res.ok) throw new Error(`Queue fetch failed: ${res.status}`);
      const data = await res.json();
      setStudies(data.studies);
    } catch (err) {
      console.error("Failed to fetch queue:", err);
      // Fallback: leave studies empty, user sees empty state
    } finally {
      setQueueLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchQueue();
  }, [fetchQueue]);

  // Checklist state
  const [pixelSpacingMm, setPixelSpacingMm] = useState<number>(0.143);
  const [imageWidth, setImageWidth] = useState<number>(2048);
  const [imageHeight, setImageHeight] = useState<number>(2048);
  const [checklist, setChecklist] = useState<ChecklistStep[]>([
    { id: "spine_top", label: "Highest point of the spine", status: "pending" },
    { id: "spine_bottom", label: "Lowest point of the spine", status: "pending" },
    { id: "heart_right", label: "Right side of the heart at its widest point", status: "pending" },
    { id: "heart_left", label: "Left side of the heart at its widest point", status: "pending" },
    { id: "chest_right", label: "Right side of the chest at its widest point", status: "pending" },
    { id: "chest_left", label: "Left side of the chest at its widest point", status: "pending" }
  ]);

  const handleChecklistUpdate = (updatedChecklist: ChecklistStep[]) => {
    setChecklist(updatedChecklist);
  };

  const handleSelectStudy = async (study: Study) => {
    setSelectedStudy(study);
    setViewMode("WORKSPACE");
    
    // Fetch pixel spacing metadata
    try {
      const res = await fetch(`${API_BASE}/api/v1/studies/${study.id}/metadata`);
      if (res.ok) {
        const meta = await res.json();
        setPixelSpacingMm(meta.pixelSpacingMm || 0.143);
        if (meta.width) setImageWidth(meta.width);
        if (meta.height) setImageHeight(meta.height);
      }
    } catch(err) {
      console.error(err);
      setPixelSpacingMm(0.143);
      setImageWidth(2048);
      setImageHeight(2048);
    }
    
    // Reset controls
    setBrightness(100);
    setContrast(100);
    setSharpness(100);
    setZoomLevel(1);
    setResults(null);
    setEvidence([]);
    setError(null);
    
    // Reset checklist
    setChecklist(checklist.map(item => ({ ...item, status: "pending", point: undefined })));
    
    // Trigger analysis automatically
    triggerWorkflow(study);
  };

  const triggerWorkflow = (study: Study) => {
    setLoading(true);
    setResults(null);
    setEvidence([]);
    setActiveStageIdx(0);
  };

  // Run the progressive pipeline animation steps
  useEffect(() => {
    if (!loading || activeStageIdx === -1) return;

    if (activeStageIdx < PIPELINE_STAGES.length) {
      const duration = activeStageIdx === 6 ? 1200 : 400; // Let QSVM step take slightly longer for visual impact
      const timer = setTimeout(() => {
        setActiveStageIdx((prev) => prev + 1);
      }, duration);
      return () => clearTimeout(timer);
    } else {
      // Pipeline complete: Fetch live results from backend
      const fetchResults = async () => {
        if (!selectedStudy) return;
        try {
          const res = await fetch(`${API_BASE}/api/v1/studies/${selectedStudy.id}/predict`);
          if (!res.ok) throw new Error("Prediction failed");
          const data = await res.json();
          setResults(data);
          setEvidence(data.evidence || []);
        } catch (err) {
          console.error(err);
          // Fallback if backend is down
          setResults(mockPredictions[selectedStudy.id] || {
            classical_svm_confidence: 0.87,
            quantum_svm_confidence: 0.92,
            prediction: "Anomaly Detected",
            inference_time_seconds: 0.485,
            is_mock: true,
            qubits: 8,
            circuit_depth: 24,
            runtime: 0.485
          });
          setEvidence(mockEvidence[selectedStudy.id] || []);
        } finally {
          setLoading(false);
          setActiveStageIdx(-1);
        }
      };
      
      fetchResults();
    }
  }, [loading, activeStageIdx, selectedStudy]);

  const handleCustomUpload = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_BASE}/api/v1/upload`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({ detail: "Upload failed" }));
        setError(errData.detail || "Upload failed");
        return;
      }

      // Refresh the queue to include the new study
      await fetchQueue();

      // Select the newly uploaded study
      const uploadData = await res.json().catch(() => null);
      if (uploadData?.studyId) {
        const newStudy = studies.find(s => s.id === uploadData.studyId);
        if (newStudy) handleSelectStudy(newStudy);
      }
    } catch (err) {
      console.error("Upload error:", err);
      setError("Failed to upload image. Is the backend running?");
    }
  };

  const handleResetWorkspace = () => {
    setSelectedStudy(null);
    setResults(null);
    setEvidence([]);
    setViewMode("QUEUE");
  };

  const handleZoomIn = () => setZoomLevel((prev) => Math.min(prev + 0.1, 2.0));
  const handleZoomOut = () => setZoomLevel((prev) => Math.max(prev - 0.1, 0.5));
  const handleResetZoom = () => setZoomLevel(1);
  const handleToggleFullscreen = () => setIsFullscreen((prev) => !prev);


  return (
    <main className="min-h-screen bg-[#07090d] text-[#e2e8f0] py-4 px-4 md:px-6 font-sans">
      <div className="max-w-7xl mx-auto space-y-4">
        
        {/* HEADER BAR */}
        <header className="border-b border-gray-800 pb-3 flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-2 sm:space-y-0">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="text-[9px] font-mono tracking-widest text-emerald-400">SYS READY</span>
              <span className="text-gray-800">|</span>
              <span className="text-[9px] font-mono text-gray-500">SIH26139 WORKSTATION v1.2</span>
            </div>
            <h1 className="text-lg font-bold tracking-tight text-white font-mono uppercase">
              ANATOMY // INTELLIGENCE
            </h1>
            <p className="text-[10px] text-gray-400 font-mono">
              Chest X-Ray Anatomy-Grounded Hybrid Quantum Analysis Console
            </p>
          </div>

          <div className="flex items-center space-x-3">
            {viewMode === "WORKSPACE" && (
              <button
                onClick={handleResetWorkspace}
                className="px-2.5 py-1 bg-gray-900 border border-gray-800 hover:bg-gray-800 text-[10px] font-mono text-gray-400 rounded transition-colors"
              >
                [ VIEW ALL STUDIES ]
              </button>
            )}
            
            <div className="px-3 py-1 border border-yellow-950 bg-yellow-950/10 rounded text-[9px] text-yellow-600 max-w-xs leading-tight">
              <strong>EVALUATION PROTOCOL:</strong> Experimental QML interface. Not for clinical diagnostic use.
            </div>
          </div>
        </header>

        {/* WORKSPACE LAYOUT CONTAINER */}
        {viewMode === "QUEUE" ? (
          <div className="space-y-4">
            {/* Custom Scan Importer Box */}
            <div className="border border-gray-800 bg-[#0d1117] rounded-lg p-4 flex items-center justify-between">
              <div>
                <h4 className="text-xs font-bold text-white font-mono">DEMONSTRATION SCAN INGESTION</h4>
                <p className="text-[10px] text-gray-500 mt-1">Upload a JPEG/PNG chest X-ray image to start a live analysis session.</p>
              </div>
              <div className="relative">
                <input
                  type="file"
                  onChange={(e) => e.target.files && handleCustomUpload(e.target.files[0])}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  accept="image/jpeg, image/png"
                />
                <button className="px-3 py-1.5 bg-blue-950/40 hover:bg-blue-900/60 border border-blue-900/50 text-blue-400 text-[10px] font-mono font-bold rounded">
                  + IMPORT NEW SCAN
                </button>
              </div>
            </div>

            {/* Radiology Queue Table */}
            <RadiologyQueue studies={studies} onSelectStudy={handleSelectStudy} />
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 items-start">
            
            {/* LEFT COLUMN: TOOLS (2 cols) */}
            <div className="lg:col-span-2">
              <LeftToolRail
                activeMode={activeMode}
                onModeChange={setActiveMode}
                brightness={brightness}
                onBrightnessChange={setBrightness}
                contrast={contrast}
                onContrastChange={setContrast}
                sharpness={sharpness}
                onSharpnessChange={setSharpness}
              />
            </div>

            {/* CENTER COLUMN: VIEWPORT CANVAS (7 cols) */}
            <div className="lg:col-span-7 space-y-3">
              <XrayCanvas
                study={selectedStudy}
                activeMode={activeMode}
                pixelSpacingMm={pixelSpacingMm}
                brightness={brightness}
                contrast={contrast}
                sharpness={sharpness}
                evidence={evidence}
                zoomLevel={zoomLevel}
                onZoomIn={handleZoomIn}
                onZoomOut={handleZoomOut}
                onReset={handleResetZoom}
                onToggleFullscreen={handleToggleFullscreen}
                checklist={checklist}
                onChecklistUpdate={handleChecklistUpdate}
                imageWidth={imageWidth}
                imageHeight={imageHeight}
              />

              {/* Patient Record Card */}
              {selectedStudy && (
                <div className="bg-[#0d1117] border border-gray-800 rounded-lg p-3 text-[10px] font-mono grid grid-cols-4 gap-4 text-gray-400">
                  <div>
                    <span className="text-gray-500 block">PATIENT ID</span>
                    <span className="text-white">{selectedStudy.patientId}</span>
                  </div>
                  <div>
                    <span className="text-gray-500 block">PATIENT NAME</span>
                    <span className="text-white">{selectedStudy.patientName}</span>
                  </div>
                  <div>
                    <span className="text-gray-500 block">AGE / SEX</span>
                    <span className="text-white">{selectedStudy.age}Y / {selectedStudy.sex}</span>
                  </div>
                  <div>
                    <span className="text-gray-500 block">ACQUISITION TIME</span>
                    <span className="text-white">{selectedStudy.acquisitionDate}</span>
                  </div>
                </div>
              )}
            </div>

            {/* RIGHT COLUMN: INTELLIGENCE & CIRCUITS (3 cols) */}
            <div className="lg:col-span-3 space-y-4">
              {/* Pipeline Loading Screen or Right Intelligence results */}
              {loading ? (
                <div className="border border-gray-800 rounded-lg p-4 bg-[#0d1117] space-y-4 font-mono">
                  <span className="text-[10px] text-gray-500 tracking-wider block">EXECUTION PIPELINE</span>
                  <div className="space-y-2">
                    {PIPELINE_STAGES.map((stage, idx) => {
                      const isComplete = idx < activeStageIdx;
                      const isProcessing = idx === activeStageIdx;
                      return (
                        <div key={stage} className="flex items-center justify-between text-[9px] py-1 border-b border-gray-850/30">
                          <span className={isProcessing ? "text-blue-400 font-bold" : isComplete ? "text-gray-500" : "text-gray-700"}>
                            {stage}
                          </span>
                          <span className="text-[9px]">
                            {isComplete && <span className="text-green-500">✓ COMPLETE</span>}
                            {isProcessing && <span className="text-blue-400 animate-pulse">● RUNNING</span>}
                            {!isComplete && !isProcessing && <span className="text-gray-700">○ QUEUED</span>}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ) : (
                <>
                  <RightIntelligence 
                    study={selectedStudy}
                    results={results} 
                    loading={loading} 
                    checklist={checklist}
                    onAccept={async () => {
                      if (!selectedStudy) return;
                      await fetch(`${API_BASE}/api/v1/studies/${selectedStudy.id}/status`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({status: 'ACCEPTED'})
                      });
                      alert("Study Accepted");
                    }}
                    onReject={async () => {
                      if (!selectedStudy) return;
                      await fetch(`${API_BASE}/api/v1/studies/${selectedStudy.id}/status`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({status: 'REJECTED'})
                      });
                      alert("Study Rejected");
                    }}
                  />
                  
                  {/* Quantum circuit board visualization */}
                  <QuantumCircuitView isAnimating={activeStageIdx >= 5 || loading} />
                </>
              )}
            </div>

          </div>
        )}

      </div>
    </main>
  );
}
