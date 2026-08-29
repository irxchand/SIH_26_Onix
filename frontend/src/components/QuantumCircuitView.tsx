"use client";

import React, { useEffect, useState } from "react";

interface QuantumCircuitViewProps {
  isAnimating: boolean;
  metrics?: {
    qubits: number;
    circuitDepth: number;
    featureMap: string;
  };
}

export default function QuantumCircuitView({ isAnimating, metrics }: QuantumCircuitViewProps) {
  const [activeStep, setActiveStep] = useState(-1);

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (isAnimating) {
      setActiveStep(0);
      let step = 0;
      timer = setInterval(() => {
        step = (step + 1) % 6;
        setActiveStep(step);
      }, 500);
    } else {
      setActiveStep(-1);
    }
    return () => clearInterval(timer);
  }, [isAnimating]);

  const numQubits = metrics?.qubits || 8;
  const qubits = Array.from({ length: Math.min(numQubits, 8) }, (_, i) => `q${i}`); // Cap visually to 8 for UI layout

  // Coordinate setup for drawing paths
  const stepX = [50, 90, 130, 170, 210, 250];

  return (
    <div className="border border-gray-800 rounded-lg p-3 bg-[#0d1117] space-y-3 font-mono">
      <div className="flex items-center justify-between border-b border-gray-850 pb-2 mb-2">
        <span className="text-[10px] text-purple-400 font-bold tracking-wider">QUANTUM CIRCUIT REGISTER</span>
        <span className="text-[9px] text-gray-500 uppercase">{metrics?.featureMap || 'ZZFEATUREMAP'} / {numQubits} QUBITS</span>
      </div>

      <div className="relative w-full h-[150px] bg-[#07090e] border border-gray-900 rounded p-1 overflow-x-auto flex items-center justify-center">
        <svg className="w-[300px] h-[130px]" viewBox="0 0 300 130">
          {/* Wire channels */}
          {qubits.map((qubit, idx) => {
            const y = 10 + idx * 15;
            return (
              <g key={qubit}>
                <text x="5" y={y + 4} fill="#6B7280" className="text-[8px] font-mono">
                  {qubit}
                </text>
                <line x1="20" y1={y} x2="290" y2={y} stroke="#1F2937" strokeWidth="1" />
              </g>
            );
          })}

          {/* Active scan gate cursor */}
          {isAnimating && activeStep !== -1 && (
            <line
              x1={stepX[activeStep]}
              y1="5"
              x2={stepX[activeStep]}
              y2="125"
              stroke="#8B5CF6"
              strokeWidth="1.5"
              strokeDasharray="2 2"
              className="animate-pulse"
            />
          )}

          {/* Phase 1 Gates: Hadamard gates H */}
          {qubits.map((_, idx) => {
            const y = 10 + idx * 15;
            const isHighlighted = activeStep === 0;
            return (
              <rect
                key={`h-${idx}`}
                x="35"
                y={y - 5}
                width="10"
                height="10"
                fill={isHighlighted ? "#8B5CF6" : "#111827"}
                stroke={isHighlighted ? "#A78BFA" : "#374151"}
                strokeWidth="1"
                className="transition-all duration-300"
              />
            );
          })}

          {/* Entangling CNOT / Rz gates */}
          {/* q0 - q1 connector */}
          <line x1="75" y1="10" x2="75" y2="25" stroke={activeStep === 1 ? "#8B5CF6" : "#374151"} strokeWidth="1" />
          <circle cx="75" cy="10" r="2" fill={activeStep === 1 ? "#A78BFA" : "#6B7280"} />
          <circle cx="75" cy="25" r="3" fill="none" stroke={activeStep === 1 ? "#A78BFA" : "#6B7280"} strokeWidth="1" />

          {/* q2 - q3 connector */}
          <line x1="115" y1="40" x2="115" y2="55" stroke={activeStep === 2 ? "#8B5CF6" : "#374151"} strokeWidth="1" />
          <circle cx="115" cy="40" r="2" fill={activeStep === 2 ? "#A78BFA" : "#6B7280"} />
          <circle cx="115" cy="55" r="3" fill="none" stroke={activeStep === 2 ? "#A78BFA" : "#6B7280"} strokeWidth="1" />

          {/* q4 - q5 connector */}
          <line x1="155" y1="70" x2="155" y2="85" stroke={activeStep === 3 ? "#8B5CF6" : "#374151"} strokeWidth="1" />
          <circle cx="155" cy="70" r="2" fill={activeStep === 3 ? "#A78BFA" : "#6B7280"} />
          <circle cx="155" cy="85" r="3" fill="none" stroke={activeStep === 3 ? "#A78BFA" : "#6B7280"} strokeWidth="1" />

          {/* q6 - q7 connector */}
          <line x1="195" y1="100" x2="195" y2="115" stroke={activeStep === 4 ? "#8B5CF6" : "#374151"} strokeWidth="1" />
          <circle cx="195" cy="100" r="2" fill={activeStep === 4 ? "#A78BFA" : "#6B7280"} />
          <circle cx="195" cy="115" r="3" fill="none" stroke={activeStep === 4 ? "#A78BFA" : "#6B7280"} strokeWidth="1" />

          {/* Final Measurement box gates M */}
          {qubits.map((_, idx) => {
            const y = 10 + idx * 15;
            const isHighlighted = activeStep === 5;
            return (
              <rect
                key={`m-${idx}`}
                x="265"
                y={y - 5}
                width="10"
                height="10"
                fill={isHighlighted ? "#10B981" : "#111827"}
                stroke={isHighlighted ? "#34D399" : "#374151"}
                strokeWidth="1"
                className="transition-all duration-300"
              />
            );
          })}
        </svg>
      </div>

      <div className="flex justify-between text-[8px] text-gray-600">
        <span>STAGES: [0] H-GATES → [1-4] ZZ-ENTANGLING → [5] MEASURE</span>
        <span className={isAnimating ? "text-purple-400 animate-pulse font-bold" : ""}>
          {isAnimating ? "SIMULATING..." : "STANDBY"}
        </span>
      </div>
    </div>
  );
}
