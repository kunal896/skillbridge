'use client';

import React from 'react';
import { useVernacular } from '../../hooks/useVernacular';
import { ShieldCheck, GitFork } from 'lucide-react';

export const Footer: React.FC = () => {
  const { t } = useVernacular();

  return (
    <footer
      style={{ backgroundColor: '#232f3e', borderTop: '1px solid #37475a', color: '#9ca3af' }}
      className="text-xs py-8 px-4 mt-auto"
    >
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <GitFork className="w-4 h-4" style={{ color: '#ff9900' }} />
          <span className="font-semibold text-white">{t('nav.brand')}</span>
          <span className="text-gray-500">— AGENTRIX 2026 Hackathon (Team Unserious)</span>
        </div>
        <div className="flex items-center gap-6 text-gray-400">
          <span className="flex items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5" style={{ color: '#ff9900' }} />
            Verified Job Citations Engine
          </span>
          <span>FastAPI + LangGraph + Vector DB</span>
        </div>
      </div>
    </footer>
  );
};
