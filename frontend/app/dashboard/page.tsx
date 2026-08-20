'use client';

import Link from 'next/link';
import { BarChart3, CheckCircle2, Clock3, Sparkles, Target, TrendingUp } from 'lucide-react';

const demand = [
  ['SQL & Analytics', 92],
  ['Python / Pandas', 84],
  ['Excel Automation', 76],
  ['Power BI', 68],
];

export default function Dashboard() {
  return (
    <div className="max-w-6xl mx-auto py-6 space-y-6">
      <div>
        <div className="flex items-center gap-2">
          <h1 className="text-2xl font-bold">Learner dashboard</h1>
          <span className="px-2 py-1 rounded-full text-[10px] font-bold uppercase bg-green-100 text-green-700">Demo profile</span>
        </div>
        <p className="text-sm text-gray-600 mt-1">Your SkillBridge progress, verified skills and current market alignment.</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        {[
          ['Skill alignment', '88%', Target],
          ['Verified skills', '4', CheckCircle2],
          ['Roadmap progress', '62%', TrendingUp],
          ['Projects completed', '3', Sparkles],
        ].map(([label, value, Icon]: any) => (
          <div key={label} className="border rounded-xl bg-white p-5 shadow-sm">
            <Icon className="w-5 h-5 text-orange-500 mb-3" />
            <div className="text-2xl font-black">{value}</div>
            <div className="text-xs text-gray-500 mt-1">{label}</div>
          </div>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-5">
        <div className="border rounded-xl bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="font-bold">Current skill profile</h2>
              <p className="text-xs text-gray-500">Against Data Analyst roles in Karnataka</p>
            </div>
            <span className="text-sm font-black text-orange-500">88%</span>
          </div>
          <div className="space-y-4">
            {demand.map(([name, pct]) => (
              <div key={name}>
                <div className="flex justify-between text-xs font-semibold mb-1.5"><span>{name}</span><span>{pct}%</span></div>
                <div className="h-2 rounded-full bg-gray-100 overflow-hidden">
                  <div className="h-full rounded-full bg-orange-400" style={{ width: `${pct}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="border rounded-xl bg-white p-5 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 className="w-5 h-5 text-orange-500" />
            <div>
              <h2 className="font-bold">Verification history</h2>
              <p className="text-xs text-gray-500">Recent proof-of-skill activity</p>
            </div>
          </div>
          {[
            ['Advanced SQL & Window Functions', '92/100', 'Verified'],
            ['Pandas Data Transformation', '89/100', 'Verified'],
            ['Excel Automation', '87/100', 'Verified'],
          ].map(([title, score, status]) => (
            <div key={title} className="flex items-center justify-between py-3 border-b last:border-0">
              <div>
                <div className="text-sm font-semibold">{title}</div>
                <div className="text-[11px] text-gray-500 flex items-center gap-1"><Clock3 className="w-3 h-3" /> Recently completed</div>
              </div>
              <div className="text-right"><div className="font-bold text-green-700">{score}</div><div className="text-[10px] text-green-700">{status}</div></div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        <Link href="/roadmap" className="px-4 py-2.5 rounded-lg bg-orange-400 font-bold text-sm">Continue skill tree</Link>
        <Link href="/employer" className="px-4 py-2.5 rounded-lg border bg-white font-semibold text-sm">View verified talent</Link>
      </div>
    </div>
  );
}
