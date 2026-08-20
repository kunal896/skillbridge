'use client';

import React from 'react';
import { useVernacular } from '../../hooks/useVernacular';
import { Languages } from 'lucide-react';
import { SupportedLanguage } from '../../lib/types';

export const VernacularToggle: React.FC = () => {
  const { lang, changeLanguage } = useVernacular();

  return (
    <button
      onClick={() => changeLanguage(lang === 'en' ? 'kn' : ('en' as SupportedLanguage))}
      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-semibold transition-all"
      style={{
        backgroundColor: 'rgba(255,153,0,0.15)',
        border: '1px solid rgba(255,153,0,0.4)',
        color: '#ff9900',
      }}
      title="Toggle Language"
    >
      <Languages className="w-3.5 h-3.5" />
      <span>{lang === 'en' ? 'ಕನ್ನಡ' : 'English'}</span>
    </button>
  );
};
