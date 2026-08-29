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
              <th className="py-2.5 px-4">Exam Desc</th>
              <th className="py-2.5 px-4">Patient</th>
              <th className="py-2.5 px-4 text-center">Age</th>
              <th className="py-2.5 px-4 text-center">Issues</th>
              <th className="py-2.5 px-4 text-center">BI-RADS</th>
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
                <React.Fragment key={study.id}>
                  <tr 
                    className={`hover:bg-gray-850/20 transition-colors cursor-pointer ${expandedStudyId === study.id ? 'bg-[#111827]' : ''}`}
                    onClick={() => setExpandedStudyId(expandedStudyId === study.id ? null : study.id)}
                  >
                    <td className="py-3.5 px-4 text-gray-400">{study.examDesc || study.modality}</td>
                    <td className="py-3.5 px-4 font-bold text-white">{study.patientName}</td>
                    <td className="py-3.5 px-4 text-center text-gray-500">{study.age}</td>
                    <td className="py-3.5 px-4 text-center">
                      {(study.issuesCount || 0) > 0 ? (
                        <span className="inline-flex items-center justify-center w-4 h-4 rounded-full bg-red-950 text-red-400 text-[10px]">
                          {study.issuesCount}
                        </span>
                      ) : (
                        <span className="text-gray-600">-</span>
                      )}
                    </td>
                    <td className="py-3.5 px-4 text-center text-gray-500">{study.birads || "-"}</td>
                  </tr>
                  
                  {/* EXPANDED DETAILS PANEL */}
                  {expandedStudyId === study.id && (
                    <tr className="bg-[#111827] border-b border-gray-800">
                      <td colSpan={5} className="p-4">
                        <div className="bg-[#0d1117] border border-gray-800 rounded-lg p-4 font-mono space-y-4">
                          <div className="grid grid-cols-4 gap-4">
                            <div>
                              <span className="text-gray-500 text-[10px] block">Type:</span>
                              <span className="text-white text-xs">{study.examDesc || study.modality}</span>
                            </div>
                            <div>
                              <span className="text-gray-500 text-[10px] block">Age:</span>
                              <span className="text-white text-xs">{study.age}</span>
                            </div>
                            <div>
                              <span className="text-gray-500 text-[10px] block">Issues:</span>
                              <span className="text-white text-xs">{study.issuesCount || 0}</span>
                            </div>
                            <div>
                              <span className="text-gray-500 text-[10px] block">Med. Doctor:</span>
                              <span className="text-white text-xs">{study.referringPhysician || "N/A"}</span>
                            </div>
                          </div>
                          
                          <div className="grid grid-cols-2 gap-4 border-t border-gray-850 pt-3 mt-3">
                            <div>
                              <span className="text-gray-500 text-[10px] block">Referring Physician:</span>
                              <span className="text-gray-300 text-xs">{study.referringPhysician || "N/A"}</span>
                            </div>
                            <div>
                              <span className="text-gray-500 text-[10px] block">Signs/Symptoms:</span>
                              <span className="text-gray-300 text-xs">Chest pain, dizziness</span>
                            </div>
                            <div>
                              <span className="text-gray-500 text-[10px] block">History:</span>
                              <span className="text-gray-300 text-xs">{study.history || "N/A"}</span>
                            </div>
                            <div className="col-span-2">
                              <span className="text-gray-500 text-[10px] block">Comments:</span>
                              <span className="text-gray-300 text-xs">{study.comments || "N/A"}</span>
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
                              <button className="px-4 py-1.5 border border-gray-700 hover:bg-gray-800 text-gray-300 text-[10px] font-bold rounded transition-colors">
                                Confirm
                              </button>
                              <button className="px-4 py-1.5 border border-gray-700 hover:bg-gray-800 text-gray-300 text-[10px] font-bold rounded transition-colors">
                                Edit
                              </button>
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
