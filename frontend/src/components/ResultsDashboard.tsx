import React from 'react';

export default function ResultsDashboard() {
  const mockedResults = {
    classical: {
      model: "RBF-SVM",
      prediction: "TB Positive",
      confidence: 0.89,
      accuracy: "92.4%",
      inference_time_ms: 15
    },
    quantum: {
      model: "QSVM (ZZFeatureMap, 8 qubits)",
      prediction: "TB Positive",
      confidence: 0.85,
      accuracy: "91.8%",
      inference_time_ms: 1150,
      circuit_depth: 24
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto mt-8">
      <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100 flex items-center">
        <svg className="w-6 h-6 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
        Analysis Results
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Classical Card */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 transform transition duration-300 hover:scale-[1.02]">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200">Classical Baseline</h3>
            <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 text-xs font-bold rounded-full">
              {mockedResults.classical.model}
            </span>
          </div>
          
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Prediction</p>
              <p className="text-xl font-bold text-red-500">{mockedResults.classical.prediction}</p>
            </div>
            
            <div>
              <p className="text-sm flex justify-between text-gray-500 dark:text-gray-400 mb-1">
                <span>Confidence</span>
                <span className="font-semibold text-gray-700 dark:text-gray-200">{Math.round(mockedResults.classical.confidence * 100)}%</span>
              </p>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${mockedResults.classical.confidence * 100}%` }}></div>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-100 dark:border-gray-700">
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Benchmark Acc.</p>
                <p className="font-semibold text-gray-800 dark:text-gray-200">{mockedResults.classical.accuracy}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Inference Time</p>
                <p className="font-semibold text-gray-800 dark:text-gray-200">{mockedResults.classical.inference_time_ms} ms</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quantum Card */}
        <div className="bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 p-6 rounded-2xl shadow-lg border border-indigo-100 dark:border-indigo-800/30 transform transition duration-300 hover:scale-[1.02]">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 flex items-center">
              <svg className="w-5 h-5 mr-2 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
              </svg>
              Quantum Evaluation
            </h3>
            <span className="px-3 py-1 bg-purple-100 dark:bg-purple-900/40 text-purple-700 dark:text-purple-300 text-xs font-bold rounded-full">
              {mockedResults.quantum.model}
            </span>
          </div>
          
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Prediction</p>
              <p className="text-xl font-bold text-red-500">{mockedResults.quantum.prediction}</p>
            </div>
            
            <div>
              <p className="text-sm flex justify-between text-gray-500 dark:text-gray-400 mb-1">
                <span>Confidence</span>
                <span className="font-semibold text-gray-800 dark:text-gray-200">{Math.round(mockedResults.quantum.confidence * 100)}%</span>
              </p>
              <div className="w-full bg-gray-200 dark:bg-gray-700/50 rounded-full h-2">
                <div className="bg-purple-500 h-2 rounded-full" style={{ width: `${mockedResults.quantum.confidence * 100}%` }}></div>
              </div>
            </div>
            
            <div className="grid grid-cols-3 gap-2 pt-4 border-t border-indigo-100 dark:border-indigo-800/30">
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Bench. Acc.</p>
                <p className="font-semibold text-gray-800 dark:text-gray-200">{mockedResults.quantum.accuracy}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Inf. Time</p>
                <p className="font-semibold text-gray-800 dark:text-gray-200">{mockedResults.quantum.inference_time_ms} ms</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Depth</p>
                <p className="font-semibold text-gray-800 dark:text-gray-200">{mockedResults.quantum.circuit_depth}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
