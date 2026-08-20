'use client';

import { useState, useCallback } from 'react';
import { SkillGapDiagnosis } from '../lib/types';
import { apiClient } from '../lib/api-client';

export function useSkillGapDiagnosis() {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [diagnosis, setDiagnosis] = useState<SkillGapDiagnosis | null>(null);

  const runDiagnosis = useCallback(async (payload: {
    targetRole: string;
    resumeText?: string;
    mcqAnswers?: Record<string, string>;
  }) => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiClient.submitDiagnosis(payload);
      setDiagnosis(result);
      return result;
    } catch (err: any) {
      const msg = err?.message || 'Failed to analyze skill gap';
      setError(msg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { loading, error, diagnosis, runDiagnosis };
}
