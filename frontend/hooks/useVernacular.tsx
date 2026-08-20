'use client';

import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { SupportedLanguage } from '../lib/types';
import en from '../lib/i18n/en.json';
import kn from '../lib/i18n/kn.json';

const translations: Record<SupportedLanguage, any> = { en, kn };

interface VernacularContextValue {
  lang: SupportedLanguage;
  changeLanguage: (lang: SupportedLanguage) => void;
  t: (keyPath: string) => string;
}

const VernacularContext = createContext<VernacularContextValue | null>(null);

export function VernacularProvider({ children }: { children: React.ReactNode }) {
  const [lang, setLang] = useState<SupportedLanguage>('en');

  useEffect(() => {
    const saved = localStorage.getItem('skillbridge_lang') as SupportedLanguage;
    if (saved === 'en' || saved === 'kn') setLang(saved);
  }, []);

  const changeLanguage = useCallback((newLang: SupportedLanguage) => {
    setLang(newLang);
    localStorage.setItem('skillbridge_lang', newLang);
  }, []);

  const t = useCallback(
    (keyPath: string): string => {
      const keys = keyPath.split('.');
      const resolve = (dict: any) =>
        keys.reduce((cur, k) => (cur && typeof cur === 'object' ? cur[k] : undefined), dict);
      const result = resolve(translations[lang]) ?? resolve(translations.en);
      return typeof result === 'string' ? result : keyPath;
    },
    [lang]
  );

  return (
    <VernacularContext.Provider value={{ lang, changeLanguage, t }}>
      {children}
    </VernacularContext.Provider>
  );
}

export function useVernacular(): VernacularContextValue {
  const ctx = useContext(VernacularContext);
  if (!ctx) throw new Error('useVernacular must be used inside <VernacularProvider>');
  return ctx;
}
