"use client";

import React, { useEffect, useState } from "react";

interface CircuitInfo {
  id: string;
  name: string;
  subtitle: string;
  tag: string;
  qubits: number;
  depth: number;
  hilbert_dim: string;
  description: string;
  ascii: string;
  qasm: string;
}

interface QuantumCircuitViewProps {
  isAnimating: boolean;
  metrics?: {
    qubits: number;
    circuitDepth: number;
    featureMap: string;
  };
}

const DEFAULT_CIRCUITS: Record<string, CircuitInfo> = {
  zz_linear: {
    id: "zz_linear",
    name: "ZZFeatureMap (Linear Entanglement)",
    subtitle: "8 Qubits • Reps=2 • Linear CNOT Chains",
    tag: "STANDARD QML PIPELINE",
    qubits: 8,
    depth: 24,
    hilbert_dim: "2⁸ = 256 Dimensions",
    description: "Applies Hadamard superposition, parameterized Phase rotations P(2θ_i), and pairwise adjacent ZZ entanglement gates (CNOT + Phase + CNOT). Models local anatomical spatial correlations.",
    ascii: `     ┌───┐┌─────────────┐                                                                             
q_0: ┤ H ├┤ P(2.0*x[0]) ├──■──────────────────────────────────────────────────────────────────────────
     ├───┤├─────────────┤┌─┴─┐┌───────────────────┐┌───┐                                             
q_1: ┤ H ├┤ P(2.0*x[1]) ├┤ X ├┤ P(2.0*x[0]*x[1]) ├┤ X ├──■────────────────────────────────────────────
     ├───┤├─────────────┤└───┘└───────────────────┘└───┘┌─┴─┐┌───────────────────┐┌───┐              
q_2: ┤ H ├┤ P(2.0*x[2]) ├───────────────────────────────┤ X ├┤ P(2.0*x[1]*x[2]) ├┤ X ├──■─────────────
     ├───┤├─────────────┤                               └───┘└───────────────────┘└───┘┌─┴─┐┌─────────
q_3: ┤ H ├┤ P(2.0*x[3]) ├──────────────────────────────────────────────────────────────┤ X ├┤ P(2.0*x
     ├───┤├─────────────┤                                                              └───┘└─────────
q_4: ┤ H ├┤ P(2.0*x[4]) ├─────────────────────────────────────────────────────────────────────────────
     ├───┤├─────────────┤                                                                             
q_5: ┤ H ├┤ P(2.0*x[5]) ├─────────────────────────────────────────────────────────────────────────────
     ├───┤├─────────────┤                                                                             
q_6: ┤ H ├┤ P(2.0*x[6]) ├─────────────────────────────────────────────────────────────────────────────
     ├───┤├─────────────┤                                                                             
q_7: ┤ H ├┤ P(2.0*x[7]) ├─────────────────────────────────────────────────────────────────────────────
     └───┘└─────────────┘                                                                             `,
    qasm: `// Qiskit ZZFeatureMap (Linear Entanglement, 8 Qubits)\nOPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[8];\nh q[0];\nh q[1];\nh q[2];\nh q[3];\nh q[4];\nh q[5];\nh q[6];\nh q[7];\ncx q[0],q[1];\nrz(2.0*x[0]*x[1]) q[1];\ncx q[0],q[1];`
  },
  zz_full: {
    id: "zz_full",
    name: "ZZFeatureMap (Full All-to-All Entanglement)",
    subtitle: "4 Qubits • Complete Pairwise Graph • Reps=1",
    tag: "HIGH-EXPRESSIBILITY KERNEL",
    qubits: 4,
    depth: 16,
    hilbert_dim: "2⁴ = 16 Dimensions",
    description: "Entangles every qubit with every other qubit across all N(N-1)/2 pairs. Computes global, non-local cross-correlations across disparate anatomical lobes.",
    ascii: `     ┌───┐┌─────────────┐                                                                             
q_0: ┤ H ├┤ P(2.0*x[0]) ├──■────────────────────────■────────────────────────■────────────────────────
     ├───┤├─────────────┤┌─┴─┐┌───────────────────┐┌───┐└───┘                        │                        
q_1: ┤ H ├┤ P(2.0*x[1]) ├┤ X ├┤ P(2.0*x[0]*x[1]) ├┤ X ├──■───────────────────┼────■───────────────────
     ├───┤├─────────────┤└───┘└───────────────────┘└───┘┌─┴─┐┌───────────────┐│  ┌─┴─┐┌───────────────┐
q_2: ┤ H ├┤ P(2.0*x[2]) ├───────────────────────────────┤ X ├┤ P(2.0*x[0]*x) ├┼──┤ X ├┤ P(2.0*x[1]*x) ├
     ├───┤├─────────────┤                               └───┘└───────────────┘│  └───┘└───────────────┘
q_3: ┤ H ├┤ P(2.0*x[3]) ├─────────────────────────────────────────────────────■────────────────────────
     └───┘└─────────────┘                                                                             `,
    qasm: `// Qiskit ZZFeatureMap (Full Entanglement, 4 Qubits)\nOPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[4];\nh q[0];\nh q[1];\nh q[2];\nh q[3];\ncx q[0],q[1];\ncx q[0],q[2];\ncx q[0],q[3];`
  },
  z_map: {
    id: "z_map",
    name: "ZFeatureMap (Unentangled 1st-Order Baseline)",
    subtitle: "8 Qubits • No Entanglement Gates • Reps=2",
    tag: "ABLATION BASELINE",
    qubits: 8,
    depth: 4,
    hilbert_dim: "Unentangled Product State",
    description: "Contains only single-qubit Hadamard and Phase rotations without two-qubit CNOT gates. Proves that without quantum entanglement, performance reduces to classical linear kernels.",
    ascii: `     ┌───┐┌─────────────┐┌───┐┌─────────────┐
q_0: ┤ H ├┤ P(2.0*x[0]) ├┤ H ├┤ P(2.0*x[0]) ├
     ├───┤├─────────────┤├───┤├─────────────┤
q_1: ┤ H ├┤ P(2.0*x[1]) ├┤ H ├┤ P(2.0*x[1]) ├
     ├───┤├─────────────┤├───┤├─────────────┤
q_2: ┤ H ├┤ P(2.0*x[2]) ├┤ H ├┤ P(2.0*x[2]) ├
     ├───┤├─────────────┤├───┤├─────────────┤
q_3: ┤ H ├┤ P(2.0*x[3]) ├┤ H ├┤ P(2.0*x[3]) ├
     ├───┤├─────────────┤├───┤├─────────────┤
q_4: ┤ H ├┤ P(2.0*x[4]) ├┤ H ├┤ P(2.0*x[4]) ├
     ├───┤├─────────────┤├───┤├─────────────┤
q_5: ┤ H ├┤ P(2.0*x[5]) ├┤ H ├┤ P(2.0*x[5]) ├
     ├───┤├─────────────┤├───┤├─────────────┤
q_6: ┤ H ├┤ P(2.0*x[6]) ├┤ H ├┤ P(2.0*x[6]) ├
     ├───┤├─────────────┤├───┤├─────────────┤
q_7: ┤ H ├┤ P(2.0*x[7]) ├┤ H ├┤ P(2.0*x[7]) ├
     └───┘└─────────────┘└───┘└─────────────┘`,
    qasm: `// Qiskit ZFeatureMap (Unentangled Baseline, 8 Qubits)\nOPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[8];\nh q;\nrz(2.0*x[0]) q[0];\nrz(2.0*x[1]) q[1];`
  },
  ansatz: {
    id: "ansatz",
    name: "RealAmplitudes (Variational VQC Ansatz)",
    subtitle: "8 Qubits • Parameterized Ry Layers • Linear CNOTs",
    tag: "QUANTUM NEURAL NETWORK",
    qubits: 8,
    depth: 14,
    hilbert_dim: "2⁸ = 256 Dimensions",
    description: "Parameterized variational circuit with trainable rotation angles θ_i and circular entanglers, utilized for hybrid quantum neural network backpropagation.",
    ascii: `     ┌──────────┐     ┌──────────┐     ┌──────────┐
q_0: ┤ Ry(θ[0]) ├──■──┤ Ry(θ[8]) ├──■──┤ Ry(θ[16])├
     ├──────────┤┌─┴─┐├──────────┤┌─┴─┐├──────────┤
q_1: ┤ Ry(θ[1]) ├┤ X ├┤ Ry(θ[9]) ├┤ X ├┤ Ry(θ[17])├
     ├──────────┤└───┘├──────────┤└───┘├──────────┤
q_2: ┤ Ry(θ[2]) ├──■──┤ Ry(θ[10])├──■──┤ Ry(θ[18])├
     ├──────────┤┌─┴─┐├──────────┤┌─┴─┐├──────────┤
q_3: ┤ Ry(θ[3]) ├┤ X ├┤ Ry(θ[11])├┤ X ├┤ Ry(θ[19])├
     ├──────────┤└───┘├──────────┤└───┘├──────────┤
q_4: ┤ Ry(θ[4]) ├──■──┤ Ry(θ[12])├──■──┤ Ry(θ[20])├
     ├──────────┤┌─┴─┐├──────────┤┌─┴─┐├──────────┤
q_5: ┤ Ry(θ[5]) ├┤ X ├┤ Ry(θ[13])├┤ X ├┤ Ry(θ[21])├
     ├──────────┤└───┘├──────────┤└───┘├──────────┤
q_6: ┤ Ry(θ[6]) ├──■──┤ Ry(θ[14])├──■──┤ Ry(θ[22])├
     ├──────────┤┌─┴─┐├──────────┤┌─┴─┐├──────────┤
q_7: ┤ Ry(θ[7]) ├┤ X ├┤ Ry(θ[15])├┤ X ├┤ Ry(θ[23])├
     └──────────┘└───┘└──────────┘└───┘└──────────┘`,
    qasm: `// Qiskit RealAmplitudes Variational Ansatz (8 Qubits, reps=2)\nOPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[8];\nry(θ[0]) q[0];\nry(θ[1]) q[1];\ncx q[0],q[1];`
  }
};

