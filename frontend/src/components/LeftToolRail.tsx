"use client";

import React from "react";
import { ToolMode } from "../types/workstation";

interface LeftToolRailProps {
  activeMode: ToolMode;
  onModeChange: (mode: ToolMode) => void;
  brightness: number;
  onBrightnessChange: (val: number) => void;
  contrast: number;
  onContrastChange: (val: number) => void;
  sharpness: number;
  onSharpnessChange: (val: number) => void;
}

export default function LeftToolRail({
  activeMode,
  onModeChange,
  brightness,
  onBrightnessChange,
  contrast,
  onContrastChange,
  sharpness,
  onSharpnessChange,
}: LeftToolRailProps) {
  const tools = [
    { id: "SCAN" as ToolMode, label: "SCAN", desc: "Pipeline trigger" },
    { id: "MEASURE" as ToolMode, label: "MEASURE", desc: "Anatomical calipers" },
    { id: "ANNOTATE" as ToolMode, label: "ANNOTATE", desc: "Workspace markup" },
    { id: "SEGMENT" as ToolMode, label: "SEGMENT", desc: "U-Net Lung outline" },
    { id: "EVIDENCE" as ToolMode, label: "EVIDENCE", desc: "Anchored anomalies" },
    { id: "QUANTUM" as ToolMode, label: "QUANTUM", desc: "QML gate view" },
  ];

  return (
    <div className="w-48 bg-[#0d1117] border border-gray-800 rounded-lg p-3 space-y-6 flex flex-col justify-between h-[450px]">
      <div className="space-y-4">
        <span className="text-[10px] text-gray-500 font-mono tracking-widest block border-b border-gray-850 pb-1">
          ANATOMY // LAB
        </span>
        
        <nav className="flex flex-col space-y-1.5">
          {tools.map((tool) => {
            const isActive = activeMode === tool.id;
            return (
              <button
                key={tool.id}
                onClick={() => onModeChange(tool.id)}
                className={`w-full flex items-center justify-between px-2.5 py-2 rounded text-left transition-all ${
                  isActive
                    ? "bg-blue-950/30 border border-blue-900/60 text-blue-400 font-semibold"
                    : "border border-transparent text-gray-400 hover:text-gray-200 hover:bg-gray-850/40"
                }`}
              >
                <span className="text-[10px] font-mono tracking-wide">{tool.label}</span>
                <span className={`w-1.5 h-1.5 rounded-full ${isActive ? "bg-blue-400" : "bg-transparent"}`}></span>
              </button>
            );
          })}
        </nav>
      </div>

      <div className="space-y-3 pt-3 border-t border-gray-850">
        <span className="text-[9px] text-gray-500 font-mono tracking-wider block">IMAGE CONTROLS</span>
        
        <div className="space-y-2">
          {/* Brightness slider */}
          <div className="space-y-1">
            <div className="flex justify-between text-[9px] font-mono text-gray-500">
              <span>BRIGHT</span>
              <span>{brightness}%</span>
            </div>
            <input
              type="range"
              min="50"
              max="150"
              value={brightness}
              onChange={(e) => onBrightnessChange(Number(e.target.value))}
              className="w-full accent-blue-500 h-1 bg-gray-900 rounded-lg appearance-none cursor-pointer"
            />
          </div>

          {/* Contrast slider */}
          <div className="space-y-1">
            <div className="flex justify-between text-[9px] font-mono text-gray-500">
              <span>CONTRAST</span>
              <span>{contrast}%</span>
            </div>
            <input
              type="range"
              min="50"
              max="150"
              value={contrast}
              onChange={(e) => onContrastChange(Number(e.target.value))}
              className="w-full accent-blue-500 h-1 bg-gray-900 rounded-lg appearance-none cursor-pointer"
            />
          </div>

          {/* Sharpness (Simulated using CSS contrast/saturate mix) */}
          <div className="space-y-1">
            <div className="flex justify-between text-[9px] font-mono text-gray-500">
              <span>SHARP</span>
              <span>{sharpness}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="200"
              value={sharpness}
              onChange={(e) => onSharpnessChange(Number(e.target.value))}
              className="w-full accent-blue-500 h-1 bg-gray-900 rounded-lg appearance-none cursor-pointer"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
