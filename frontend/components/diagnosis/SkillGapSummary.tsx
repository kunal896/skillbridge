'use client';

import React from 'react';
import Link from 'next/link';
import { SkillGapDiagnosis } from '../../lib/types';
import { CheckCircle2, XCircle, ArrowRight, Target, Sparkles, BookOpen } from 'lucide-react';

interface SkillGapSummaryProps {
  diagnosis: SkillGapDiagnosis;
}

export const SkillGapSummary: React.FC<SkillGapSummaryProps> = ({ diagnosis }) => {
  return (
    <div
      className="space-y-6 max-w-3xl mx-auto rounded-xl border p-6 md:p-8"
      style={{ backgroundColor: '#fff', borderColor: '#d5d9d9', boxShadow: '0 1px 8px rgba(0,0,0,0.07)' }}
    >
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b" style={{ borderColor: '#e9ebed' }}>
        <div>
          <span
            className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold mb-2"
            style={{ backgroundColor: '#fff8ec', color: '#c45500', border: '1px solid #f5c887' }}
          >
            <Target className="w-3.5 h-3.5" />
            Target Role
          </span>
          <h2 className="text-xl font-bold" style={{ color: '#0f1111' }}>{diagnosis.targetRole}</h2>
        </div>
        <div className="text-right">
          <span className="block text-xs font-medium" style={{ color: '#565959' }}>Skill Alignment</span>
          <span className="text-3xl font-black" style={{ color: '#ff9900' }}>{diagnosis.matchPercentage}%</span>
        </div>
      </div>

      {/* Progress bar */}
      <div className="w-full h-2 rounded-full" style={{ backgroundColor: '#e9ebed' }}>
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${diagnosis.matchPercentage}%`, backgroundColor: '#ff9900' }}
        />
      </div>

      {/* Summary */}
      <p className="text-sm leading-relaxed rounded-lg p-4 border" style={{ color: '#565959', borderColor: '#e9ebed', backgroundColor: '#fafafa' }}>
        {diagnosis.summary}
      </p>

      {/* Skills grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 rounded-xl border space-y-3" style={{ borderColor: '#c6f0d4', backgroundColor: '#f0faf4' }}>
          <h3 className="text-xs font-bold uppercase tracking-wider flex items-center gap-1.5" style={{ color: '#067340' }}>
            <CheckCircle2 className="w-4 h-4" />
            Current Skills ({diagnosis.currentSkills.length})
          </h3>
          <div className="flex flex-wrap gap-2">
            {diagnosis.currentSkills.map((skill, i) => (
              <span key={i} className="px-2.5 py-1 rounded text-xs font-medium" style={{ backgroundColor: '#c6f0d4', color: '#067340' }}>
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div className="p-4 rounded-xl border space-y-3" style={{ borderColor: '#fad4b0', backgroundColor: '#fef6ee' }}>
          <h3 className="text-xs font-bold uppercase tracking-wider flex items-center gap-1.5" style={{ color: '#c45500' }}>
            <XCircle className="w-4 h-4" />
            Skill Gaps ({diagnosis.missingSkills.length})
          </h3>
          <div className="flex flex-wrap gap-2">
            {diagnosis.missingSkills.map((skill, i) => (
              <span key={i} className="px-2.5 py-1 rounded text-xs font-medium" style={{ backgroundColor: '#fad4b0', color: '#c45500' }}>
                {skill}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Focus areas */}
      <div className="p-4 rounded-xl border space-y-2" style={{ borderColor: '#b8d5f5', backgroundColor: '#edf3fb' }}>
        <h4 className="text-xs font-bold uppercase tracking-wider flex items-center gap-1.5" style={{ color: '#007fa3' }}>
          <BookOpen className="w-4 h-4" />
          Recommended Focus Areas
        </h4>
        <ul className="list-disc pl-5 space-y-1 text-xs" style={{ color: '#0f1111' }}>
          {diagnosis.recommendedFocus.map((item, i) => <li key={i}>{item}</li>)}
        </ul>
      </div>

      {/* CTA */}
      <Link
        href="/roadmap"
        className="w-full flex items-center justify-center gap-2 py-3 px-6 rounded-lg font-bold text-sm transition-colors"
        style={{ backgroundColor: '#ff9900', color: '#111' }}
      >
        <Sparkles className="w-4 h-4" />
        Generate Cited Skill Tree Roadmap
        <ArrowRight className="w-4 h-4" />
      </Link>
    </div>
  );
};
