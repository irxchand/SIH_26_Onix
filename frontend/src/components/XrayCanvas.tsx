"use client";

import React, { useState, useRef, useEffect } from "react";
import { ToolMode, MeasurementPoint, EvidenceItem, Study } from "../types/workstation";

interface XrayCanvasProps {
  study: Study | null;
  activeMode: ToolMode;
  brightness: number;
  contrast: number;
  sharpness: number;
  evidence: EvidenceItem[];
  zoomLevel: number;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onReset: () => void;
  onToggleFullscreen: () => void;
}

export default function XrayCanvas({
  study,
  activeMode,
  brightness,
  contrast,
  sharpness,
  evidence,
  zoomLevel,
  onZoomIn,
  onZoomOut,
  onReset,
  onToggleFullscreen,
}: XrayCanvasProps) {
  const [points, setPoints] = useState<MeasurementPoint[]>([]);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [notes, setNotes] = useState<Record<string, string>>({});
  const [activeNote, setActiveNote] = useState<string | null>(null);

  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Reset measurements when study changes or mode changes
    setPoints([]);
  }, [study, activeMode]);

  const handleCanvasClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (activeMode !== "MEASURE" || !containerRef.current) return;

    const rect = containerRef.current.getBoundingClientRect();
    const x = Math.round(((e.clientX - rect.left) / rect.width) * 100);
    const y = Math.round(((e.clientY - rect.top) / rect.height) * 100);

    if (points.length < 4) {
      setPoints([...points, { x, y }]);
    }
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = Math.round(((e.clientX - rect.left) / rect.width) * 100);
    const y = Math.round(((e.clientY - rect.top) / rect.height) * 100);
    setMousePos({ x, y });
  };

  const getMeasurementResults = () => {
    if (points.length < 2) return null;
    const dy = Math.abs(points[0].y - (points[1]?.y ?? points[0].y));
    const dx = points.length >= 4 ? Math.abs(points[2].x - points[3].x) : 0;
    
    // Scale to simulated mm metrics
    const vertMm = Math.round(dy * 3.5);
    const horizMm = Math.round(dx * 3.5);
    const ratio = vertMm > 0 ? (horizMm / vertMm).toFixed(2) : "0.00";

    return { vertMm, horizMm, ratio };
  };

  const meas = getMeasurementResults();

  return (
    <div className="flex flex-col space-y-3 w-full">
      {/* Dynamic Instruction Bar */}
      <div className="bg-[#0d1117] border border-gray-800 rounded px-3 py-1.5 text-[10px] font-mono text-gray-400 flex items-center justify-between">
        <span>
          {activeMode === "MEASURE" && `[CALIPER MODE]: Click to set landmarks (${points.length}/4 points set)`}
          {activeMode === "SEGMENT" && "[SEGMENTATION MODE]: Rendering U-Net lung contours"}
          {activeMode === "EVIDENCE" && "[EVIDENCE LAYER]: Spatially anchored anomalies active"}
          {activeMode === "SCAN" && "[SCANNING ACTIVE]: Image grid calibration ready"}
          {activeMode === "ANNOTATE" && "[ANNOTATE MODE]: Visual markup active"}
          {activeMode === "IMAGE" && "[IMAGE MODE]: Drag sliders to adjust filter attributes"}
        </span>
        <span className="text-gray-600">X: {mousePos.x}% Y: {mousePos.y}%</span>
      </div>

      {/* Main Viewport Container */}
      <div
        ref={containerRef}
        onClick={handleCanvasClick}
        onMouseMove={handleMouseMove}
        className="relative border border-gray-800 rounded-lg bg-[#07090e] h-[450px] flex items-center justify-center overflow-hidden cursor-crosshair group"
      >
        {/* Reticles & Border markings */}
        <div className="absolute inset-4 border border-gray-900/30 pointer-events-none z-0"></div>
        <div className="absolute top-2 left-2 border-t-2 border-l-2 border-gray-700 w-3 h-3 pointer-events-none"></div>
        <div className="absolute top-2 right-2 border-t-2 border-r-2 border-gray-700 w-3 h-3 pointer-events-none"></div>
        <div className="absolute bottom-2 left-2 border-b-2 border-l-2 border-gray-700 w-3 h-3 pointer-events-none"></div>
        <div className="absolute bottom-2 right-2 border-b-2 border-r-2 border-gray-700 w-3 h-3 pointer-events-none"></div>

        {/* Dynamic Image Display */}
        {study ? (
          <div
            className="relative select-none max-h-[90%] max-w-[90%] transition-all duration-200"
            style={{
              transform: `scale(${zoomLevel})`,
              filter: `brightness(${brightness}%) contrast(${contrast}%) saturate(${100 + sharpness}%)`,
            }}
          >
            {/* Chest X-Ray Image */}
            <img src={study.imageUrl} alt="DICOM scan study" className="object-contain max-h-[400px] pointer-events-none" />

            {/* SVG Interactive Drawing Plane */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none z-10">
              {/* U-NET SEGMENTATION OVERLAY */}
              {activeMode === "SEGMENT" && (
                <>
                  {/* Left Lung overlay */}
                  <path
                    d="M 25 30 C 20 20, 10 30, 8 50 C 6 70, 12 85, 20 90 C 28 85, 30 50, 25 30 Z"
                    fill="rgba(59, 130, 246, 0.15)"
                    stroke="#3B82F6"
                    strokeWidth="1.5"
                    strokeDasharray="2 1"
                    transform="scale(4) translate(5, 5)"
                  />
                  {/* Right Lung overlay */}
                  <path
                    d="M 45 30 C 40 20, 30 30, 28 50 C 26 70, 32 85, 40 90 C 48 85, 50 50, 45 30 Z"
                    fill="rgba(59, 130, 246, 0.15)"
                    stroke="#3B82F6"
                    strokeWidth="1.5"
                    strokeDasharray="2 1"
                    transform="scale(4) translate(5, 5)"
                  />
                </>
              )}

              {/* CALIPERS / MEASUREMENT MARKERS */}
              {activeMode === "MEASURE" && (
                <>
                  {/* Calibration lines */}
                  {points[0] && points[1] && (
                    <line
                      x1={`${points[0].x}%`}
                      y1={`${points[0].y}%`}
                      x2={`${points[1].x}%`}
                      y2={`${points[1].y}%`}
                      stroke="#3B82F6"
                      strokeWidth="1.5"
                    />
                  )}
                  {points[2] && points[3] && (
                    <line
                      x1={`${points[2].x}%`}
                      y1={`${points[2].y}%`}
                      x2={`${points[3].x}%`}
                      y2={`${points[3].y}%`}
                      stroke="#3B82F6"
                      strokeWidth="1.5"
                    />
                  )}

                  {/* Highlight dots */}
                  {points.map((p, idx) => {
                    const labels = ["SUP", "INF", "L_BND", "R_BND"];
                    return (
                      <g key={idx}>
                        <circle cx={`${p.x}%`} cy={`${p.y}%`} r="3.5" fill="#3B82F6" stroke="#ffffff" strokeWidth="1" />
                        <text
                          x={`${p.x + 2}%`}
                          y={`${p.y - 2}%`}
                          fill="#3B82F6"
                          className="text-[8px] font-mono font-bold fill-blue-400 bg-black"
                        >
                          {labels[idx]}
                        </text>
                      </g>
                    );
                  })}
                </>
              )}
            </svg>

            {/* FLOATING ANCHORED ISSUES */}
            {activeMode === "EVIDENCE" &&
              evidence.map((item) => (
                <div
                  key={item.id}
                  className="absolute z-20"
                  style={{ left: `${item.xPercent}%`, top: `${item.yPercent}%` }}
                >
                  {/* Pulse Pin */}
                  <div className="relative flex items-center justify-center">
                    <span className="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-red-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-red-500"></span>
                  </div>

                  {/* floating evidence dialog */}
                  <div className="absolute left-4 top-0 w-52 bg-[#0d1117]/95 border border-red-900/50 rounded-lg p-2.5 shadow-xl text-[9px] font-mono text-gray-300 space-y-2">
                    <div className="flex justify-between items-center text-red-400 font-bold border-b border-red-950 pb-1">
                      <span>ANOMALY // {item.id}</span>
                      <span>{Math.round(item.confidence * 100)}% CONF</span>
                    </div>
                    <div>
                      <span className="text-gray-500 block">REGION:</span>
                      <span>{item.region}</span>
                    </div>
                    <div>
                      <span className="text-gray-500 block">SIGNAL:</span>
                      <span>{item.signal}</span>
                    </div>

                    <div className="space-y-1">
                      <span className="text-gray-500 block">OBSERVATION NOTE:</span>
                      <input
                        type="text"
                        placeholder="Add clinical observation..."
                        value={notes[item.id] || ""}
                        onChange={(e) => setNotes({ ...notes, [item.id]: e.target.value })}
                        className="w-full bg-[#07090e] border border-gray-800 rounded px-1.5 py-0.5 text-[8px] text-gray-300 focus:outline-none"
                      />
                    </div>
                  </div>
                </div>
              ))}
          </div>
        ) : (
          <div className="text-xs text-gray-600 font-mono">[ ACTIVE STUDY VIEWPORT EMPTY ]</div>
        )}
      </div>

      {/* Measurement Metrics Display panel */}
      {activeMode === "MEASURE" && meas && (
        <div className="bg-[#0d1117] border border-gray-800 rounded p-3 text-[10px] font-mono grid grid-cols-3 gap-2">
          <div>
            <span className="text-gray-500 block">VERT LANDMARK DISTANCE</span>
            <span className="text-white font-bold">{meas.vertMm} mm</span>
          </div>
          <div>
            <span className="text-gray-500 block">HORIZ LANDMARK DISTANCE</span>
            <span className="text-white font-bold">{meas.horizMm} mm</span>
          </div>
          <div>
            <span className="text-gray-500 block">EXPANSION RATIO (H/V)</span>
            <span className="text-blue-400 font-bold">{meas.ratio}</span>
          </div>
        </div>
      )}

      {/* Control Strip */}
      {study && (
        <div className="flex justify-between items-center bg-[#0d1117] p-2 border border-gray-850 rounded-lg">
          <div className="flex items-center space-x-1">
            <button
              onClick={onZoomIn}
              className="px-2 py-1 bg-gray-900 border border-gray-800 hover:bg-gray-800 text-gray-400 rounded text-[9px] font-mono"
            >
              ZOOM +
            </button>
            <button
              onClick={onZoomOut}
              className="px-2 py-1 bg-gray-900 border border-gray-800 hover:bg-gray-800 text-gray-400 rounded text-[9px] font-mono"
            >
              ZOOM -
            </button>
            <button
              onClick={onReset}
              className="px-2 py-1 bg-gray-900 border border-gray-800 hover:bg-gray-800 text-gray-400 rounded text-[9px] font-mono"
            >
              RESET
            </button>
            <button
              onClick={onToggleFullscreen}
              className="px-2 py-1 bg-gray-900 border border-gray-800 hover:bg-gray-800 text-gray-400 rounded text-[9px] font-mono"
            >
              FULL
            </button>
          </div>
          <span className="text-[9px] text-gray-500 font-mono uppercase">DICOM VIEWER MODE</span>
        </div>
      )}
    </div>
  );
}
