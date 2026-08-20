'use client';

import Link from 'next/link';
import { useState } from 'react';
import { Building2, CheckCircle2, MapPin, Sparkles, Trophy } from 'lucide-react';
import { apiClient } from '../../lib/api-client';

const DEMO_MATCHES = [
  {
    id: 'demo-1',
    learnerName: 'Ananya Rao',
    learnerId: 'usr_20411',
    role: 'Data Analyst',
    score: 96,
    skills: ['SQL', 'Excel', 'Python', 'Power BI'],
    location: 'Bengaluru, Karnataka',
    status: 'Ready to hire',
    badges: 4,
  },
  {
    id: 'demo-2',
    learnerName: 'Arjun Mehta',
    learnerId: 'usr_30922',
    role: 'Data Analyst',
    score: 91,
    skills: ['Advanced SQL', 'Pandas', 'Excel Automation'],
    location: 'Mysuru, Karnataka',
    status: 'Ready to hire',
    badges: 3,
  },
  {
    id: 'demo-3',
    learnerName: 'Meera Nair',
    learnerId: 'usr_10293',
    role: 'Data Analyst',
    score: 84,
    skills: ['Python', 'SQL', 'Data Visualization'],
    location: 'Bengaluru, Karnataka',
    status: 'Near ready',
    badges: 3,
  },
  {
    id: 'demo-4',
    learnerName: 'Rohit Kulkarni',
    learnerId: 'usr_48107',
    role: 'Data Analyst',
    score: 76,
    skills: ['Excel', 'SQL', 'Pandas'],
    location: 'Hubballi, Karnataka',
    status: 'Reskilling',
    badges: 2,
  },
];

export default function EmployerPage() {
  const [company, setCompany] = useState('TechNova Solutions');
  const [role, setRole] = useState('Data Analyst');
  const [skills, setSkills] = useState('SQL, Excel, Python, Power BI');
  const [matches, setMatches] = useState<any[]>(DEMO_MATCHES);
  const [matched, setMatched] = useState(true);

  function runMatch() {
    setMatched(false);
    setTimeout(() => setMatched(true), 350);
    setMatches(
      DEMO_MATCHES.map((m, index) => ({
        ...m,
        score: Math.max(72, m.score - (index === 0 ? 0 : 2)),
      }))
    );
  }

  return (
    <div className="max-w-5xl mx-auto py-6 space-y-6">
      <div>
        <div className="flex items-center gap-2">
          <h1 className="text-2xl font-bold">Verified talent matching</h1>
          <span className="px-2 py-1 rounded-full text-[10px] font-bold uppercase bg-green-100 text-green-700">Demo data</span>
        </div>
        <p className="text-sm text-gray-600 mt-1">
          Create a hiring requirement and rank learners by verified skills, readiness, and role fit.
        </p>
      </div>

      <div className="border rounded-xl bg-white p-5 space-y-4 shadow-sm">
        <div className="flex items-center gap-2 font-semibold">
          <Building2 className="w-4 h-4" /> Hiring requirement
        </div>

        <div className="grid md:grid-cols-2 gap-3">
          <div>
            <label className="text-xs font-semibold text-gray-500">Company</label>
            <input className="w-full border rounded-lg p-2.5 mt-1" value={company} onChange={e => setCompany(e.target.value)} />
          </div>
          <div>
            <label className="text-xs font-semibold text-gray-500">Role</label>
            <input className="w-full border rounded-lg p-2.5 mt-1" value={role} onChange={e => setRole(e.target.value)} />
          </div>
        </div>

        <div>
          <label className="text-xs font-semibold text-gray-500">Required skills</label>
          <input className="w-full border rounded-lg p-2.5 mt-1" value={skills} onChange={e => setSkills(e.target.value)} />
        </div>

        <div className="flex items-center justify-between gap-3">
          <div className="text-xs text-gray-500">
            <Sparkles className="inline w-3.5 h-3.5 mr-1 text-orange-500" />
            Suggested requirement loaded from the demo profile.
          </div>
          <button onClick={runMatch} className="rounded-lg bg-black text-white px-4 py-2.5 text-sm font-semibold">
            {matched ? 'Match learners' : 'Matching…'}
          </button>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <div>
          <h2 className="font-bold">Top matched learners</h2>
          <p className="text-xs text-gray-500">Ranked by verified skills and role alignment</p>
        </div>
        <div className="text-xs font-semibold text-green-700 bg-green-50 px-3 py-1.5 rounded-full">
          {matches.length} candidates found
        </div>
      </div>

      <div className="space-y-3">
        {matches.map((m, index) => (
          <div key={m.id} className="border rounded-xl bg-white p-5 shadow-sm">
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center font-bold text-orange-700">
                  {m.learnerName.split(' ').map((x:string) => x[0]).join('').slice(0,2)}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-bold">{m.learnerName}</h3>
                    {index === 0 && <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-orange-100 text-orange-700 flex items-center gap-1"><Trophy className="w-3 h-3" /> Top match</span>}
                  </div>
                  <p className="text-xs text-gray-500">{m.role} · {m.learnerId}</p>
                  <p className="text-xs text-gray-500 mt-1"><MapPin className="inline w-3 h-3 mr-1" />{m.location}</p>
                </div>
              </div>

              <div className="text-right">
                <div className="text-2xl font-black text-orange-500">{m.score}%</div>
                <div className="text-[10px] text-gray-500 uppercase font-semibold">Match score</div>
              </div>
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
              {m.skills.map((s:string) => (
                <span key={s} className="px-2.5 py-1 rounded-md bg-gray-100 text-xs font-medium">{s}</span>
              ))}
            </div>

            <div className="mt-4 pt-3 border-t flex items-center justify-between text-xs">
              <div className="flex items-center gap-3">
                <span className="text-green-700 font-semibold"><CheckCircle2 className="inline w-3.5 h-3.5 mr-1" />{m.badges} verified skills</span>
                <span className="text-gray-500">{m.status}</span>
              </div>
              <Link href={`/talent/${m.id}`} className="text-orange-600 font-bold hover:text-orange-700">View profile →</Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
