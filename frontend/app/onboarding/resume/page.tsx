'use client';

import React from 'react';
import { useSkillGapDiagnosis } from '../../../hooks/useSkillGapDiagnosis';
import { ResumeUploader } from '../../../components/diagnosis/ResumeUploader';
import { SkillGapSummary } from '../../../components/diagnosis/SkillGapSummary';

export default function ResumeOnboardingPage() {
  const { loading, diagnosis, runDiagnosis } = useSkillGapDiagnosis();

  const handleResumeSubmit = async (data: { targetRole: string; resumeText: string }) => {
    await runDiagnosis({
      targetRole: data.targetRole,
      resumeText: data.resumeText,
    });
  };

  return (
    <div className="space-y-6 py-4">
      <div className="text-center max-w-xl mx-auto space-y-1">
        <h1 className="text-2xl font-bold text-slate-100">Resume Skill Analysis</h1>
        <p className="text-xs text-slate-400">Upload or paste your resume to extract baseline skills.</p>
      </div>

      {diagnosis ? (
        <SkillGapSummary diagnosis={diagnosis} />
      ) : (
        <ResumeUploader onSubmit={handleResumeSubmit} isLoading={loading} />
      )}
    </div>
  );
}
