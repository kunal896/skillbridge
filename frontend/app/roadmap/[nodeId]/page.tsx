'use client';
import {useEffect,useState} from 'react';
import {useParams,useRouter} from 'next/navigation';
import {apiClient} from '../../../lib/api-client';
export default function MicroProjectPage(){
 const params=useParams<{nodeId:string}>(); const router=useRouter(); const [code,setCode]=useState(''); const [busy,setBusy]=useState(false); const [msg,setMsg]=useState(''); const [project,setProject]=useState<any|null>(null); const [loading,setLoading]=useState(true);
 useEffect(()=>{
   let cancelled=false;
   apiClient.getRoadmap().then(async roadmap=>{
     const node=roadmap.nodes.find(n=>n.id===params.nodeId);
     if(!node) throw new Error('Roadmap node not found.');
     const p=await apiClient.createMicroProject({roadmapStepId:node.id,skill:node.category,title:node.microProject.title,description:node.description,instructions:node.microProject.instructions?.join(' ')||node.description,rubric:node.microProject.rubricCriteria||[]});
     if(!cancelled) setProject(p);
   }).catch((e:any)=>{if(!cancelled)setMsg(e.message||'Could not prepare micro-project.');}).finally(()=>{if(!cancelled)setLoading(false)});
   return ()=>{cancelled=true};
 },[params.nodeId]);
 async function submit(){setBusy(true);setMsg('');try{const r=await apiClient.submitProject({nodeId:params.nodeId,projectId:project?.id,code});setMsg(`${r.passed?'Passed':'Not passed'} — ${r.score}/100. ${r.feedback}`);}catch(e:any){setMsg(e.message||'Submission failed.')}finally{setBusy(false)}}
 if(loading) return <div className="max-w-3xl mx-auto py-8">Preparing your micro-project…</div>;
 if(msg && !project) return <div className="max-w-3xl mx-auto py-8 space-y-4"><h1 className="text-xl font-bold">Micro-project unavailable</h1><div className="rounded-lg border p-4 text-sm">{msg}</div><button onClick={()=>router.push('/roadmap')} className="px-4 py-2 rounded border">Back to roadmap</button></div>;
 return <div className="max-w-3xl mx-auto py-8 space-y-6">
  <div className="px-3 py-2 rounded-lg bg-green-50 border border-green-100 text-xs text-green-800">
    Demo verification enabled — submission is evaluated with the local demo rubric.
  </div><div><h1 className="text-2xl font-bold">{project?.title||'Micro-project verification'}</h1><p className="text-sm text-gray-600">{project?.description||'Complete the task for this roadmap node and submit your code for sandboxed verification.'}</p>{project?.instructions&&<div className="mt-3 rounded-lg border bg-gray-50 p-4 text-sm">{project.instructions}</div>}</div><textarea className="w-full min-h-[360px] border rounded-lg p-4 font-mono text-sm" value={code} onChange={e=>setCode(e.target.value)} placeholder="# Write Python code here"/><div className="flex gap-3"><button onClick={submit} disabled={busy||!code.trim()||!project} className="px-4 py-2 rounded bg-black text-white disabled:opacity-40">{busy?'Verifying…':'Submit for verification'}</button><button onClick={()=>router.push('/roadmap')} className="px-4 py-2 rounded border">Back</button></div>{msg&&<div className="rounded-lg border p-4 text-sm">{msg}</div>}</div>
}
