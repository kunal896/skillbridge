'use client';

import React, { useState } from 'react';
import { useSkillGapDiagnosis } from '../../hooks/useSkillGapDiagnosis';
import { ResumeUploader } from '../../components/diagnosis/ResumeUploader';
import { MCQAssessment } from '../../components/diagnosis/MCQAssessment';
import { SkillGapSummary } from '../../components/diagnosis/SkillGapSummary';
import { FileText, CheckSquare } from 'lucide-react';

export default function OnboardingPage() {
  const { loading, diagnosis, runDiagnosis } = useSkillGapDiagnosis();
  const [mode, setMode] = useState<'resume' | 'mcq'>('resume');

  return (
    <div className="space-y-8 py-4">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight" style={{ color: '#0f1111' }}>
          Diagnose Your Skill Gap
        </h1>
        <p className="text-sm" style={{ color: '#565959' }}>
          Upload your resume or answer 3 quick questions to receive a job-market-cited skill roadmap.
        </p>
      </div>

      {/* Mode Tabs */}
      {!diagnosis && (
        <div
          className="flex max-w-md mx-auto p-1 rounded-xl gap-1"
          style={{ backgroundColor: '#e9ebed' }}
        >
          {[
            { key: 'resume', label: 'Upload Resume / CV', icon: FileText },
            { key: 'mcq', label: 'MCQ Assessment', icon: CheckSquare },
          ].map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setMode(key as 'resume' | 'mcq')}
              className="flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg text-xs font-semibold transition-all"
              style={
                mode === key
                  ? { backgroundColor: '#fff', color: '#0f1111', boxShadow: '0 1px 4px rgba(0,0,0,0.12)' }
                  : { backgroundColor: 'transparent', color: '#565959' }
              }
            >
              <Icon className="w-4 h-4" />
              {label}
            </button>
          ))}
        </div>
      )}

      {/* Content */}
      {diagnosis ? (
        <SkillGapSummary diagnosis={diagnosis} />
      ) : mode === 'resume' ? (
        <ResumeUploader onSubmit={(d) => runDiagnosis({ targetRole: d.targetRole, resumeText: d.resumeText })} isLoading={loading} />
      ) : (
        <MCQAssessment onSubmit={(a, r) => runDiagnosis({ targetRole: r, mcqAnswers: a })} isLoading={loading} />
      )}
    </div>
  );
}
