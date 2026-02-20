'use client';

import { motion } from 'framer-motion';
import { ShieldCheck, ShieldAlert, Activity, Volume2, Eye } from 'lucide-react';
import { clsx } from 'clsx';

interface AnalysisDetails {
  visual_prob?: number;
  audio_prob?: number | null;
  frames_analyzed: number;
}

interface AnalysisResultProps {
  result: {
    is_fake: boolean;
    confidence: number;
    fake_probability: number;
    details: AnalysisDetails;
  };
}

export default function AnalysisResult({ result }: AnalysisResultProps) {
  const isFake = result.is_fake;
  const percentage = Math.round(result.fake_probability * 100);
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-2xl mx-auto space-y-6"
    >
      {/* Main Verdict Card */}
      <div className={clsx(
        "relative overflow-hidden rounded-2xl p-8 text-center border-2 shadow-2xl transition-all",
        isFake 
          ? "border-[var(--danger)] bg-[rgba(255,0,85,0.05)] shadow-[0_0_30px_rgba(255,0,85,0.2)]"
          : "border-[var(--primary)] bg-[rgba(0,255,157,0.05)] shadow-[0_0_30px_rgba(0,255,157,0.2)]"
      )}>
        <div className="relative z-10 flex flex-col items-center gap-4">
          {isFake ? (
            <ShieldAlert className="w-20 h-20 text-[var(--danger)] drop-shadow-[0_0_10px_rgba(255,0,85,0.8)]" />
          ) : (
            <ShieldCheck className="w-20 h-20 text-[var(--primary)] drop-shadow-[0_0_10px_rgba(0,255,157,0.8)]" />
          )}
          
          <div>
            <h2 className={clsx(
              "text-4xl font-bold tracking-tighter mb-2",
              isFake ? "text-[var(--danger)]" : "text-[var(--primary)]"
            )}>
              {isFake ? "DEEPFAKE DETECTED" : "AUTHENTIC MEDIA"}
            </h2>
            <p className="text-gray-400 text-lg uppercase tracking-widest">
              Confidence Score
            </p>
          </div>

          <div className="flex items-end gap-2 mt-2">
            <span className="text-6xl font-black text-white">
              {percentage}%
            </span>
            <span className="text-xl text-gray-500 mb-2 font-mono">
              / 100%
            </span>
          </div>
        </div>
        
        {/* Background Gradient */}
        <div className={clsx(
          "absolute top-0 left-0 w-full h-full opacity-10 blur-3xl",
          isFake ? "bg-[var(--danger)]" : "bg-[var(--primary)]"
        )} />
      </div>

      {/* Detailed Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Visual Analysis */}
        <div className="bg-[var(--card)] border border-gray-800 p-5 rounded-xl flex items-center gap-4">
          <div className="p-3 bg-gray-900 rounded-lg">
            <Eye className="w-6 h-6 text-blue-400" />
          </div>
          <div className="flex-1">
            <p className="text-xs text-gray-400 uppercase tracking-wider">Visual Probability</p>
            <div className="w-full bg-gray-800 h-2 mt-2 rounded-full overflow-hidden">
              <div 
                className="h-full bg-blue-500 rounded-full transition-all duration-1000"
                style={{ width: `${(result.details.visual_prob || 0) * 100}%` }}
              />
            </div>
          </div>
          <span className="text-lg font-mono font-bold text-blue-400">
            {Math.round((result.details.visual_prob || 0) * 100)}%
          </span>
        </div>

        {/* Audio Analysis */}
        <div className="bg-[var(--card)] border border-gray-800 p-5 rounded-xl flex items-center gap-4">
          <div className="p-3 bg-gray-900 rounded-lg">
            <Volume2 className="w-6 h-6 text-purple-400" />
          </div>
          <div className="flex-1">
            <p className="text-xs text-gray-400 uppercase tracking-wider">Audio Probability</p>
            {result.details.audio_prob !== null ? (
              <div className="w-full bg-gray-800 h-2 mt-2 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-purple-500 rounded-full transition-all duration-1000"
                  style={{ width: `${(result.details.audio_prob || 0) * 100}%` }}
                />
              </div>
            ) : (
              <p className="text-xs text-gray-600 mt-1 italic">Not Available</p>
            )}
          </div>
          <span className="text-lg font-mono font-bold text-purple-400">
            {result.details.audio_prob !== null 
              ? `${Math.round(result.details.audio_prob * 100)}%`
              : "N/A"}
          </span>
        </div>
      </div>

      <div className="text-center">
        <p className="text-xs text-gray-600 flex items-center justify-center gap-2">
          <Activity className="w-3 h-3" />
          Analyzed {result.details.frames_analyzed} frames across visual and audio spectrums.
        </p>
      </div>
    </motion.div>
  );
}


