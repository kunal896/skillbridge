'use client';

import React from 'react';
import Link from 'next/link';
import { useVernacular } from '../hooks/useVernacular';
import { ArrowRight, CheckCircle2, FileCheck, ShieldCheck, Zap, Building2, Compass } from 'lucide-react';

export default function LandingPage() {
  const { t } = useVernacular();

  const features = [
    {
      icon: Compass,
      iconBg: '#fff8ec',
      iconColor: '#ff9900',
      title: t('landing.feature1Title'),
      desc: t('landing.feature1Desc'),
      chip: 'Citation: Job #4821 (TechCorp Logistics)',
      chipColor: '#ff9900',
      chipBg: '#fff8ec',
    },
    {
      icon: FileCheck,
      iconBg: '#edfaf4',
      iconColor: '#007fa3',
      title: t('landing.feature2Title'),
      desc: t('landing.feature2Desc'),
      chip: 'LLM Judge: Rubric Score 92/100',
      chipColor: '#007fa3',
      chipBg: '#edf6fb',
    },
    {
      icon: ShieldCheck,
      iconBg: '#f0f4ff',
      iconColor: '#4a6cf7',
      title: t('landing.feature3Title'),
      desc: t('landing.feature3Desc'),
      chip: 'Hash: 0x8f2a419c83b7…',
      chipColor: '#4a6cf7',
      chipBg: '#f0f4ff',
    },
  ];

  return (
    <div className="space-y-14">
      {/* Hero */}
      <section
        className="rounded-2xl p-8 md:p-14 text-center space-y-6"
        style={{
          background: 'linear-gradient(135deg, #232f3e 0%, #37475a 100%)',
          boxShadow: '0 4px 24px rgba(35,47,62,0.18)',
        }}
      >
        <div
          className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider"
          style={{ backgroundColor: '#ff9900', color: '#111' }}
        >
          <Zap className="w-3.5 h-3.5" />
          AGENTRIX 2026 · Team Unserious
        </div>

        <h1 className="text-3xl md:text-5xl font-extrabold text-white leading-tight tracking-tight">
          {t('landing.heroTitle')}
        </h1>

        <p className="text-base md:text-lg text-gray-300 max-w-2xl mx-auto leading-relaxed">
          {t('landing.heroSubtitle')}
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          <Link
            href="/onboarding"
            className="flex items-center gap-2 px-7 py-3 rounded-lg font-bold text-sm transition-colors"
            style={{ backgroundColor: '#ff9900', color: '#111' }}
          >
            {t('landing.ctaStart')}
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            href="/employer"
            className="flex items-center gap-2 px-7 py-3 rounded-lg font-semibold text-sm border transition-colors"
            style={{ borderColor: 'rgba(255,255,255,0.3)', color: '#fff', backgroundColor: 'rgba(255,255,255,0.07)' }}
          >
            <Building2 className="w-4 h-4" />
            {t('landing.ctaEmployer')}
          </Link>
        </div>
      </section>

      {/* Feature Cards */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {features.map((f, i) => {
          const Icon = f.icon;
          return (
            <div
              key={i}
              className="p-6 rounded-xl space-y-4 border"
              style={{
                backgroundColor: '#ffffff',
                borderColor: '#d5d9d9',
                boxShadow: '0 1px 6px rgba(0,0,0,0.06)',
              }}
            >
              <div className="p-2.5 rounded-lg w-fit" style={{ backgroundColor: f.iconBg }}>
                <Icon className="w-6 h-6" style={{ color: f.iconColor }} />
              </div>
              <h3 className="text-base font-bold" style={{ color: '#0f1111' }}>
                {f.title}
              </h3>
              <p className="text-xs leading-relaxed" style={{ color: '#565959' }}>
                {f.desc}
              </p>
              <span
                className="inline-block px-2.5 py-1 rounded text-[11px] font-mono font-medium"
                style={{ backgroundColor: f.chipBg, color: f.chipColor }}
              >
                {f.chip}
              </span>
            </div>
          );
        })}
      </section>

      {/* How it works strip */}
      <section
        className="rounded-xl p-6 md:p-10 border"
        style={{ backgroundColor: '#fafafa', borderColor: '#d5d9d9' }}
      >
        <h2 className="text-xl font-bold text-center mb-8" style={{ color: '#0f1111' }}>
          How SkillBridge Works
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {[
            { step: '01', title: 'Upload Resume or Take MCQ', desc: 'We diagnose your current skills against active job postings in your target region.' },
            { step: '02', title: 'Get a Cited Skill Roadmap', desc: 'Each node is backed by real job-posting citations — not generic course suggestions.' },
            { step: '03', title: 'Complete Micro-Projects', desc: 'Prove skills through sandboxed code challenges graded by an LLM rubric judge.' },
          ].map((item) => (
            <div key={item.step} className="flex gap-4 items-start">
              <span
                className="text-2xl font-black flex-shrink-0 leading-none"
                style={{ color: '#ff9900' }}
              >
                {item.step}
              </span>
              <div>
                <h4 className="font-bold text-sm mb-1" style={{ color: '#0f1111' }}>{item.title}</h4>
                <p className="text-xs leading-relaxed" style={{ color: '#565959' }}>{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
