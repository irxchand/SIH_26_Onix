"use client";

import React, { useState } from "react";
import { Study } from "../types/workstation";

interface RadiologyQueueProps {
  studies: Study[];
  onSelectStudy: (study: Study) => void;
}

export default function RadiologyQueue({ studies, onSelectStudy }: RadiologyQueueProps) {
  const [search, setSearch] = useState("");
  const [expandedStudyId, setExpandedStudyId] = useState<string | null>(null);

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
              <th className="py-2.5 px-4">Dataset</th>
              <th className="py-2.5 px-4 text-center">Age / Sex</th>
              <th className="py-2.5 px-4 text-center">True Label</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-850 text-gray-300">
            {filtered.map((study) => {
              return (
                <React.Fragment key={study.id}>
                  <tr 
                    className={`hover:bg-gray-850/20 transition-colors cursor-pointer ${expandedStudyId === study.id ? 'bg-[#111827]' : ''}`}
                    onClick={() => setExpandedStudyId(expandedStudyId === study.id ? null : study.id)}
                  >
                    <td className="py-3.5 px-4 font-bold text-white">{study.id}</td>
                    <td className="py-3.5 px-4 text-gray-400">{study.dataset || "Montgomery County"}</td>
                    <td className="py-3.5 px-4 text-center text-gray-500">{study.age}y / {study.sex}</td>
                    <td className="py-3.5 px-4 text-center">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] ${
                        study.trueLabel === "Tuberculosis" 
                          ? "bg-red-950/40 text-red-400 border border-red-900/50" 
                          : "bg-green-950/40 text-green-400 border border-green-900/50"
                      }`}>
                        {study.trueLabel || "Normal"}
                      </span>
                    </td>
                  </tr>
                  
                  {/* EXPANDED DETAILS PANEL */}
                  {expandedStudyId === study.id && (
                    <tr className="bg-[#111827] border-b border-gray-800">
                      <td colSpan={4} className="p-4">
                        <div className="bg-[#0d1117] border border-gray-800 rounded-lg p-4 font-mono space-y-4">
                          <div className="grid grid-cols-4 gap-4">
                            <div>
                              <span className="text-gray-500 text-[10px] block">Study ID:</span>
                              <span className="text-white text-xs">{study.id}</span>
                            </div>
                            <div>
                              <span className="text-gray-500 text-[10px] block">Dataset Origin:</span>
                              <span className="text-white text-xs">{study.dataset || "Montgomery County"}</span>
                            </div>
                            <div>
                              <span className="text-gray-500 text-[10px] block">True Label:</span>
                              <span className="text-white text-xs">{study.trueLabel || "Normal"}</span>
                            </div>
                            <div>
                              <span className="text-gray-500 text-[10px] block">Age / Sex:</span>
                              <span className="text-white text-xs">{study.age}y / {study.sex}</span>
                            </div>
                          </div>
                          
                          <div className="grid grid-cols-1 gap-4 border-t border-gray-850 pt-3 mt-3">
                            <div>
                              <span className="text-gray-500 text-[10px] block">Clinical Readings & Metadata:</span>
                              <span className="text-gray-300 text-xs italic">{study.comments || "No reading available"}</span>
                            </div>
                          </div>
                          
                          <div className="flex justify-between items-center border-t border-gray-850 pt-3 mt-3">
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                onSelectStudy(study);
                              }}
                              className="px-4 py-1.5 bg-[#40b8c4] hover:bg-[#3496a0] text-black text-[10px] font-bold rounded transition-colors"
                            >
                              Select for analysis
                            </button>
                            <div className="space-x-2">
                              <span className="text-gray-600 text-[10px]">RESEARCH USE ONLY</span>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
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