export default function QuantumCircuitView({ isAnimating, metrics }: QuantumCircuitViewProps) {
  const [activeTab, setActiveTab] = useState<string>("zz_linear");
  const [circuits, setCircuits] = useState<Record<string, CircuitInfo>>(DEFAULT_CIRCUITS);
  const [showQasm, setShowQasm] = useState<boolean>(false);

  // Fetch circuits from backend
  useEffect(() => {
    fetch("http://localhost:8000/api/v1/quantum/circuit/ascii")
      .then(res => res.json())
      .then(data => {
        if (data.circuits) {
          setCircuits(data.circuits);
        }
      })
      .catch(() => {
        // DEFAULT_CIRCUITS used as fallback
      });
  }, []);

  const cur = circuits[activeTab] || DEFAULT_CIRCUITS["zz_linear"];

  return (
    <div className="border border-gray-800 rounded-xl p-4 bg-[#0a0d14] space-y-4 font-mono shadow-xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-gray-800/80 pb-3 gap-2">
        <div className="flex items-center space-x-2">
          <div className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_8px_#22d3ee]" />
          <span className="text-[11px] text-cyan-300 font-bold tracking-wider uppercase">
            QUANTUM CIRCUIT ARCHITECTURE
          </span>
          <span className="text-[9px] px-2 py-0.5 rounded bg-purple-950/70 border border-purple-500/40 text-purple-300 font-semibold">
            {cur.tag}
          </span>
        </div>
        <div className="flex items-center space-x-2 text-[10px] text-gray-400">
          <span className="text-gray-500">HILBERT SPACE:</span>
          <span className="text-emerald-400 font-bold">{cur.hilbert_dim}</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-1.5 p-1 bg-[#05070a] border border-gray-900 rounded-lg">
        {[
          { id: "zz_linear", label: "ZZ-Linear (Standard)", badge: "8Q" },
          { id: "zz_full", label: "ZZ-Full (All-to-All)", badge: "4Q" },
          { id: "z_map", label: "Z-Map (Baseline)", badge: "8Q" },
          { id: "ansatz", label: "VQC Ansatz (Ry-CX)", badge: "8Q" }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center justify-between px-2.5 py-1.5 rounded text-[10px] font-semibold transition-all ${
              activeTab === tab.id
                ? "bg-gradient-to-r from-purple-900/60 to-cyan-950/60 border border-cyan-500/40 text-cyan-200 shadow-md"
                : "text-gray-400 hover:text-gray-200 hover:bg-white/5 border border-transparent"
            }`}
          >
            <span className="truncate mr-1">{tab.label}</span>
            <span className={`text-[8px] px-1 py-0.2 rounded font-mono ${
              activeTab === tab.id ? "bg-cyan-500/20 text-cyan-300" : "bg-gray-800 text-gray-500"
            }`}>
              {tab.badge}
            </span>
          </button>
        ))}
      </div>

      {/* Description & Circuit Specs Bar */}
      <div className="bg-[#0e131f]/80 border border-gray-850 rounded-lg p-3 space-y-1.5">
        <div className="flex flex-wrap items-center justify-between text-[10px] gap-2">
          <span className="text-white font-bold">{cur.name}</span>
          <div className="flex items-center space-x-3 text-[9px]">
            <span className="text-gray-400">QUBITS: <strong className="text-cyan-400">{cur.qubits}</strong></span>
            <span className="text-gray-600">•</span>
            <span className="text-gray-400">DEPTH: <strong className="text-purple-400">{cur.depth}</strong></span>
            <span className="text-gray-600">•</span>
            <span className="text-gray-400">BACKEND: <strong className="text-emerald-400">StatevectorSampler</strong></span>
          </div>
        </div>
        <p className="text-[10px] text-gray-400 leading-relaxed font-sans">
          {cur.description}
        </p>
      </div>

      {/* Spacious Circuit ASCII Viewport */}
      <div className="relative w-full min-h-[220px] max-h-[360px] bg-[#04060a] border border-cyan-950/50 rounded-xl p-4 overflow-x-auto overflow-y-auto shadow-inner">
        <pre className="text-[11px] sm:text-[12px] text-cyan-200/90 font-mono leading-relaxed tracking-wider select-text">
          {cur.ascii}
        </pre>
      </div>

      {/* Footer Controls & Status */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between text-[9px] text-gray-400 pt-1 gap-2 border-t border-gray-900">
        <div className="flex items-center space-x-2">
          <span className="text-gray-500 font-semibold">STAGE SEQUENCE:</span>
          <span className="text-gray-300 bg-gray-900/90 px-2 py-0.5 rounded border border-gray-800">
            [0] H-GATES → [1-4] ZZ-ENTANGLE → [5] STATEVECTOR PROJECTION
          </span>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setShowQasm(!showQasm)}
            className="text-[9px] px-2.5 py-1 rounded bg-gray-900 hover:bg-gray-800 border border-gray-800 text-gray-300 hover:text-cyan-300 transition-colors"
          >
            {showQasm ? "HIDE OPENQASM" : "VIEW OPENQASM 2.0"}
          </button>
          <div className="flex items-center space-x-1.5">
            <span className={`w-2 h-2 rounded-full ${isAnimating ? "bg-purple-400 animate-ping" : "bg-emerald-400"}`} />
            <span className={isAnimating ? "text-purple-300 font-bold" : "text-emerald-400 font-semibold"}>
              {isAnimating ? "QUANTUM KERNEL SAMPLING..." : "STANDBY (READY)"}
            </span>
          </div>
        </div>
      </div>

      {/* Collapsible QASM Drawer */}
      {showQasm && (
        <div className="mt-3 border-t border-gray-850 pt-3 space-y-1.5 animate-fadeIn">
          <div className="flex items-center justify-between text-[9px] text-gray-500 font-bold uppercase tracking-wider">
            <span>OPENQASM 2.0 KERNEL SOURCE CODE</span>
            <span className="text-gray-600">QISKIT EXPORT</span>
          </div>
          <pre className="bg-[#030508] border border-gray-850 rounded-lg p-3 text-[9px] text-emerald-400/90 overflow-x-auto max-h-[140px] leading-relaxed">
            {cur.qasm}
          </pre>
        </div>
      )}
    </div>
  );
}
