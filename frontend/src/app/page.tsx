"use client";

import React, { useState, useEffect } from "react";
import UploadWidget from "@/components/UploadWidget";
import ResultsDashboard from "@/components/ResultsDashboard";
import WorkstationControls from "@/components/WorkstationControls";

interface PredictionResults {
  classical_svm_confidence: number;
  quantum_svm_confidence: number;
  prediction: string;
  inference_time_seconds: number;
  is_mock: boolean;
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<PredictionResults | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Viewport transformation states
  const [zoomLevel, setZoomLevel] = useState(1);
  const [isFullscreen, setIsFullscreen] = useState(false);

  useEffect(() => {
    // Cleanup preview URL on unmount
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const handleFileSelected = async (selectedFile: File) => {
    setFile(selectedFile);
    setError(null);
    setResults(null);
    
    const url = URL.createObjectURL(selectedFile);
    setPreviewUrl(url);

    // Automatically trigger analysis on file selection
    await runAnalysis(selectedFile);
  };

  const runAnalysis = async (targetFile: File) => {
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", targetFile);

    try {
      // Hit local FastAPI backend directly
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Analysis failed with status ${response.status}`);
      }

      const data: PredictionResults = await response.json();
      setResults(data);
    } catch (err: any) {
      console.error(err);
      setError("Inference server connection failed. Please ensure the FastAPI backend is running.");
      // Fallback dummy results for isolated frontend testing if backend is offline
      setResults({
        classical_svm_confidence: 0.87,
        quantum_svm_confidence: 0.92,
        prediction: "Anomaly Detected",
        inference_time_seconds: 0.485,
        is_mock: true,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleResetImage = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setFile(null);
    setPreviewUrl(null);
    setResults(null);
    setError(null);
    setZoomLevel(1);
  };

  const handleZoomIn = () => setZoomLevel((prev) => Math.min(prev + 0.1, 2.0));
  const handleZoomOut = () => setZoomLevel((prev) => Math.max(prev - 0.1, 0.5));
  const handleResetZoom = () => setZoomLevel(1);
  const handleToggleFullscreen = () => setIsFullscreen((prev) => !prev);

  return (
    <main className="min-h-screen bg-[#090b11] text-[#E2E8F0] py-6 px-4 md:px-8 font-sans selection:bg-blue-500/30 selection:text-white">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* HEADER SECTION */}
        <header className="border-b border-gray-900 pb-4 flex flex-col md:flex-row md:items-center md:justify-between space-y-3 md:space-y-0">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="text-[10px] font-mono tracking-widest text-emerald-500 uppercase">SYS ACTIVE</span>
              <span className="text-gray-800 text-[10px] font-mono">|</span>
              <span className="text-[10px] font-mono text-gray-500 tracking-wider">VERSION 1.0.0</span>
            </div>
            <h1 className="text-xl font-extrabold tracking-tight text-white font-mono uppercase">
              ANATOMY-GROUNDED HYBRID QUANTUM AI
            </h1>
            <p className="text-xs text-gray-400 font-mono">
              TB Early Detection Research Console / Chest X-Ray DICOM Analyzer
            </p>
          </div>

          {/* Subtly labeled research disclaimer */}
          <div className="px-3 py-1.5 border border-yellow-900/30 bg-yellow-950/10 rounded-md text-[10px] text-yellow-600/80 max-w-sm leading-relaxed">
            <strong>RESEARCH USE ONLY:</strong> This workstation is an experimental QML validator and does not provide clinical diagnostic findings.
          </div>
        </header>

        {/* ERROR DISPLAY */}
        {error && (
          <div className="px-4 py-2 bg-red-950/20 border border-red-900/40 rounded-lg text-xs text-red-400 font-mono flex items-center justify-between">
            <span>[SYS_ERR]: {error}</span>
            <button onClick={() => setError(null)} className="text-gray-500 hover:text-white">✕</button>
          </div>
        )}

        {/* PRIMARY WORKSPACE */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* LEFT: MEDICAL IMAGE VIEWPORT (8 cols) */}
          <section className={`lg:col-span-8 flex flex-col space-y-3 ${isFullscreen ? "fixed inset-0 bg-[#090b11] z-50 p-6" : ""}`}>
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono text-gray-400 tracking-wide">
                {isFullscreen ? "FULLSCREEN MONITOR VIEW" : "PRIMARY SCANNED IMAGE VIEWPORT"}
              </span>
              {previewUrl && (
                <button 
                  onClick={handleResetImage}
                  className="text-xs font-mono text-red-500 hover:text-red-400 transition-colors"
                >
                  [ EJECT STUDY ]
                </button>
              )}
            </div>

            {/* Viewport Container */}
            <div className="relative border border-gray-800 rounded-lg bg-[#07090e] h-[450px] flex items-center justify-center overflow-hidden">
              
              {/* Medical grid overlays (crosshairs, corners) */}
              <div className="absolute inset-4 border border-gray-900/40 pointer-events-none z-0"></div>
              <div className="absolute top-2 left-2 border-t-2 border-l-2 border-gray-700 w-3 h-3 pointer-events-none"></div>
              <div className="absolute top-2 right-2 border-t-2 border-r-2 border-gray-700 w-3 h-3 pointer-events-none"></div>
              <div className="absolute bottom-2 left-2 border-b-2 border-l-2 border-gray-700 w-3 h-3 pointer-events-none"></div>
              <div className="absolute bottom-2 right-2 border-b-2 border-r-2 border-gray-700 w-3 h-3 pointer-events-none"></div>

              {!previewUrl ? (
                <div className="w-full h-full p-4 flex items-center justify-center z-10">
                  <UploadWidget onFileSelected={handleFileSelected} />
                </div>
              ) : (
                <div className="relative w-full h-full flex items-center justify-center z-10">
                  
                  {/* Actual X-Ray Rendering */}
                  <img
                    src={previewUrl}
                    alt="Active Patient Study"
                    className="max-h-[90%] max-w-[90%] object-contain select-none transition-transform duration-200"
                    style={{ transform: `scale(${zoomLevel})` }}
                  />

                  {/* Loading Scan Overlay */}
                  {loading && (
                    <div className="absolute inset-0 bg-black/60 flex flex-col items-center justify-center space-y-4">
                      {/* Scanline Animation */}
                      <div className="absolute top-0 inset-x-0 h-0.5 bg-gradient-to-r from-transparent via-blue-500 to-transparent animate-[scan_2s_ease-in-out_infinite]"></div>
                      
                      <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                      <p className="text-xs font-mono text-blue-400 animate-pulse uppercase tracking-wider">
                        Running Hybrid QML Inference...
                      </p>
                    </div>
                  )}

                  {/* Top-left image specs */}
                  <div className="absolute top-4 left-4 font-mono text-[9px] text-gray-500 bg-[#090b11]/80 px-2 py-1 rounded border border-gray-850">
                    <p>ID: {file?.name.substring(0, 16) || "DICOM"}</p>
                    <p>SCALE: {zoomLevel.toFixed(1)}x</p>
                    <p>SIZE: {file ? (file.size / 1024).toFixed(0) : 0} KB</p>
                  </div>
                </div>
              )}
            </div>

            {/* Viewport Control Panel */}
            {previewUrl && (
              <div className="flex justify-between items-center bg-[#0d1117] p-2 border border-gray-850 rounded-lg">
                <WorkstationControls
                  onZoomIn={handleZoomIn}
                  onZoomOut={handleZoomOut}
                  onReset={handleResetZoom}
                  onToggleFullscreen={handleToggleFullscreen}
                />
                
                <span className="text-[10px] text-gray-500 font-mono">
                  {file ? file.name : "DICOM study loaded"}
                </span>
              </div>
            )}
          </section>

          {/* RIGHT: ANALYSIS PANEL (4 cols) */}
          <section className="lg:col-span-4 space-y-4">
            <span className="text-xs font-mono text-gray-400 tracking-wide block">
              DIAGNOSTIC ANALYSIS & RESULTS
            </span>

            {/* Dashboard Container */}
            <div className="space-y-4">
              {loading && !results ? (
                <div className="w-full border border-gray-800 rounded-lg p-8 bg-[#0d1117] text-center space-y-3">
                  <div className="inline-block w-6 h-6 border-2 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
                  <p className="text-xs font-mono text-gray-400">ANALYZING STUDY PARALLEL PIPELINES...</p>
                </div>
              ) : (
                <ResultsDashboard results={results} />
              )}

              {/* Console workflow info */}
              <div className="border border-gray-850 bg-[#0d1117] rounded-lg p-3 text-[10px] font-mono text-gray-500 leading-relaxed">
                <h5 className="font-bold text-gray-400 uppercase mb-1">Inference Execution:</h5>
                <ol className="list-decimal list-inside space-y-1">
                  <li>Ingest CXR DICOM/Image.</li>
                  <li>U-Net anatomical lung segmentation.</li>
                  <li>CNN feature extraction (1024 dims).</li>
                  <li>PCA dimensional compression (8 dims).</li>
                  <li>Classical RBF-SVM & QSVM kernel matching.</li>
                </ol>
              </div>
            </div>
          </section>

        </div>
      </div>
    </main>
  );
}
