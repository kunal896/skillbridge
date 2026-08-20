'use client';

import React from 'react';
import { Loader2 } from 'lucide-react';

export const LoadingState: React.FC<{ message?: string }> = ({ message }) => (
  <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
    <Loader2 className="w-8 h-8 animate-spin mb-3" style={{ color: '#ff9900' }} />
    <p className="text-sm font-medium" style={{ color: '#565959' }}>{message || 'Loading data…'}</p>
  </div>
);
