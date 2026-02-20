'use client';

import { useState, useRef } from 'react';
import { Upload, FileVideo, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { clsx } from 'clsx';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  isLoading: boolean;
}

export default function FileUpload({ onFileSelect, isLoading }: FileUploadProps) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file: File) => {
    if (file.type.startsWith('video/')) {
      setSelectedFile(file);
      onFileSelect(file);
    } else {
      alert("Please upload a video file.");
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    if (inputRef.current) inputRef.current.value = '';
  };

  return (
    <div className="w-full max-w-xl mx-auto mb-8">
      <AnimatePresence mode="wait">
        {!selectedFile ? (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className={clsx(
              "relative border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-all duration-300",
              dragActive 
                ? "border-[var(--primary)] bg-[rgba(0,255,157,0.05)]" 
                : "border-gray-700 hover:border-gray-500 bg-[var(--card)]"
            )}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
          >
            <input
              ref={inputRef}
              className="hidden"
              type="file"
              accept="video/*"
              onChange={handleChange}
              disabled={isLoading}
            />
            
            <div className="flex flex-col items-center gap-4">
              <div className="p-4 rounded-full bg-gray-800">
                <Upload className="w-8 h-8 text-[var(--primary)]" />
              </div>
              <div>
                <p className="text-lg font-medium text-gray-200">
                  Drop video here or click to upload
                </p>
                <p className="text-sm text-gray-400 mt-1">
                  Supports MP4, AVI, MOV
                </p>
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-[var(--card)] border border-gray-700 rounded-xl p-6 flex items-center justify-between shadow-lg"
          >
            <div className="flex items-center gap-4">
              <div className="p-3 bg-gray-800 rounded-lg">
                <FileVideo className="w-6 h-6 text-[var(--secondary)]" />
              </div>
              <div className="overflow-hidden">
                <p className="text-sm font-medium text-gray-200 truncate max-w-[200px]">
                  {selectedFile.name}
                </p>
                <p className="text-xs text-gray-400">
                  {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                </p>
              </div>
            </div>
            
            {!isLoading && (
              <button
                onClick={clearFile}
                className="p-2 hover:bg-gray-800 rounded-full transition-colors text-gray-400 hover:text-red-400"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}


