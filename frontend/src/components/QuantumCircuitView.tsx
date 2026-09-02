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

const DEFAULT_CIRCUIT_ASCII = `     ┌───┐┌─────────────┐                                                          
q_0: ┤ H ├┤ P(2.0*x[0]) ├──■───────────────────────────────────────────────────────
     ├───┤├─────────────┤┌─┴─┐┌───────────────────┐┌───┐                          
q_1: ┤ H ├┤ P(2.0*x[1]) ├┤ X ├┤ P(2.0*x[0]*x[1]) ├┤ X ├──■─────────────────────────
     ├───┤├─────────────┤└───┘└───────────────────┘└─┬─┘┌─┴─┐┌───────────────────┐
q_2: ┤ H ├┤ P(2.0*x[2]) ├────────────────────────────┼──┤ X ├┤ P(2.0*x[1]*x[2]) ├
     ├───┤├─────────────┤                            │  └───┘└───────────────────┘
q_3: ┤ H ├┤ P(2.0*x[3]) ├────────────────────────────┼─────────────────────────────
     ├───┤├─────────────┤                            │                             
q_4: ┤ H ├┤ P(2.0*x[4]) ├────────────────────────────┼─────────────────────────────
     ├───┤├─────────────┤                            │                             
q_5: ┤ H ├┤ P(2.0*x[5]) ├────────────────────────────┼─────────────────────────────
     ├───┤├─────────────┤                            │                             
q_6: ┤ H ├┤ P(2.0*x[6]) ├────────────────────────────┼─────────────────────────────
     ├───┤├─────────────┤                            │                             
q_7: ┤ H ├┤ P(2.0*x[7]) ├────────────────────────────■─────────────────────────────
     └───┘└─────────────┘                                                          `;

export default function QuantumCircuitView({ isAnimating, metrics }: QuantumCircuitViewProps) {
  const [activeStep, setActiveStep] = useState(-1);
  const [qasm, setQasm] = useState<string | null>(null);
  const [ascii, setAscii] = useState<string>(DEFAULT_CIRCUIT_ASCII);

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

  // Fetch QASM & ASCII from backend
  useEffect(() => {
    fetch("http://localhost:8000/api/v1/quantum/circuit/ascii")
      .then(res => res.json())
      .then(data => {
        if (data.qasm) setQasm(data.qasm);
        if (data.ascii) setAscii(data.ascii);
      })
      .catch(() => {
        // Fallback already set by default
      });
  }, []);


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

      <div className="relative w-full h-[250px] bg-[#07090e] border border-gray-900 rounded p-1 overflow-x-auto overflow-y-auto flex items-start justify-start">
        {ascii ? (
            <pre className="text-[10px] text-gray-400 font-mono leading-none tracking-tighter p-2">
              {ascii}
            </pre>
        ) : (
            <div className="w-full h-full flex items-center justify-center text-[10px] text-gray-500">
                LOADING QISKIT KERNEL...
            </div>
        )}
      </div>

      <div className="flex justify-between text-[8px] text-gray-600 whitespace-nowrap overflow-hidden">
        <span className="truncate mr-2">STAGES: [0] H-GATES → [1-4] ZZ-ENTANGLE → [5] MEASURE</span>
        <span className={isAnimating ? "text-purple-400 animate-pulse font-bold flex-shrink-0" : "flex-shrink-0"}>
          {isAnimating ? "SIMULATING..." : "STANDBY"}
        </span>
      </div>

      {/* RAW QASM EXPORT */}
      {qasm && (
        <div className="mt-4 border-t border-gray-850 pt-3">
          <span className="text-[10px] text-gray-500 font-bold tracking-wider mb-2 block">OPENQASM KERNEL SOURCE</span>
          <pre className="bg-[#07090e] border border-gray-800 rounded p-2 text-[8px] text-gray-400 overflow-x-auto max-h-[100px]">
            {qasm}
          </pre>
        </div>
      )}
    </div>
  );
}
