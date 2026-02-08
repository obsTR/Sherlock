'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Fingerprint, Lock, Cpu } from 'lucide-react';
import FileUpload from '@/components/FileUpload';
import AnalysisResult from '@/components/AnalysisResult';

// Use the local Edge Worker URL (or straight to backend if worker not running)
// For now, let's point to the local Edge Worker as per our architecture
const API_URL = "http://localhost:8787/api/v1/analyze";
const API_KEY = "dev-secret-key"; 

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "X-API-KEY": API_KEY,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Analysis failed. Ensure Edge Worker & Backend are running.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8 md:p-24 relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-[-20%] right-[-10%] w-[500px] h-[500px] bg-blue-900 rounded-full blur-[128px] opacity-20 pointer-events-none" />
      <div className="absolute bottom-[-20%] left-[-10%] w-[500px] h-[500px] bg-green-900 rounded-full blur-[128px] opacity-20 pointer-events-none" />

      <div className="max-w-4xl mx-auto relative z-10">
        {/* Header */}
        <header className="mb-16 text-center space-y-4">
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center justify-center gap-3 mb-6"
          >
            <div className="p-3 bg-[var(--primary)] bg-opacity-10 rounded-xl border border-[var(--primary)] border-opacity-30">
              <Fingerprint className="w-8 h-8 text-[var(--primary)]" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight">
              SHERLOCK <span className="text-gray-600 font-light">AI</span>
            </h1>
          </motion.div>
          
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.1 }}
            className="text-gray-400 text-lg max-w-xl mx-auto"
          >
            Advanced Multi-Modal Deepfake Detection System secured by Edge Computing.
          </motion.p>
        </header>

        {/* Main Interface */}
        <div className="space-y-8">
          <FileUpload onFileSelect={(f) => setFile(f)} isLoading={loading} />

          {/* Action Area */}
          <div className="flex justify-center">
            {file && !loading && !result && (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleAnalyze}
                className="bg-[var(--primary)] text-black px-8 py-3 rounded-full font-bold text-lg shadow-[0_0_20px_rgba(0,255,157,0.4)] flex items-center gap-2 hover:bg-[#33ffb0] transition-colors"
              >
                <Cpu className="w-5 h-5" />
                Analyze Media
              </motion.button>
            )}

            {loading && (
              <div className="text-center space-y-4">
                <div className="relative w-16 h-16 mx-auto">
                  <motion.div 
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
                    className="absolute inset-0 border-4 border-t-[var(--primary)] border-r-transparent border-b-gray-800 border-l-gray-800 rounded-full"
                  />
                </div>
                <p className="text-[var(--primary)] animate-pulse font-mono">
                  SCANNING NEURAL PATTERNS...
                </p>
              </div>
            )}
          </div>

          {/* Error Message */}
          {error && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="bg-red-900/20 border border-red-500/50 p-4 rounded-lg text-red-200 text-center max-w-xl mx-auto"
            >
              <p className="flex items-center justify-center gap-2">
                <Lock className="w-4 h-4" />
                {error}
              </p>
            </motion.div>
          )}

          {/* Result Display */}
          {result && <AnalysisResult result={result} />}
        </div>
      </div>
      
      {/* Footer Status */}
      <footer className="fixed bottom-0 left-0 w-full p-4 border-t border-gray-900 bg-black/80 backdrop-blur-sm text-center">
        <p className="text-xs text-gray-600 font-mono">
          SYSTEM STATUS: <span className="text-[var(--primary)]">OPERATIONAL</span> | EDGE NODE: <span className="text-blue-400">CONNECTED</span> | v1.0.0
        </p>
      </footer>
    </main>
  );
}
