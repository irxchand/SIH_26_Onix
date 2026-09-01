"use client";

import React, { useState } from "react";

interface UploadWidgetProps {
  onFileSelected: (file: File) => void;
}

export default function UploadWidget({ onFileSelected }: UploadWidgetProps) {
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith("image/")) {
        onFileSelected(file);
      } else {
        alert("Please upload a valid image file (JPEG/PNG).");
      }
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      onFileSelected(e.target.files[0]);
      e.target.value = "";
    }
  };

  return (
    <div
      className={`relative flex flex-col items-center justify-center w-full h-[400px] border-2 border-dashed rounded-lg transition-all duration-200 ${
        dragActive
          ? "border-blue-500 bg-blue-950/20"
          : "border-gray-800 bg-[#0d1117] hover:border-gray-700 hover:bg-[#12161f]"
      }`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input
        type="file"
        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
        onChange={handleChange}
        accept="image/*,.dcm,.png,.jpg,.jpeg,.bmp,.webp"
      />

      <div className="flex flex-col items-center space-y-4 p-8 text-center pointer-events-none">
        {/* Reticle / Medical Scanner Icon */}
        <div className="relative w-16 h-16 flex items-center justify-center">
          <div className="absolute inset-0 border border-gray-700 rounded-full animate-pulse"></div>
          <div className="absolute w-8 h-px bg-gray-600"></div>
          <div className="absolute h-8 w-px bg-gray-600"></div>
          <svg className="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 12h10M12 7v10" />
          </svg>
        </div>

        <div>
          <p className="text-sm font-semibold text-gray-300">IMPORT CHEST X-RAY STUDY</p>
          <p className="text-xs text-gray-500 mt-1">Drag & Drop DICOM/JPEG/PNG format</p>
        </div>

        <button className="px-4 py-1.5 bg-gray-850 hover:bg-gray-800 border border-gray-700 text-xs text-gray-400 hover:text-white rounded transition-colors font-medium">
          Select Source Image
        </button>

        <div className="text-[10px] text-gray-600 space-y-1">
          <p>Supported dimensions: up to 4096 x 4096 px</p>
          <p>Strict patient de-identification applied locally</p>
        </div>
      </div>
    </div>
  );
}
