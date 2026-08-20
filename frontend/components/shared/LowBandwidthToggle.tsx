'use client';

import React from 'react';
import { useLowBandwidthMode } from '../../hooks/useLowBandwidthMode';
import { Zap, ZapOff } from 'lucide-react';

export const LowBandwidthToggle: React.FC = () => {
  const { isLowBandwidth, toggleLowBandwidth } = useLowBandwidthMode();

  return (
    <button
      onClick={toggleLowBandwidth}
      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-semibold transition-all"
      style={
        isLowBandwidth
          ? { backgroundColor: 'rgba(234,179,8,0.15)', border: '1px solid rgba(234,179,8,0.4)', color: '#ca8a04' }
          : { backgroundColor: 'rgba(255,255,255,0.08)', border: '1px solid rgba(255,255,255,0.2)', color: '#9ca3af' }
      }
      title="Toggle Low Bandwidth Mode"
    >
      {isLowBandwidth ? (
        <><ZapOff className="w-3.5 h-3.5" /><span>Low Data ON</span></>
      ) : (
        <><Zap className="w-3.5 h-3.5" /><span>Low Data</span></>
      )}
    </button>
  );
};
