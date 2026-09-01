"use client";

import React, { useState, useRef, useEffect } from "react";
import { ToolMode, MeasurementPoint, EvidenceItem, Study, ChecklistStep, BoundingBox } from "../types/workstation";

interface XrayCanvasProps {
  study: Study | null;
  activeMode: ToolMode;
  pixelSpacingMm: number;
  imageWidth: number;
  brightness: number;
  contrast: number;
  sharpness: number;
  evidence: EvidenceItem[];
  zoomLevel: number;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onReset: () => void;
  onToggleFullscreen: () => void;
  checklist: ChecklistStep[];
  onChecklistUpdate: (updatedChecklist: ChecklistStep[]) => void;
  imageHeight?: number;
  annoTrigger?: number;
  activePinId?: string | null;
  onHoverPin?: (id: string | null) => void;
}

export default function XrayCanvas({
  study,
  activeMode,
  pixelSpacingMm,
  imageWidth,
  brightness,
  contrast,
  sharpness,
  evidence,
  zoomLevel,
  onZoomIn,
  onZoomOut,
  onReset,
  onToggleFullscreen,
  checklist,
  onChecklistUpdate,
  imageHeight,
  annoTrigger,
  activePinId = null,
  onHoverPin,
}: XrayCanvasProps) {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [notes, setNotes] = useState<Record<string, string>>({});
  const [measurementNote, setMeasurementNote] = useState("");
  const [savedMeasurementIssue, setSavedMeasurementIssue] = useState(false);
  const [segmentationPaths, setSegmentationPaths] = useState<{leftLung: string, rightLung: string} | null>(null);
  const [segmentationMode, setSegmentationMode] = useState<"ground_truth" | "automated">("ground_truth");
  
  // Annotation states
  const [isDrawing, setIsDrawing] = useState(false);
  const [dragStart, setDragStart] = useState<{ x: number; y: number } | null>(null);
  const [currentBox, setCurrentBox] = useState<{ x: number; y: number; width: number; height: number } | null>(null);
  const [drawnBoxes, setDrawnBoxes] = useState<BoundingBox[]>([]);
  const [globalTags, setGlobalTags] = useState<string[]>([]);
  
  // Evidence dragging states
  const [localEvidence, setLocalEvidence] = useState<EvidenceItem[]>(evidence);
  const [draggingPin, setDraggingPin] = useState<string | null>(null);

  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setLocalEvidence(evidence);
  }, [evidence]);

  useEffect(() => {
    // Reset state on study change
    setMeasurementNote("");
    setSavedMeasurementIssue(false);
    setSegmentationPaths(null);
  }, [study]);

  useEffect(() => {
    if (activeMode === "SEGMENT" && study) {
      setSegmentationPaths(null); // Reset path
      fetch(`http://localhost:8000/api/v1/studies/${study.id}/segmentation?mode=${segmentationMode}`)
        .then(res => res.ok ? res.json() : null)
        .then(data => {
          if (data && data.leftLung && data.rightLung) {
            setSegmentationPaths({ leftLung: data.leftLung, rightLung: data.rightLung });
          }
        })
        .catch(err => console.error("Failed to fetch segmentation:", err));
    } else if (activeMode === "ANNOTATE" && study) {
      fetch(`http://localhost:8000/api/v1/studies/${study.id}/annotations`)
        .then(res => res.ok ? res.json() : null)
        .then(data => {
          if (data) {
            setDrawnBoxes(data.boxes || []);
            setGlobalTags(data.global_tags || []);
          }
        })
        .catch(err => console.error("Failed to fetch annotations:", err));
    }
  }, [activeMode, study, segmentationMode, annoTrigger]);

  const handlePointerDown = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = Math.round(((e.clientX - rect.left) / rect.width) * 100);
    const y = Math.round(((e.clientY - rect.top) / rect.height) * 100);

    if (activeMode === "MEASURE") {
      const pendingIdx = checklist.findIndex(item => item.status === "pending");
      if (pendingIdx !== -1) {
        const updated = [...checklist];
        updated[pendingIdx] = { ...updated[pendingIdx], status: "completed", point: { x, y } };
        onChecklistUpdate(updated);
      }
    } else if (activeMode === "ANNOTATE") {
      setIsDrawing(true);
      const fx = ((e.clientX - rect.left) / rect.width) * 100;
      const fy = ((e.clientY - rect.top) / rect.height) * 100;
      setDragStart({ x: fx, y: fy });
      setCurrentBox({ x: fx, y: fy, width: 0, height: 0 });
      (e.target as HTMLElement).setPointerCapture(e.pointerId);
    }
  };

  const handlePointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = Math.round(((e.clientX - rect.left) / rect.width) * 100);
    const y = Math.round(((e.clientY - rect.top) / rect.height) * 100);
    setMousePos({ x, y });

    if (activeMode === "ANNOTATE" && isDrawing && dragStart) {
       const fx = ((e.clientX - rect.left) / rect.width) * 100;
       const fy = ((e.clientY - rect.top) / rect.height) * 100;
       setCurrentBox({
         x: Math.min(dragStart.x, fx),
         y: Math.min(dragStart.y, fy),
         width: Math.abs(fx - dragStart.x),
         height: Math.abs(fy - dragStart.y)
       });
    } else if (activeMode === "EVIDENCE" && draggingPin) {
       setLocalEvidence(prev => prev.map(pin => pin.id === draggingPin ? { ...pin, xPercent: x, yPercent: y } : pin));
    }
  };

  const handlePointerUp = (e: React.PointerEvent<HTMLDivElement>) => {
    if (activeMode === "ANNOTATE" && isDrawing) {
       setIsDrawing(false);
       if (currentBox && currentBox.width > 1 && currentBox.height > 1) {
         const newBox: BoundingBox = {
           id: `BOX-${Date.now()}`,
           label: "UNKNOWN",
           ...currentBox
         };
         const updated = [...drawnBoxes, newBox];
         setDrawnBoxes(updated);
         setDragStart(null);
         setCurrentBox(null);
         if (study) {
            fetch(`http://localhost:8000/api/v1/studies/${study.id}/annotations`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ boxes: updated, global_tags: globalTags })
            }).then(res => {
                if (res.status === 409) alert("Conflict: Another user has modified this study.");
            }).catch(console.error);
         }
       }
    } else if (activeMode === "EVIDENCE" && draggingPin) {
       setDraggingPin(null);
    }
  };

  const getMeasurementResults = () => {
    const heartRight = checklist.find(i => i.id === "heart_right")?.point;
    const heartLeft = checklist.find(i => i.id === "heart_left")?.point;
    const chestRight = checklist.find(i => i.id === "chest_right")?.point;
    const chestLeft = checklist.find(i => i.id === "chest_left")?.point;

    if (!heartRight || !heartLeft || !chestRight || !chestLeft) return null;

    const hDistPx = Math.abs(heartLeft.x - heartRight.x);
    const cDistPx = Math.abs(chestLeft.x - chestRight.x);

    // True physical conversion using the actual image dimensions fetched from OpenCV
    // Since coordinates are percentages (0-100), distance in true pixels is: (percentage / 100) * imageWidth
    const hDistTruePx = (hDistPx / 100.0) * imageWidth;
    const cDistTruePx = (cDistPx / 100.0) * imageWidth;
    
    const hDistMm = Math.round(hDistTruePx * pixelSpacingMm);
    const cDistMm = Math.round(cDistTruePx * pixelSpacingMm);
    const ratio = cDistMm > 0 ? (hDistMm / cDistMm) : 0;
    
    return { hDistMm, cDistMm, ratio, isComplete: true };
  };

  const meas = getMeasurementResults();
  
  const getCompletedPoints = () => checklist.filter(item => item.status === "completed" && item.point).map(item => item.point!);

  return (
    <div className="flex flex-col space-y-3 w-full">
      {/* Dynamic Instruction Bar */}
      <div className="bg-[#0d1117] border border-gray-800 rounded px-3 py-1.5 text-[10px] font-mono text-gray-400 flex items-center justify-between">
        <span className="flex items-center space-x-2">
          {activeMode === "MEASURE" && (
            <div className="flex items-center space-x-4">
              <span>{`[CALIPER MODE]: Click to set landmarks (${getCompletedPoints().length}/${checklist.length} points set)`}</span>
              <button 
                onClick={async () => {
                  if (!study) return;
                  try {
                    const res = await fetch(`http://localhost:8000/api/v1/studies/${study.id}/segmentation?mode=ground_truth`);
                    let data = res.ok ? await res.json() : null;
                    if (!data || !data.leftLung || !data.rightLung) {
                      const res2 = await fetch(`http://localhost:8000/api/v1/studies/${study.id}/segmentation?mode=automated`);
                      data = res2.ok ? await res2.json() : null;
                    }

                    let autoPoints = [
                      { id: "spine_top", x: 50, y: 30 },
                      { id: "spine_bottom", x: 50, y: 70 },
                      { id: "heart_right", x: 45, y: 50 },
                      { id: "heart_left", x: 55, y: 50 },
                      { id: "chest_right", x: 30, y: 50 },
                      { id: "chest_left", x: 70, y: 50 }
                    ];

                    if (data && data.leftLung && data.rightLung) {
                      const parseSvgPath = (path: string) => {
                        const matches = path.match(/[-+]?[0-9]*\.?[0-9]+/g);
                        if (!matches) return [];
                        const coords: { x: number; y: number }[] = [];
                        for (let i = 0; i < matches.length; i += 2) {
                          const x = parseFloat(matches[i]);
                          const y = parseFloat(matches[i + 1]);
                          if (!isNaN(x) && !isNaN(y)) {
                            coords.push({ x, y });
                          }
                        }
                        return coords;
                      };

                      const leftCoords = parseSvgPath(data.leftLung);
                      const rightCoords = parseSvgPath(data.rightLung);

                      if (leftCoords.length > 0 && rightCoords.length > 0) {
                        const rightXs = rightCoords.map(c => c.x);
                        const rightYs = rightCoords.map(c => c.y);
                        const minRightX = Math.min(...rightXs);
                        const maxRightX = Math.max(...rightXs);
                        
                        const leftXs = leftCoords.map(c => c.x);
                        const leftYs = leftCoords.map(c => c.y);
                        const minLeftX = Math.min(...leftXs);
                        const maxLeftX = Math.max(...leftXs);

                        const allYs = [...rightYs, ...leftYs];
                        const minY = Math.min(...allYs);
                        const maxY = Math.max(...allYs);

                        const chestRightY = rightCoords.find(c => c.x === minRightX)?.y || 65;
                        const chestLeftY = leftCoords.find(c => c.x === maxLeftX)?.y || 65;
                        const heartRightY = rightCoords.find(c => c.x === maxRightX)?.y || 60;
                        const heartLeftY = leftCoords.find(c => c.x === minLeftX)?.y || 60;

                        const chestY = (chestRightY + chestLeftY) / 2;
                        const heartY = (heartRightY + heartLeftY) / 2;

                        const spineX = (maxRightX + minLeftX) / 2;

                        autoPoints = [
                          { id: "spine_top", x: spineX, y: Math.max(5, minY - 3) },
                          { id: "spine_bottom", x: spineX, y: Math.min(95, maxY + 5) },
                          { id: "heart_right", x: maxRightX, y: heartY },
                          { id: "heart_left", x: minLeftX, y: heartY },
                          { id: "chest_right", x: minRightX, y: chestY },
                          { id: "chest_left", x: maxLeftX, y: chestY }
                        ];
                      }
                    }

                    const updated = checklist.map(item => {
                      const ap = autoPoints.find(p => p.id === item.id);
                      return ap ? { ...item, status: "completed" as const, point: { x: ap.x, y: ap.y } } : item;
                    });
                    onChecklistUpdate(updated);

                  } catch (err) {
                    console.error("Auto-measure failed:", err);
                  }
                }}
                className="px-2 py-0.5 bg-blue-900/30 text-blue-400 border border-blue-800 rounded hover:bg-blue-800/50 transition-colors"
              >
                AUTO-MEASURE
              </button>
            </div>
          )}
          {activeMode === "SEGMENT" && (
            <span className="flex items-center space-x-2">
              <span>[SEGMENTATION]:</span>
              <button 
                onClick={() => setSegmentationMode("ground_truth")}
                className={`px-1.5 py-0.5 rounded text-[8px] font-bold transition-all ${
                  segmentationMode === "ground_truth" 
                    ? "bg-purple-900/60 text-purple-300 border border-purple-800" 
                    : "bg-gray-900/40 text-gray-500 border border-transparent hover:text-gray-300"
                }`}
              >
                Ground Truth Reference
              </button>
              <button 
                onClick={() => setSegmentationMode("automated")}
                className={`px-1.5 py-0.5 rounded text-[8px] font-bold transition-all ${
                  segmentationMode === "automated" 
                    ? "bg-blue-900/60 text-blue-300 border border-blue-800" 
                    : "bg-gray-900/40 text-gray-500 border border-transparent hover:text-gray-300"
                }`}
              >
                Automated (Otsu Threshold)
              </button>
            </span>
          )}
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
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
        className="relative border border-gray-800 rounded-lg bg-[#07090e] h-[450px] flex items-center justify-center overflow-hidden cursor-crosshair group touch-none"
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
              {(activeMode === "SEGMENT" || activeMode === "EVIDENCE") && segmentationPaths && (
                <svg width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none">
                  {/* Left Lung overlay */}
                  <path
                    d={segmentationPaths.leftLung}
                    fill="rgba(59, 130, 246, 0.15)"
                    stroke="#3B82F6"
                    strokeWidth="1.5"
                    strokeDasharray="2 1"
                    vectorEffect="non-scaling-stroke"
                  />
                  {/* Right Lung overlay */}
                  <path
                    d={segmentationPaths.rightLung}
                    fill="rgba(59, 130, 246, 0.15)"
                    stroke="#3B82F6"
                    strokeWidth="1.5"
                    strokeDasharray="2 1"
                    vectorEffect="non-scaling-stroke"
                  />
                </svg>
              )}

              {/* CALIPERS / MEASUREMENT MARKERS */}
              {activeMode === "MEASURE" && (
                <>
                  {/* Lines between specific points */}
                  {checklist.find(i=>i.id==="spine_top")?.point && checklist.find(i=>i.id==="spine_bottom")?.point && (
                    <line x1={`${checklist.find(i=>i.id==="spine_top")!.point!.x}%`} y1={`${checklist.find(i=>i.id==="spine_top")!.point!.y}%`} 
                          x2={`${checklist.find(i=>i.id==="spine_bottom")!.point!.x}%`} y2={`${checklist.find(i=>i.id==="spine_bottom")!.point!.y}%`} 
                          stroke="#3B82F6" strokeWidth="1" strokeDasharray="3 2" />
                  )}
                  {checklist.find(i=>i.id==="heart_right")?.point && checklist.find(i=>i.id==="heart_left")?.point && (
                    <line x1={`${checklist.find(i=>i.id==="heart_right")!.point!.x}%`} y1={`${checklist.find(i=>i.id==="heart_right")!.point!.y}%`} 
                          x2={`${checklist.find(i=>i.id==="heart_left")!.point!.x}%`} y2={`${checklist.find(i=>i.id==="heart_left")!.point!.y}%`} 
                          stroke="#3B82F6" strokeWidth="1.5" />
                  )}
                  {checklist.find(i=>i.id==="chest_right")?.point && checklist.find(i=>i.id==="chest_left")?.point && (
                    <line x1={`${checklist.find(i=>i.id==="chest_right")!.point!.x}%`} y1={`${checklist.find(i=>i.id==="chest_right")!.point!.y}%`} 
                          x2={`${checklist.find(i=>i.id==="chest_left")!.point!.x}%`} y2={`${checklist.find(i=>i.id==="chest_left")!.point!.y}%`} 
                          stroke="#3B82F6" strokeWidth="1.5" />
                  )}

                  {/* Highlight dots */}
                  {checklist.map((item, idx) => {
                    if (!item.point) return null;
                    return (
                      <g key={idx}>
                        {/* If it's a saved issue (like chest right in the video), add red marker */}
                        {(item.id === "chest_left" && savedMeasurementIssue) ? (
                           <>
                             <circle cx={`${item.point.x}%`} cy={`${item.point.y}%`} r="6" fill="rgba(248,113,113,0.3)" />
                             <circle cx={`${item.point.x}%`} cy={`${item.point.y}%`} r="3" fill="#EF4444" stroke="#ffffff" strokeWidth="1" />
                           </>
                        ) : (
                          <circle cx={`${item.point.x}%`} cy={`${item.point.y}%`} r="3.5" fill="#3B82F6" stroke="#ffffff" strokeWidth="1" />
                        )}
                      </g>
                    );
                  })}
                </>
              )}
              
              {/* ML BOUNDING BOX ANNOTATIONS */}
              {activeMode === "ANNOTATE" && (
                <>
                  {drawnBoxes.map((box) => (
                    <g key={box.id}>
                      <rect 
                        x={`${box.x}%`} y={`${box.y}%`} 
                        width={`${box.width}%`} height={`${box.height}%`} 
                        fill="rgba(59, 130, 246, 0.2)" 
                        stroke="#3B82F6" strokeWidth="2" 
                      />
                      <text 
                        x={`${box.x}%`} y={`${box.y - 1}%`} 
                        fill="#3B82F6" fontSize="10" fontFamily="monospace"
                      >
                        {box.label}
                      </text>
                    </g>
                  ))}
                  {currentBox && (
                    <rect 
                      x={`${currentBox.x}%`} y={`${currentBox.y}%`} 
                      width={`${currentBox.width}%`} height={`${currentBox.height}%`} 
                      fill="rgba(59, 130, 246, 0.4)" 
                      stroke="#3B82F6" strokeWidth="2" strokeDasharray="4"
                    />
                  )}
                </>
              )}
            </svg>

            {/* INTERACTIVE MEASUREMENT POPOVER */}
            {activeMode === "MEASURE" && meas?.isComplete && !savedMeasurementIssue && (
               <div 
                 className="absolute z-30 bg-[#0d1117] border border-gray-700 shadow-2xl rounded-lg p-3 text-[10px] font-mono w-64"
                 style={{ 
                   left: `${checklist.find(i=>i.id==="chest_left")!.point!.x + 2}%`, 
                   top: `${checklist.find(i=>i.id==="chest_left")!.point!.y + 2}%` 
                 }}
                 onClick={(e) => e.stopPropagation()}
               >
                 <div className="flex justify-between items-center mb-2">
                   <span className="text-gray-300 font-bold">Issues</span>
                   <span className="text-gray-500 cursor-pointer text-xs" onClick={() => setSavedMeasurementIssue(true)}>✕</span>
                 </div>
                 
                 <div className="text-gray-400 mb-2 border-b border-gray-800 pb-2">
                   H {meas.hDistMm}mm / C {meas.cDistMm}mm / R {(meas.ratio * 100).toFixed(2)}%
                 </div>

                 {meas.ratio > 0.50 ? (
                   <div className="bg-red-950/40 text-red-400 border border-red-900 rounded px-2 py-1 mb-2 font-bold inline-block">
                     ABOVE AVERAGE RATIO
                   </div>
                 ) : (
                   <div className="bg-green-950/40 text-green-400 border border-green-900 rounded px-2 py-1 mb-2 font-bold inline-block">
                     NORMAL RATIO
                   </div>
                 )}

                 <textarea
                   className="w-full h-16 bg-[#07090e] border border-gray-700 rounded p-1.5 text-gray-300 focus:border-blue-500 focus:outline-none resize-none mb-2 placeholder-gray-600"
                   placeholder="Type here..."
                   value={measurementNote}
                   onChange={(e) => setMeasurementNote(e.target.value)}
                 />

                 <button 
                   className="w-full bg-[#40b8c4] hover:bg-[#3496a0] text-black font-bold py-1.5 rounded transition-colors"
                   onClick={async (e) => { 
                     e.stopPropagation(); 
                     setSavedMeasurementIssue(true); 
                     if (study) {
                       try {
                         const res = await fetch(`http://localhost:8000/api/v1/studies/${study.id}/measurements`, {
                           method: 'POST',
                           headers: { 'Content-Type': 'application/json' },
                           body: JSON.stringify({
                             points: checklist,
                             hDistMm: meas.hDistMm,
                             cDistMm: meas.cDistMm,
                             ratio: meas.ratio,
                             note: measurementNote
                           })
                         });
                         if (res.status === 409) alert("Conflict: Another user has modified this study.");
                       } catch(err) {
                         console.error(err);
                       }
                     }
                   }}
                 >
                   Save ✓
                 </button>
               </div>
            )}

            {/* FLOATING ANCHORED ISSUES */}
            {activeMode === "EVIDENCE" &&
              localEvidence.map((item) => (
                <div
                  key={item.id}
                  className="absolute z-20"
                  style={{ left: `${item.xPercent}%`, top: `${item.yPercent}%` }}
                >
                  {/* Pulse Pin */}
                  <div 
                    className="relative flex items-center justify-center cursor-move"
                    onPointerDown={(e) => {
                      e.stopPropagation();
                      setDraggingPin(item.id);
                    }}
                  >
                    <span className="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-red-400 opacity-75 pointer-events-none"></span>
                    <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-red-500 pointer-events-none"></span>
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
                        onBlur={async () => {
                          if (study && notes[item.id]) {
                            try {
                              const res = await fetch(`http://localhost:8000/api/v1/studies/${study.id}/evidence`, {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ note: notes[item.id], xPercent: item.xPercent, yPercent: item.yPercent })
                              });
                              if (res.status === 409) alert("Conflict: Another user has modified this study.");
                            } catch(err) { console.error(err); }
                          }
                        }}
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
            <span className="text-gray-500 block">HEART DIAMETER (H)</span>
            <span className="text-white font-bold">{meas.hDistMm} mm</span>
          </div>
          <div>
            <span className="text-gray-500 block">CHEST DIAMETER (C)</span>
            <span className="text-white font-bold">{meas.cDistMm} mm</span>
          </div>
          <div>
            <span className="text-gray-500 block">CARDIOTHORACIC RATIO</span>
            <span className="text-blue-400 font-bold">{(meas.ratio * 100).toFixed(2)}%</span>
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
