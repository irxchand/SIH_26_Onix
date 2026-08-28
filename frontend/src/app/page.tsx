import UploadWidget from '@/components/UploadWidget';
import ResultsDashboard from '@/components/ResultsDashboard';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-12">
        
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 tracking-tight">
            Anatomy-Grounded Hybrid Quantum AI
          </h1>
          <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Early Disease Detection Platform — TB Demonstrator (SIH26139)
          </p>
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-200 text-sm font-medium border border-yellow-200 dark:border-yellow-800/50">
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            Research demonstration only. Not a clinical diagnosis.
          </div>
        </div>

        {/* Upload Section */}
        <div className="flex justify-center">
          <UploadWidget />
        </div>

        {/* Results Section */}
        <ResultsDashboard />
        
        {/* Footer info */}
        <div className="mt-16 text-center text-sm text-gray-500 dark:text-gray-400">
          <p>Powered by Next.js, FastAPI, Scikit-Learn, and Qiskit.</p>
        </div>
      </div>
    </main>
  );
}
