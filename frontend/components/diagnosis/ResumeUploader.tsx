'use client';

import React, { useState } from 'react';
import { Upload, FileText, CheckCircle2, ArrowRight, Loader2 } from 'lucide-react';

interface ResumeUploaderProps {
  onSubmit: (data: { targetRole: string; resumeText: string }) => void;
  isLoading?: boolean;
}

export const ResumeUploader: React.FC<ResumeUploaderProps> = ({ onSubmit, isLoading = false }) => {
  const [targetRole, setTargetRole] = useState('Data Analyst & Automation Specialist');
  const [resumeText, setResumeText] = useState('');
  const [fileName, setFileName] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFile = (file: File) => {
    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (e) => setResumeText((e.target?.result as string) || '');
    reader.readAsText(file);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!targetRole.trim()) return;
    onSubmit({ targetRole, resumeText: resumeText || 'Sample resume with SQL and Python basics.' });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-6 max-w-2xl mx-auto rounded-xl border p-6 md:p-8"
      style={{ backgroundColor: '#fff', borderColor: '#d5d9d9', boxShadow: '0 1px 6px rgba(0,0,0,0.06)' }}
    >
      {/* Target Role */}
      <div>
        <label className="block text-xs font-bold uppercase tracking-wider mb-1.5" style={{ color: '#565959' }}>
          1. Target Job Role
        </label>
        <input
          type="text"
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
          placeholder="e.g. Data Analyst & Automation Specialist"
          className="w-full px-4 py-2.5 rounded-lg text-sm font-medium outline-none"
          style={{
            border: '1px solid #d5d9d9',
            color: '#0f1111',
            backgroundColor: '#fff',
          }}
          required
        />
      </div>

      {/* Drop Zone */}
      <div>
        <label className="block text-xs font-bold uppercase tracking-wider mb-1.5" style={{ color: '#565959' }}>
          2. Upload or Paste Resume
        </label>
        <div
          onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
          onDragLeave={() => setDragActive(false)}
          onDrop={(e) => { e.preventDefault(); setDragActive(false); if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]); }}
          className="border-2 border-dashed rounded-xl p-8 text-center transition-colors"
          style={{
            borderColor: dragActive ? '#ff9900' : fileName ? '#007fa3' : '#d5d9d9',
            backgroundColor: dragActive ? '#fff8ec' : fileName ? '#edf6fb' : '#fafafa',
          }}
        >
          <input
            type="file"
            id="resume-upload"
            accept=".pdf,.docx,.txt"
            className="hidden"
            onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
          />
          <label htmlFor="resume-upload" className="cursor-pointer">
            {fileName ? (
              <div className="flex items-center justify-center gap-2 font-semibold text-sm" style={{ color: '#007fa3' }}>
                <CheckCircle2 className="w-5 h-5" />
                <span>{fileName}</span>
              </div>
            ) : (
              <div className="space-y-2">
                <Upload className="w-8 h-8 mx-auto" style={{ color: '#adb1b8' }} />
                <p className="text-sm font-medium" style={{ color: '#0f1111' }}>
                  Drag & drop, or{' '}
                  <span className="underline" style={{ color: '#007fa3' }}>browse files</span>
                </p>
                <p className="text-xs" style={{ color: '#adb1b8' }}>PDF, DOCX, TXT supported</p>
              </div>
            )}
          </label>
        </div>

        <div className="mt-4">
          <div className="flex items-center gap-1.5 mb-1.5">
            <FileText className="w-3.5 h-3.5" style={{ color: '#adb1b8' }} />
            <span className="text-xs font-medium" style={{ color: '#565959' }}>Or paste text directly:</span>
          </div>
          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            rows={4}
            placeholder="Paste your work experience, skills, or project history..."
            className="w-full px-4 py-3 rounded-lg text-xs font-mono outline-none resize-none"
            style={{ border: '1px solid #d5d9d9', color: '#0f1111', backgroundColor: '#fafafa' }}
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading || !targetRole.trim()}
        className="w-full flex items-center justify-center gap-2 py-3 px-6 rounded-lg font-bold text-sm transition-colors disabled:opacity-50"
        style={{ backgroundColor: '#ff9900', color: '#111' }}
      >
        {isLoading ? (
          <><Loader2 className="w-4 h-4 animate-spin" /><span>Analyzing against job postings…</span></>
        ) : (
          <><span>Analyze Skill Gap</span><ArrowRight className="w-4 h-4" /></>
        )}
      </button>
    </form>
  );
};
