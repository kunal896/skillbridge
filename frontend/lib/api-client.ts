import { Roadmap, SkillGapDiagnosis, GradingResult, EmployerMatch, DemandTrend, ProgressLedgerEntry } from './types';
import { MOCK_ROADMAP, MOCK_DIAGNOSIS, MOCK_GRADING_RESULT, MOCK_EMPLOYER_MATCHES, MOCK_DEMAND_TRENDS, MOCK_LEDGER_ENTRIES } from './mock-data';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';
const USE_MOCKS = true; // Demo mode: use deterministic local data so the pitch/demo works without API keys.

class ApiClient {
  constructor(private baseUrl: string) {}
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, { ...options, headers: { 'Content-Type': 'application/json', ...(options.headers || {}) } });
    if (!response.ok) throw new Error(`API error ${response.status}: ${await response.text()}`);
    return response.json() as Promise<T>;
  }
  private authHeaders(): Record<string,string> {
    if (typeof window === 'undefined') return {};
    const token = localStorage.getItem('skillbridge_token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  }
  async register(email:string,password:string,role:'learner'|'employer'='learner') {
    const result = await this.request<{access_token:string;account_id:string;role:string}>('/auth/register',{method:'POST',body:JSON.stringify({email,password,role})});
    if (typeof window!=='undefined') localStorage.setItem('skillbridge_token',result.access_token);
    return result;
  }

  async login(email:string,password:string){
    const body = new URLSearchParams({ username: email, password });
    const result=await this.request<{access_token:string;account_id:string;role:string}>('/auth/login',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:body.toString()});
    if(typeof window!=='undefined'){localStorage.setItem('skillbridge_token',result.access_token);localStorage.setItem('skillbridge_account_id',result.account_id);} return result;
  }
  async submitDiagnosis(payload:{targetRole:string;resumeText?:string;mcqAnswers?:Record<string,string>;learnerId?:string}):Promise<SkillGapDiagnosis> {
    if(USE_MOCKS) return { ...MOCK_DIAGNOSIS, targetRole:payload.targetRole };
    const raw=await this.request<any>('/diagnosis',{method:'POST',headers:this.authHeaders(),body:JSON.stringify({target_role:payload.targetRole,resume_text:payload.resumeText,mcq_answers:payload.mcqAnswers,learner_id:payload.learnerId})});
    if(raw.learner_id && typeof window!=='undefined') localStorage.setItem('skillbridge_learner_id',raw.learner_id);
    return {learnerId:raw.learner_id||'anonymous',targetRole:raw.target_role,currentSkills:(raw.current_skills||[]).map((x:any)=>typeof x==='string'?x:x.name),missingSkills:(raw.skill_gaps||[]).map((x:any)=>typeof x==='string'?x:x.name),matchPercentage:Math.round((raw.confidence||0)*100),summary:raw.diagnosis_summary||'',recommendedFocus:(raw.roadmap||[]).slice(0,6).map((x:any)=>x.skill||x.title)};
  }
  async getRoadmap(learnerId?:string):Promise<Roadmap> {
    learnerId=learnerId||(typeof window!=='undefined'?localStorage.getItem('skillbridge_learner_id')||'':'');
    if(!learnerId) throw new Error('No learner profile found. Complete onboarding first.');
    if(USE_MOCKS) return MOCK_ROADMAP;
    const raw=await this.request<any>(`/roadmaps/learner/${encodeURIComponent(learnerId)}`);
    return mapRoadmap(raw);
  }
  async generateRoadmap(learnerId:string):Promise<Roadmap> {
    if(USE_MOCKS) return MOCK_ROADMAP;
    const raw=await this.request<any>(`/roadmaps/generate?learner_id=${encodeURIComponent(learnerId)}`,{method:'POST',headers:this.authHeaders()});
    return mapRoadmap(raw);
  }
  async createMicroProject(payload:{roadmapStepId:string;skill:string;title:string;description:string;instructions:string;language?:string;difficulty?:string;rubric?:any[];testCases?:any[]}) {
    if(USE_MOCKS) return {id:payload.roadmapStepId,...payload};
    return this.request<any>('/verification/projects',{method:'POST',headers:this.authHeaders(),body:JSON.stringify({
      roadmap_step_id:payload.roadmapStepId,
      skill:payload.skill,
      title:payload.title,
      description:payload.description,
      instructions:payload.instructions,
      language:payload.language||'python',
      difficulty:payload.difficulty||'beginner',
      rubric:payload.rubric||[],
      test_cases:payload.testCases||[],
    })});
  }

  async submitProject(payload:{nodeId:string;code:string;projectId?:string;learnerId?:string}):Promise<GradingResult> {
    if(USE_MOCKS) return {...MOCK_GRADING_RESULT,nodeId:payload.nodeId,timestamp:new Date().toISOString()};
    const raw=await this.request<any>('/verification/submissions',{method:'POST',headers:this.authHeaders(),body:JSON.stringify({node_id:payload.nodeId,project_id:payload.projectId,code:payload.code,language:'python'})});
    return {nodeId:payload.nodeId,passed:raw.status==='pass',score:raw.score,feedback:raw.judge_feedback||raw.llm_feedback||'',rubricBreakdown:[],timestamp:raw.verified_at,ledgerHash:'db:'+raw.id};
  }
  async createEmployerProfile(companyName:string,description:string=''){
    return this.request<any>('/employers/me',{method:'PUT',headers:this.authHeaders(),body:JSON.stringify({company_name:companyName,description})});
  }
  async createEmployerRequirement(roleTitle:string,requiredSkills:string[],region?:string){
    return this.request<any>('/employers/requirements',{method:'POST',headers:this.authHeaders(),body:JSON.stringify({role_title:roleTitle,region,required_skills:requiredSkills.map(skill=>({skill,required_level:'beginner',weight:1})),description:`Hiring for ${roleTitle}`})});
  }
  async getEmployerMatches(employerId?:string):Promise<EmployerMatch[]> { if(USE_MOCKS)return MOCK_EMPLOYER_MATCHES; if(!employerId) throw new Error('Employer profile required.'); const raw=await this.request<any[]>(`/matches/employer/${employerId}`,{headers:this.authHeaders()}); return raw.map((x:any)=>({id:x.id,learnerId:x.learner_id,learnerName:x.learner_id,targetRole:x.role_title,verifiedSkills:x.verified_skills||[],overallMatchScore:Math.round((x.match_score||0)*100),location:'',readinessStatus:(x.match_score||0)>=0.8?'ready':(x.match_score||0)>=0.6?'near_ready':'reskilling',verificationBadgeCount:(x.verified_skills||[]).length,lastActive:x.created_at})); }
  async getDemandTrends(region?:string):Promise<DemandTrend[]> { if(USE_MOCKS)return region&&region!=='all'?MOCK_DEMAND_TRENDS.filter(x=>x.region.toLowerCase().includes(region.toLowerCase())):MOCK_DEMAND_TRENDS; return []; }
  async getLedgerHistory(learnerId:string):Promise<ProgressLedgerEntry[]> { if(USE_MOCKS)return MOCK_LEDGER_ENTRIES; const raw=await this.request<any[]>(`/verification/history`,{headers:this.authHeaders()}); return raw.map(x=>({id:x.id,nodeId:x.project_id,nodeTitle:x.project_id,verifiedAt:x.verified_at,score:x.score,hash:x.id,previousHash:''})); }
}
function mapRoadmap(raw:any):Roadmap {
  return { id:raw.id,targetRole:raw.target_role,learnerId:raw.learner_id,createdAt:raw.created_at,nodes:(raw.steps||[]).map((s:any)=>({id:s.id,title:s.title,description:s.description,category:s.skill,status:s.status==='passed'?'verified':s.status==='in_progress'?'unlocked':s.status==='unlocked'?'unlocked':'locked',prerequisites:[],citation:s.citations?.[0]?{id:s.citations[0].source_id,jobTitle:s.citations[0].title,company:s.citations[0].source_name,location:'',postingUrl:s.citations[0].url,relevanceExcerpt:s.citations[0].snippet||''}:undefined,estimatedHours:4,difficulty:'beginner',microProject:{id:s.id,title:`${s.skill} Micro-project`,description:s.description,instructions:[s.description],rubricCriteria:[]}}))};
}
export const apiClient=new ApiClient(API_BASE_URL);
