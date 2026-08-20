'use client';

import React from 'react';
import { useSkillGapDiagnosis } from '../../../hooks/useSkillGapDiagnosis';
import { MCQAssessment } from '../../../components/diagnosis/MCQAssessment';
import { SkillGapSummary } from '../../../components/diagnosis/SkillGapSummary';

export default function MCQOnboardingPage() {
  const { loading, diagnosis, runDiagnosis } = useSkillGapDiagnosis();

  const handleMCQSubmit = async (answers: Record<string, string>, targetRole: string) => {
    await runDiagnosis({
      targetRole,
      mcqAnswers: answers,
    });
  };

  return (
    <div className="space-y-6 py-4">
      <div className="text-center max-w-xl mx-auto space-y-1">
        <h1 className="text-2xl font-bold text-slate-100">MCQ Diagnostic Test</h1>
        <p className="text-xs text-slate-400">Answer 3 simple questions to determine your starting skill level.</p>
      </div>

      {diagnosis ? (
        <SkillGapSummary diagnosis={diagnosis} />
      ) : (
        <MCQAssessment onSubmit={handleMCQSubmit} isLoading={loading} />
      )}
    </div>
  );
}
