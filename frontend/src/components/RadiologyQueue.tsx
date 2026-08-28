"use client";

import React, { useState } from "react";
import { Study } from "../types/workstation";

interface RadiologyQueueProps {
  studies: Study[];
  onSelectStudy: (study: Study) => void;
}

export default function RadiologyQueue({ studies, onSelectStudy }: RadiologyQueueProps) {
  const [search, setSearch] = useState("");

  const filtered = studies.filter(
    (s) =>
      s.id.toLowerCase().includes(search.toLowerCase()) ||
      s.patientId.toLowerCase().includes(search.toLowerCase()) ||
      s.patientName.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="w-full border border-gray-800 rounded-lg bg-[#0d1117] overflow-hidden">
      <div className="p-4 border-b border-gray-850 flex items-center justify-between bg-[#111827]">
        <h3 className="text-xs font-bold font-mono tracking-wider text-white">RADIOLOGY SCAN QUEUE</h3>
        <div className="relative">
          <input
            type="text"
            placeholder="Search patient / Study ID..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-[#07090e] border border-gray-800 rounded px-3 py-1 text-xs text-gray-300 placeholder-gray-600 focus:outline-none focus:border-blue-500 w-64"
          />
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-gray-850 bg-[#0c0f16] text-gray-500 text-[10px] tracking-wider uppercase">
              <th className="py-2.5 px-4">Study ID</th>
              <th className="py-2.5 px-4">Patient Info</th>
              <th className="py-2.5 px-4">Modality</th>
              <th className="py-2.5 px-4">Acquisition Time</th>
              <th className="py-2.5 px-4">Pipeline Status</th>
              <th className="py-2.5 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-850 text-gray-300">
            {filtered.map((study) => {
              const statusColors = {
                READY: "text-blue-400 bg-blue-950/20 border border-blue-900/55",
                ANALYZING: "text-yellow-400 bg-yellow-950/20 border border-yellow-900/55 animate-pulse",
                COMPLETE: "text-green-400 bg-green-950/20 border border-green-900/55",
                REVIEW: "text-red-400 bg-red-950/20 border border-red-900/55",
              };

              return (
                <tr key={study.id} className="hover:bg-gray-850/20 transition-colors">
                  <td className="py-3.5 px-4 font-bold text-white">{study.id}</td>
                  <td className="py-3.5 px-4">
                    <div>{study.patientName}</div>
                    <div className="text-[10px] text-gray-500">
                      ID: {study.patientId} / {study.age}y / {study.sex}
                    </div>
                  </td>
                  <td className="py-3.5 px-4 text-gray-400">{study.modality}</td>
                  <td className="py-3.5 px-4 text-gray-500">{study.acquisitionDate}</td>
                  <td className="py-3.5 px-4">
                    <span className={`px-2 py-0.5 rounded text-[10px] ${statusColors[study.status]}`}>
                      {study.status}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={() => onSelectStudy(study)}
                      className="px-2.5 py-1 bg-blue-950/40 hover:bg-blue-900/60 border border-blue-900/50 text-blue-400 font-bold rounded transition-colors text-[10px]"
                    >
                      [ OPEN WORKSPACE ]
                    </button>
                  </td>
                </tr>
              );
            })}
            {filtered.length === 0 && (
              <tr>
                <td colSpan={6} className="text-center py-6 text-gray-600">
                  No matching active records found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
