import React from 'react';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Navbar } from '../components/shared/Navbar';
import { Footer } from '../components/shared/Footer';
import { ErrorBoundary } from '../components/shared/ErrorBoundary';
import { VernacularProvider } from '../hooks/useVernacular';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'SkillBridge — Cited & Verified Reskilling Platform',
  description:
    'AI-powered workforce reskilling with job-citation backed roadmaps and cryptographic skill verifications.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body
        className={`${inter.className} min-h-screen flex flex-col antialiased`}
        style={{ backgroundColor: '#f2f3f3', color: '#0f1111' }}
      >
        <VernacularProvider>
          <Navbar />
          <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <ErrorBoundary>{children}</ErrorBoundary>
          </main>
          <Footer />
        </VernacularProvider>
      </body>
    </html>
  );
}
