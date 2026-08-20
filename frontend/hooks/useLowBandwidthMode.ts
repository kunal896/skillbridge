'use client';

import { useState, useEffect, useCallback } from 'react';

export function useLowBandwidthMode() {
  const [isLowBandwidth, setIsLowBandwidth] = useState<boolean>(false);

  useEffect(() => {
    const saved = localStorage.getItem('skillbridge_low_bandwidth');
    if (saved !== null) {
      const active = saved === 'true';
      setIsLowBandwidth(active);
      if (active) {
        document.documentElement.classList.add('low-bandwidth');
      } else {
        document.documentElement.classList.remove('low-bandwidth');
      }
    }
  }, []);

  const toggleLowBandwidth = useCallback(() => {
    setIsLowBandwidth((prev) => {
      const next = !prev;
      localStorage.setItem('skillbridge_low_bandwidth', String(next));
      if (next) {
        document.documentElement.classList.add('low-bandwidth');
      } else {
        document.documentElement.classList.remove('low-bandwidth');
      }
      return next;
    });
  }, []);

  return { isLowBandwidth, toggleLowBandwidth };
}
