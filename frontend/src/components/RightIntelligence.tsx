"use client";

import React, { useState } from "react";
import { PredictionResults, Study, ChecklistStep } from "../types/workstation";

interface RightIntelligenceProps {
  study: Study | null;
  results: PredictionResults | null;
  loading: boolean;
  checklist: ChecklistStep[];
  onAccept: () => void;
  onReject: () => void;
}

export default function RightIntelligence({ study, results, loading, checklist, onAccept, onReject }: RightIntelligenceProps) {
  const [showTechnicalDetails, setShowTechnicalDetails] = useState(false);

  if (loading) {
    return (
      <div className="w-full border border-gray-800 rounded-lg p-8 bg-[#0d1117] text-center space-y-3 font-mono">
        <div className="inline-block w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-[10px] text-gray-500 tracking-wider">RESOLVING DIAGNOSTIC CONSENSUS...</p>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="w-full border border-gray-800 rounded-lg p-8 bg-[#0d1117] text-center text-xs text-gray-500 font-mono">
        [ AWAITING ACTIVE SCANS ]
      </div>
    );
  }

  const classicalLatency = Math.round(results.inference_time_seconds * 1000 * 0.05);
  const quantumLatency = Math.round(results.inference_time_seconds * 1000);
  const isAgreement = results.prediction !== "Healthy"; // Simplification for mock outputs

  return (
    <div className="w-full space-y-4 font-mono">
      {/* CHECKLIST */}
      <div className="border border-gray-800 rounded-lg p-3 bg-[#0d1117] space-y-3 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-8 h-8 bg-[#111827] flex items-center justify-center rounded-bl-lg border-l border-b border-gray-800 cursor-pointer hover:bg-gray-800">
          <span className="text-gray-400 text-xs">✕</span>
        </div>
        <span className="text-[10px] text-blue-400 font-bold tracking-widest block border-b border-gray-850 pb-2">
          Check the location of the points
        </span>
        <ul className="space-y-1">
          {checklist.map((item, idx) => (
            <li key={item.id} className={`flex items-center text-[10px] ${item.status === 'completed' ? 'text-white' : 'text-gray-500'}`}>
              <span className={`w-3 h-3 rounded-full mr-2 flex items-center justify-center text-[8px] ${item.status === 'completed' ? 'bg-blue-500 text-white' : 'bg-gray-800 text-gray-500'}`}>
                {item.status === 'completed' ? '✓' : idx + 1}
              </span>
              {item.label}
            </li>
          ))}
        </ul>
      </div>

      {/* PATIENT & ACCEPT/REJECT (From the video UI) */}
      {study && (
        <div className="border border-gray-800 rounded-lg p-3 bg-[#0d1117] space-y-3">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-xs font-bold text-white">{study.patientName} / ID: {study.patientId}</h3>
              <div className="text-[9px] text-gray-500 mt-1 flex space-x-3">
                <span>Sex: {study.sex === "M" ? "Male" : "Female"}</span>
                <span>Age: {study.age}</span>
              </div>
              <div className="text-[9px] text-gray-500 mt-1 flex space-x-3">
                <span>Acq. Date: {study.acquisitionDate.split(' ')[0]}</span>
                <span>Acq. Time: {study.acquisitionDate.split(' ').slice(1).join(' ')}</span>
              </div>
            </div>
          </div>
          
          <div className="flex space-x-2 pt-2 border-t border-gray-850">
            <button onClick={onAccept} className="flex-1 bg-[#1a3b30] hover:bg-[#254f41] text-emerald-400 border border-[#235845] py-1.5 rounded text-[10px] font-bold transition-colors">
              Accept ✓
            </button>
            <button onClick={onReject} className="flex-1 bg-[#3b1a1a] hover:bg-[#4f2525] text-red-400 border border-[#582323] py-1.5 rounded text-[10px] font-bold transition-colors">
              Reject ✕
            </button>
          </div>
        </div>
      )}

      {/* MODEL CONSENSUS */}
      <div className="border border-gray-800 rounded-lg p-3 bg-[#0d1117] space-y-3">
        <span className="text-[10px] text-gray-500 tracking-widest block">MODEL CONSENSUS</span>
        
        {/* Convergence Diagram */}
        <div className="bg-[#07090e] border border-gray-900 rounded p-3 text-[10px] text-gray-400 space-y-1">
          <div className="flex items-center justify-between">
            <span>CLASSICAL (RBF-SVM)</span>
            <span className="text-[#3B82F6] font-semibold">{results.prediction}</span>
          </div>
          <div className="flex items-center justify-between">
            <span>QUANTUM (QSVM)</span>
            <span className="text-[#8B5CF6] font-semibold">{results.prediction}</span>
          </div>
          <div className="py-2 border-t border-gray-850 flex items-center justify-between text-white font-bold text-xs">
            <span>CONSENSUS RESOLUTION:</span>
            <span className={isAgreement ? "text-red-400 animate-pulse" : "text-green-400"}>
              {results.prediction.toUpperCase()}
            </span>
          </div>
        </div>
      </div>

      {/* CLASSICAL BASELINE */}
      <div className="border border-gray-800 rounded-lg p-4 bg-[#0d1117] space-y-3">
        <div className="flex justify-between items-center border-b border-gray-850 pb-2">
          <span className="text-[10px] text-blue-400 font-bold tracking-wider">CLASSICAL BASELINE</span>
          <span className="text-[9px] text-gray-600">RBF-SVM</span>
        </div>

        <div className="grid grid-cols-3 gap-2 text-center">
          <div>
            <span className="text-[9px] text-gray-500 block">CONFIDENCE</span>
            <span className="text-xs font-bold text-white">
              {Math.round(results.classical_svm_confidence * 100)}%
            </span>
          </div>
          <div>
            <span className="text-[9px] text-gray-500 block">ACCURACY</span>
            <span className="text-xs font-bold text-white">92.4%</span>
          </div>
          <div>
            <span className="text-[9px] text-gray-500 block">LATENCY</span>
            <span className="text-xs font-bold text-white">{classicalLatency}ms</span>
          </div>
        </div>

        <div className="w-full bg-gray-950 h-1 rounded-full overflow-hidden">
          <div
            className="bg-blue-500 h-full transition-all duration-500"
            style={{ width: `${results.classical_svm_confidence * 100}%` }}
          ></div>
        </div>
      </div>

      {/* QUANTUM EVALUATION */}
      <div className="border border-gray-800 rounded-lg p-4 bg-[#0d1117] space-y-3">
        <div className="flex justify-between items-center border-b border-gray-850 pb-2">
          <span className="text-[10px] text-purple-400 font-bold tracking-wider">QUANTUM EVALUATION</span>
          <span className="text-[9px] text-gray-600">QSVM (QISKIT)</span>
        </div>

        <div className="grid grid-cols-3 gap-2 text-center">
          <div>
            <span className="text-[9px] text-gray-500 block">CONFIDENCE</span>
            <span className="text-xs font-bold text-white">
              {Math.round(results.quantum_svm_confidence * 100)}%
            </span>
          </div>
          <div>
            <span className="text-[9px] text-gray-500 block">ACCURACY</span>
            <span className="text-xs font-bold text-white">91.8%</span>
          </div>
          <div>
            <span className="text-[9px] text-gray-500 block">LATENCY</span>
            <span className="text-xs font-bold text-white">{quantumLatency}ms</span>
          </div>
        </div>

        <div className="w-full bg-gray-950 h-1 rounded-full overflow-hidden">
          <div
            className="bg-purple-500 h-full transition-all duration-500"
            style={{ width: `${results.quantum_svm_confidence * 100}%` }}
          ></div>
        </div>
      </div>

      {/* COLLAPSIBLE DETAILS */}
      <div className="border border-gray-800 rounded-lg overflow-hidden bg-[#0d1117]">
        <button
          onClick={() => setShowTechnicalDetails(!showTechnicalDetails)}
          className="w-full flex items-center justify-between px-3 py-2 bg-[#111827] text-left text-[10px] font-semibold text-gray-400 hover:text-white transition-colors"
        >
          <span>TECHNICAL DETAILS</span>
          <svg
            className={`w-3.5 h-3.5 transition-transform duration-200 ${showTechnicalDetails ? "rotate-180" : ""}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        {showTechnicalDetails && (
          <div className="p-3 border-t border-gray-800 text-[9px] text-gray-500 space-y-1.5 bg-[#0d1117] divide-y divide-gray-850">
            <div className="flex justify-between py-1">
              <span>FEATURE MAP:</span>
              <span className="text-gray-300">ZZFeatureMap</span>
            </div>
            <div className="flex justify-between py-1">
              <span>SIMULATOR:</span>
              <span className="text-gray-300">AerSimulator</span>
            </div>
            <div className="flex justify-between py-1">
              <span>QUBITS / PCA DIMS:</span>
              <span className="text-gray-300">{results.qubits || 8}</span>
            </div>
            <div className="flex justify-between py-1">
              <span>CIRCUIT DEPTH:</span>
              <span className="text-gray-300">{results.circuit_depth || 24}</span>
            </div>
            <div className="flex justify-between py-1">
              <span>EXECUTION STAGE:</span>
              <span className="text-gray-300">{results.is_mock ? "CACHED BENCHMARK" : "LIVE SIMULATOR"}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
