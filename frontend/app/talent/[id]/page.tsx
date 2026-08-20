'use client';

import Link from 'next/link';
import { useParams } from 'next/navigation';
import { ArrowLeft, Award, BriefcaseBusiness, CheckCircle2, Download, GraduationCap, Mail, MapPin, Phone, ShieldCheck, Star } from 'lucide-react';

const PROFILES: Record<string, {
  name: string; initials: string; learnerId: string; role: string; location: string; score: number; status: string;
  email: string; phone: string; summary: string; skills: string[]; verified: string[];
  experience: { company: string; role: string; period: string; points: string[] }[];
  education: { school: string; degree: string; period: string };
  projects: { title: string; description: string }[];
}> = {
  'demo-1': {
    name: 'Ananya Rao', initials: 'AR', learnerId: 'usr_20411', role: 'Data Analyst', location: 'Bengaluru, Karnataka', score: 96,
    status: 'Ready to hire', email: 'ananya.rao.demo@skillbridge.local', phone: '+91 90000 20411',
    summary: 'Data Analyst with strong foundations in SQL, Excel, Python and Power BI. Demonstrated ability to turn operational data into clear dashboards and decision-ready insights.',
    skills: ['SQL', 'Excel', 'Python', 'Power BI', 'Data Cleaning', 'Data Visualization'],
    verified: ['SQL', 'Excel', 'Python', 'Power BI'],
    experience: [
      { company: 'Nova Analytics Labs', role: 'Data Analyst Intern', period: 'Jan 2026 – Jun 2026', points: ['Built weekly KPI dashboards in Power BI.', 'Automated spreadsheet reporting with Python and Excel.', 'Wrote SQL queries across sales and customer datasets.'] },
      { company: 'Campus Data Club', role: 'Student Analyst', period: 'Aug 2025 – Dec 2025', points: ['Cleaned survey datasets and created summary reports.', 'Presented data-backed recommendations to project teams.'] },
    ],
    education: { school: 'Bengaluru Institute of Technology', degree: 'B.Tech — Computer Science & Engineering', period: '2024 – 2028' },
    projects: [
      { title: 'Sales Performance Dashboard', description: 'Power BI dashboard tracking revenue, conversion, regional performance and monthly trends.' },
      { title: 'Excel Reporting Automation', description: 'Python + Excel workflow that reduced repetitive weekly reporting tasks.' },
    ],
  },
  'demo-2': {
    name: 'Arjun Mehta', initials: 'AM', learnerId: 'usr_30922', role: 'Data Analyst', location: 'Mysuru, Karnataka', score: 91,
    status: 'Ready to hire', email: 'arjun.mehta.demo@skillbridge.local', phone: '+91 90000 30922',
    summary: 'Analytical learner focused on SQL, Pandas and spreadsheet automation with practical experience building repeatable data workflows.',
    skills: ['Advanced SQL', 'Pandas', 'Excel Automation', 'Python', 'Data Analysis'], verified: ['Advanced SQL', 'Pandas', 'Excel Automation'],
    experience: [{ company: 'InsightWorks', role: 'Data Intern', period: 'Feb 2026 – Jul 2026', points: ['Prepared data extracts using SQL and Pandas.', 'Automated recurring Excel reports and validation checks.'] }],
    education: { school: 'Mysuru College of Engineering', degree: 'B.Tech — Information Science', period: '2024 – 2028' },
    projects: [{ title: 'Inventory Analytics', description: 'SQL and Pandas pipeline for stock, demand and reorder analysis.' }],
  },
  'demo-3': {
    name: 'Meera Nair', initials: 'MN', learnerId: 'usr_10293', role: 'Data Analyst', location: 'Bengaluru, Karnataka', score: 84,
    status: 'Near ready', email: 'meera.nair.demo@skillbridge.local', phone: '+91 90000 10293',
    summary: 'Python-first data learner with practical SQL and visualization experience and a strong foundation in exploratory analysis.',
    skills: ['Python', 'SQL', 'Data Visualization', 'Pandas', 'Statistics'], verified: ['Python', 'SQL', 'Data Visualization'],
    experience: [{ company: 'DataNest', role: 'Analytics Trainee', period: 'Mar 2026 – Jun 2026', points: ['Performed exploratory analysis with Python.', 'Created charts and insight summaries for internal reports.'] }],
    education: { school: 'Bangalore City University', degree: 'B.Sc. — Computer Science', period: '2023 – 2026' },
    projects: [{ title: 'Customer Churn Explorer', description: 'Python notebook exploring customer behavior and churn indicators.' }],
  },
  'demo-4': {
    name: 'Rohit Kulkarni', initials: 'RK', learnerId: 'usr_48107', role: 'Data Analyst', location: 'Hubballi, Karnataka', score: 76,
    status: 'Reskilling', email: 'rohit.kulkarni.demo@skillbridge.local', phone: '+91 90000 48107',
    summary: 'Early-career analyst building practical strength in Excel, SQL and Pandas while completing a structured reskilling roadmap.',
    skills: ['Excel', 'SQL', 'Pandas', 'Reporting', 'Data Cleaning'], verified: ['Excel', 'SQL'],
    experience: [{ company: 'K-Tech Services', role: 'Operations Trainee', period: 'Jul 2025 – Jan 2026', points: ['Maintained spreadsheet-based operational reports.', 'Supported basic SQL data pulls and reconciliation.'] }],
    education: { school: 'KLE Institute of Technology', degree: 'B.E. — Computer Science', period: '2023 – 2027' },
    projects: [{ title: 'Operations Tracker', description: 'Excel reporting template for monitoring tickets, turnaround time and weekly trends.' }],
  },
};

