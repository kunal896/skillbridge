'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useVernacular } from '../../hooks/useVernacular';
import { VernacularToggle } from './VernacularToggle';
import { LowBandwidthToggle } from './LowBandwidthToggle';
import { GitFork, BarChart3, ShieldCheck, Compass, Network, Menu, X } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { t } = useVernacular();
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  const navLinks = [
    { href: '/',           label: t('nav.home'),        icon: Compass },
    { href: '/onboarding', label: t('nav.onboarding'),  icon: Network },
    { href: '/roadmap',    label: t('nav.roadmap'),     icon: GitFork },
    { href: '/dashboard',  label: t('nav.dashboard'),   icon: BarChart3 },
    { href: '/employer',   label: t('nav.employer'),    icon: ShieldCheck },
  ];

  return (
    <nav
      style={{
        backgroundColor: '#232f3e',
        borderBottom: '3px solid #ff9900',
        position: 'sticky',
        top: 0,
        zIndex: 50,
      }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14">
          {/* Brand */}
          <Link href="/" className="flex items-center gap-2">
            <div className="p-1.5 rounded" style={{ backgroundColor: 'rgba(255,153,0,0.15)' }}>
              <GitFork className="w-5 h-5" style={{ color: '#ff9900' }} />
            </div>
            <span className="font-bold text-white text-base tracking-tight">
              {t('nav.brand')}
            </span>
            <span
              className="hidden sm:inline-block px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded"
              style={{ backgroundColor: '#ff9900', color: '#111' }}
            >
              AGENTRIX '26
            </span>
          </Link>

          {/* Desktop Links */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map(({ href, label, icon: Icon }) => {
              const active = pathname === href;
              return (
                <Link
                  key={href}
                  href={href}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded text-sm font-medium transition-colors"
                  style={{
                    color: active ? '#ff9900' : '#d5d9d9',
                    backgroundColor: active ? 'rgba(255,153,0,0.1)' : 'transparent',
                  }}
                  onMouseEnter={(e) => {
                    if (!active) (e.currentTarget as HTMLElement).style.color = '#ffffff';
                  }}
                  onMouseLeave={(e) => {
                    if (!active) (e.currentTarget as HTMLElement).style.color = '#d5d9d9';
                  }}
                >
                  <Icon className="w-4 h-4" />
                  <span>{label}</span>
                </Link>
              );
            })}
          </div>

          {/* Toggles */}
          <div className="hidden sm:flex items-center gap-2">
            <LowBandwidthToggle />
            <VernacularToggle />
          </div>

          {/* Mobile burger */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="sm:hidden p-2 rounded text-gray-300 hover:text-white"
          >
            {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileOpen && (
        <div style={{ backgroundColor: '#37475a', borderTop: '1px solid #4a5568' }} className="sm:hidden px-4 pt-3 pb-4 space-y-1">
          <div className="flex gap-2 pb-3 border-b border-gray-600 mb-2">
            <LowBandwidthToggle />
            <VernacularToggle />
          </div>
          {navLinks.map(({ href, label, icon: Icon }) => {
            const active = pathname === href;
            return (
              <Link
                key={href}
                href={href}
                onClick={() => setMobileOpen(false)}
                className="flex items-center gap-3 px-3 py-2.5 rounded text-sm font-medium"
                style={{
                  color: active ? '#ff9900' : '#d5d9d9',
                  backgroundColor: active ? 'rgba(255,153,0,0.1)' : 'transparent',
                }}
              >
                <Icon className="w-5 h-5" />
                <span>{label}</span>
              </Link>
            );
          })}
        </div>
      )}
    </nav>
  );
};
