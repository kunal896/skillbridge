'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { CheckCircle2, ShieldCheck } from 'lucide-react';

export default function AuthPage() {
  const [role, setRole] = useState<'learner'|'employer'>('learner');
  const router = useRouter();

  function enterDemo() {
    localStorage.setItem('skillbridge_token', 'demo-token');
    localStorage.setItem('skillbridge_account_id', role === 'learner' ? 'demo-learner-001' : 'demo-employer-001');
    localStorage.setItem('skillbridge_signed_in', 'true');
    localStorage.setItem('skillbridge_learner_id', 'demo-learner-001');
    router.push(role === 'learner' ? '/onboarding' : '/employer');
    
  }

  return (
    <div className="max-w-md mx-auto py-10">
      <div className="border rounded-2xl bg-white p-7 shadow-sm space-y-5">
        <div className="text-center">
          <div className="mx-auto w-12 h-12 rounded-full bg-orange-100 flex items-center justify-center">
            <ShieldCheck className="w-6 h-6 text-orange-500" />
          </div>
          <h1 className="text-2xl font-bold mt-3">SkillBridge demo</h1>
          <p className="text-sm text-gray-500 mt-1">Demo access is enabled for the presentation.</p>
        </div>

        <div>
          <label className="text-xs font-semibold text-gray-500">Continue as</label>
          <select className="w-full border rounded-lg p-3 mt-1" value={role} onChange={e => setRole(e.target.value as any)}>
            <option value="learner">Learner</option>
            <option value="employer">Employer</option>
          </select>
        </div>

        <button onClick={enterDemo} className="w-full rounded-lg bg-black text-white p-3 font-bold">
          Enter demo
        </button>

        <div className="rounded-lg bg-green-50 border border-green-100 p-3 text-xs text-green-800">
          <CheckCircle2 className="inline w-4 h-4 mr-1" />
          No external API key is required in demo mode.
        </div>
      </div>
    </div>
  );
}