export default function TalentProfilePage() {
  const params = useParams();
  const profile = PROFILES[String(params?.id)] ?? PROFILES['demo-1'];

  return (
    <div className="max-w-5xl mx-auto py-2 sm:py-6 space-y-5">
      <Link href="/employer" className="inline-flex items-center gap-2 text-sm font-semibold text-gray-600 hover:text-orange-600">
        <ArrowLeft className="w-4 h-4" /> Back to matched learners
      </Link>

      <section className="bg-white border rounded-2xl shadow-sm p-6">
        <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-5">
          <div className="flex gap-4">
            <div className="w-16 h-16 rounded-2xl bg-orange-100 text-orange-700 flex items-center justify-center text-xl font-black">{profile.initials}</div>
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h1 className="text-2xl font-black">{profile.name}</h1>
                <span className="px-2 py-1 rounded-full text-[10px] font-bold uppercase bg-green-100 text-green-700 flex items-center gap-1"><ShieldCheck className="w-3 h-3" /> Verified learner</span>
              </div>
              <p className="text-gray-600 mt-1">{profile.role} · {profile.learnerId}</p>
              <p className="text-sm text-gray-500 mt-2"><MapPin className="inline w-3.5 h-3.5 mr-1" />{profile.location}</p>
            </div>
          </div>
          <div className="flex gap-3 items-stretch">
            <div className="rounded-xl bg-orange-50 border border-orange-100 px-5 py-3 text-center min-w-[120px]">
              <div className="text-3xl font-black text-orange-500">{profile.score}%</div>
              <div className="text-[10px] font-bold uppercase text-gray-500">Role match</div>
            </div>
            <button onClick={() => alert('Demo only — resume download is simulated.')} className="rounded-xl border px-4 py-3 text-sm font-bold flex items-center gap-2 hover:bg-gray-50">
              <Download className="w-4 h-4" /> Resume
            </button>
          </div>
        </div>
      </section>

      <div className="grid lg:grid-cols-[1.6fr_1fr] gap-5">
        <div className="space-y-5">
          <section className="bg-white border rounded-2xl shadow-sm p-6">
            <h2 className="font-bold text-lg">Professional summary</h2>
            <p className="text-sm leading-6 text-gray-600 mt-3">{profile.summary}</p>
          </section>

          <section className="bg-white border rounded-2xl shadow-sm p-6">
            <div className="flex items-center gap-2 mb-4"><BriefcaseBusiness className="w-5 h-5 text-orange-500" /><h2 className="font-bold text-lg">Experience</h2></div>
            <div className="space-y-5">
              {profile.experience.map((item) => (
                <div key={item.company} className="border-l-2 border-orange-200 pl-4">
                  <div className="flex flex-wrap justify-between gap-2"><div><h3 className="font-bold">{item.role}</h3><p className="text-sm text-gray-600">{item.company}</p></div><span className="text-xs text-gray-500">{item.period}</span></div>
                  <ul className="mt-2 space-y-1 text-sm text-gray-600">{item.points.map((p) => <li key={p}>• {p}</li>)}</ul>
                </div>
              ))}
            </div>
          </section>

          <section className="bg-white border rounded-2xl shadow-sm p-6">
            <div className="flex items-center gap-2 mb-4"><Award className="w-5 h-5 text-orange-500" /><h2 className="font-bold text-lg">Projects</h2></div>
            <div className="grid md:grid-cols-2 gap-3">{profile.projects.map((p) => <div key={p.title} className="border rounded-xl p-4"><h3 className="font-bold text-sm">{p.title}</h3><p className="text-xs leading-5 text-gray-600 mt-2">{p.description}</p></div>)}</div>
          </section>
        </div>

        <aside className="space-y-5">
          <section className="bg-white border rounded-2xl shadow-sm p-6">
            <h2 className="font-bold text-lg">Verified skills</h2>
            <div className="mt-4 space-y-2">{profile.skills.map((skill) => { const verified = profile.verified.includes(skill); return <div key={skill} className="flex items-center justify-between gap-3 border rounded-lg px-3 py-2.5"><span className="text-sm font-medium">{skill}</span>{verified ? <span className="text-xs font-bold text-green-700 flex items-center gap-1"><CheckCircle2 className="w-3.5 h-3.5" /> Verified</span> : <span className="text-[10px] text-gray-400 font-semibold uppercase">Learning</span>}</div>; })}</div>
          </section>

          <section className="bg-white border rounded-2xl shadow-sm p-6">
            <div className="flex items-center gap-2 mb-4"><GraduationCap className="w-5 h-5 text-orange-500" /><h2 className="font-bold text-lg">Education</h2></div>
            <h3 className="font-semibold text-sm">{profile.education.degree}</h3><p className="text-sm text-gray-600 mt-1">{profile.education.school}</p><p className="text-xs text-gray-500 mt-2">{profile.education.period}</p>
          </section>

          <section className="bg-white border rounded-2xl shadow-sm p-6">
            <h2 className="font-bold text-lg">Contact & availability</h2>
            <div className="mt-4 space-y-3 text-sm"><p><Mail className="inline w-4 h-4 mr-2 text-gray-400" />{profile.email}</p><p><Phone className="inline w-4 h-4 mr-2 text-gray-400" />{profile.phone}</p><p><Star className="inline w-4 h-4 mr-2 text-orange-500" /><span className="font-semibold">{profile.status}</span></p></div>
            <button onClick={() => alert(`Demo outreach sent to ${profile.name}.`)} className="w-full mt-5 rounded-lg bg-black text-white py-2.5 text-sm font-bold">Contact learner</button>
          </section>
        </aside>
      </div>
    </div>
  );
}
