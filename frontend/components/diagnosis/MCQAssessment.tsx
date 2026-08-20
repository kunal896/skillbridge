'use client';

import React, { useState } from 'react';
import { HelpCircle, CheckCircle2, ArrowRight, Loader2 } from 'lucide-react';

interface MCQQuestion {
  id: string;
  question: string;
  options: { key: string; text: string }[];
}

const QUESTIONS: MCQQuestion[] = [
  {
    id: 'q1',
    question: 'How do you currently handle multi-sheet data calculations?',
    options: [
      { key: 'a', text: 'Manually copy-paste values between sheets' },
      { key: 'b', text: 'Use VLOOKUP / XLOOKUP and SUMIFS formulas' },
      { key: 'c', text: 'Write SQL queries and Pandas scripts to join tables' },
    ],
  },
  {
    id: 'q2',
    question: 'What is your experience with databases?',
    options: [
      { key: 'a', text: 'I store data only in CSV or Excel files' },
      { key: 'b', text: 'I can write simple SELECT … WHERE queries' },
      { key: 'c', text: 'I write complex JOINs, GROUP BY, and window functions' },
    ],
  },
  {
    id: 'q3',
    question: 'How do you automate repetitive tasks?',
    options: [
      { key: 'a', text: 'I do them manually every time' },
      { key: 'b', text: 'I use Excel Macros or simple batch scripts' },
      { key: 'c', text: 'I write Python scripts and schedule cron jobs' },
    ],
  },
];

interface MCQAssessmentProps {
  onSubmit: (answers: Record<string, string>, targetRole: string) => void;
  isLoading?: boolean;
}

export const MCQAssessment: React.FC<MCQAssessmentProps> = ({ onSubmit, isLoading = false }) => {
  const [targetRole, setTargetRole] = useState('Data Analyst & Automation Specialist');
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [step, setStep] = useState(0);

  const q = QUESTIONS[step];
  const answered = Boolean(answers[q.id]);

  const handleNext = () => {
    if (step < QUESTIONS.length - 1) setStep((s) => s + 1);
    else onSubmit(answers, targetRole);
  };

  return (
    <div
      className="space-y-6 max-w-2xl mx-auto rounded-xl border p-6 md:p-8"
      style={{ backgroundColor: '#fff', borderColor: '#d5d9d9', boxShadow: '0 1px 6px rgba(0,0,0,0.06)' }}
    >
      {/* Target Role */}
      <div>
        <label className="block text-xs font-bold uppercase tracking-wider mb-1.5" style={{ color: '#565959' }}>
          Target Role
        </label>
        <input
          type="text"
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
          className="w-full px-4 py-2.5 rounded-lg text-sm font-medium outline-none"
          style={{ border: '1px solid #d5d9d9', color: '#0f1111' }}
        />
      </div>

      {/* Progress */}
      <div className="space-y-1">
        <div className="flex justify-between text-xs font-medium" style={{ color: '#565959' }}>
          <span>Question {step + 1} of {QUESTIONS.length}</span>
          <span>{Math.round(((step + 1) / QUESTIONS.length) * 100)}%</span>
        </div>
        <div className="w-full h-1.5 rounded-full" style={{ backgroundColor: '#e9ebed' }}>
          <div
            className="h-full rounded-full transition-all duration-300"
            style={{ width: `${((step + 1) / QUESTIONS.length) * 100}%`, backgroundColor: '#ff9900' }}
          />
        </div>
      </div>

      {/* Question */}
      <div
        className="p-5 rounded-xl space-y-4 border"
        style={{ backgroundColor: '#fafafa', borderColor: '#e9ebed' }}
      >
        <div className="flex items-start gap-3">
          <HelpCircle className="w-5 h-5 mt-0.5 flex-shrink-0" style={{ color: '#ff9900' }} />
          <h3 className="text-base font-semibold" style={{ color: '#0f1111' }}>{q.question}</h3>
        </div>
        <div className="space-y-2">
          {q.options.map((opt) => {
            const selected = answers[q.id] === opt.key;
            return (
              <button
                key={opt.key}
                type="button"
                onClick={() => setAnswers((prev) => ({ ...prev, [q.id]: opt.key }))}
                className="w-full flex items-center justify-between p-4 rounded-lg border text-left text-sm transition-colors"
                style={{
                  borderColor: selected ? '#ff9900' : '#d5d9d9',
                  backgroundColor: selected ? '#fff8ec' : '#fff',
                  color: selected ? '#c45500' : '#0f1111',
                  fontWeight: selected ? 600 : 400,
                }}
              >
                <span>{opt.text}</span>
                {selected && <CheckCircle2 className="w-4 h-4 flex-shrink-0 ml-2" style={{ color: '#ff9900' }} />}
              </button>
            );
          })}
        </div>
      </div>

      {/* Controls */}
      <div className="flex items-center justify-between">
        <button
          type="button"
          onClick={() => setStep((s) => Math.max(0, s - 1))}
          disabled={step === 0 || isLoading}
          className="px-4 py-2 text-xs font-semibold rounded-lg border disabled:opacity-30"
          style={{ borderColor: '#d5d9d9', color: '#565959', backgroundColor: '#fff' }}
        >
          Previous
        </button>
        <button
          type="button"
          onClick={handleNext}
          disabled={!answered || isLoading}
          className="flex items-center gap-2 px-6 py-2.5 rounded-lg font-bold text-xs transition-colors disabled:opacity-40"
          style={{ backgroundColor: '#ff9900', color: '#111' }}
        >
          {isLoading ? (
            <><Loader2 className="w-4 h-4 animate-spin" /><span>Analyzing…</span></>
          ) : step === QUESTIONS.length - 1 ? (
            <><span>Complete Assessment</span><CheckCircle2 className="w-4 h-4" /></>
          ) : (
            <><span>Next Question</span><ArrowRight className="w-4 h-4" /></>
          )}
        </button>
      </div>
    </div>
  );
};
