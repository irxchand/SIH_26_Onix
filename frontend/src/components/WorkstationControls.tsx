"use client";

import React from "react";

interface WorkstationControlsProps {
  onZoomIn: () => void;
  onZoomOut: () => void;
  onReset: () => void;
  onToggleFullscreen: () => void;
}

export default function WorkstationControls({
  onZoomIn,
  onZoomOut,
  onReset,
  onToggleFullscreen,
}: WorkstationControlsProps) {
  return (
    <div className="flex items-center space-x-1 bg-[#111827] border border-gray-800 rounded-lg p-1 text-xs">
      <button
        onClick={onZoomIn}
        className="px-2 py-1.5 hover:bg-gray-800 text-gray-400 hover:text-white rounded transition-colors flex items-center space-x-1"
        title="Zoom In"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v6m3-3H7" />
        </svg>
        <span>Zoom +</span>
      </button>

      <button
        onClick={onZoomOut}
        className="px-2 py-1.5 hover:bg-gray-800 text-gray-400 hover:text-white rounded transition-colors flex items-center space-x-1"
        title="Zoom Out"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10H7" />
        </svg>
        <span>Zoom -</span>
      </button>

      <div className="w-px h-4 bg-gray-800 self-center"></div>

      <button
        onClick={onReset}
        className="px-2 py-1.5 hover:bg-gray-800 text-gray-400 hover:text-white rounded transition-colors flex items-center space-x-1"
        title="Fit Image"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
        </svg>
        <span>Fit</span>
      </button>

      <button
        onClick={onToggleFullscreen}
        className="px-2 py-1.5 hover:bg-gray-800 text-gray-400 hover:text-white rounded transition-colors flex items-center space-x-1"
        title="Toggle Fullscreen"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7" />
        </svg>
        <span>Full</span>
      </button>
    </div>
  );
}
