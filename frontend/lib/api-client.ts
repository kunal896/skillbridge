import {
  Roadmap,
  SkillGapDiagnosis,
  GradingResult,
  EmployerMatch,
  DemandTrend,
  ProgressLedgerEntry,
} from './types';
import {
  MOCK_ROADMAP,
  MOCK_DIAGNOSIS,
  MOCK_GRADING_RESULT,
  MOCK_EMPLOYER_MATCHES,
  MOCK_DEMAND_TRENDS,
  MOCK_LEDGER_ENTRIES,
} from './mock-data';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';
// Default to using mock data unless explicitly configured otherwise
const USE_MOCKS = process.env.NEXT_PUBLIC_USE_MOCKS !== 'false';

// Artificial delay helper to simulate network request when using mocks
const simulateNetworkDelay = (ms = 400) =>
  new Promise((resolve) => setTimeout(resolve, ms));

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    try {
      const response = await fetch(url, { ...options, headers });
      if (!response.ok) {
        throw new Error(`API error ${response.status}: ${response.statusText}`);
      }
      return (await response.json()) as T;
    } catch (error) {
      console.error(`[ApiClient Error] ${options.method || 'GET'} ${endpoint}:`, error);
      throw error;
    }
  }

  /**
   * Fetch a learner's personalized skill tree roadmap.
   */
  async getRoadmap(learnerId: string = 'usr_10293'): Promise<Roadmap> {
    if (USE_MOCKS) {
      await simulateNetworkDelay(300);
      return MOCK_ROADMAP;
    }
    return this.request<Roadmap>(`/roadmap?learnerId=${encodeURIComponent(learnerId)}`);
  }

  /**
   * Submit resume file or MCQ answers for skill gap diagnosis against a target role.
   */
  async submitDiagnosis(payload: {
    targetRole: string;
    resumeText?: string;
    mcqAnswers?: Record<string, string>;
  }): Promise<SkillGapDiagnosis> {
    if (USE_MOCKS) {
      await simulateNetworkDelay(600);
      return {
        ...MOCK_DIAGNOSIS,
        targetRole: payload.targetRole || MOCK_DIAGNOSIS.targetRole,
      };
    }
    return this.request<SkillGapDiagnosis>('/diagnosis', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  /**
   * Submit micro-project code for a specific roadmap node to be evaluated by the LLM-as-judge.
   */
  async submitProject(payload: {
    nodeId: string;
    code: string;
    learnerId?: string;
  }): Promise<GradingResult> {
    if (USE_MOCKS) {
      await simulateNetworkDelay(800);
      // Simulate successful grading result for the submitted node
      return {
        ...MOCK_GRADING_RESULT,
        nodeId: payload.nodeId,
        timestamp: new Date().toISOString(),
      };
    }
    return this.request<GradingResult>('/verification/submit', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  /**
   * Fetch verified learner profile matches for employers.
   */
  async getEmployerMatches(filters?: {
    role?: string;
    location?: string;
    minScore?: number;
  }): Promise<EmployerMatch[]> {
    if (USE_MOCKS) {
      await simulateNetworkDelay(350);
      let results = [...MOCK_EMPLOYER_MATCHES];
      if (filters?.location) {
        results = results.filter((m) =>
          m.location.toLowerCase().includes(filters.location!.toLowerCase())
        );
      }
      if (filters?.minScore) {
        results = results.filter((m) => m.overallMatchScore >= filters.minScore!);
      }
      return results;
    }

    const queryParams = new URLSearchParams();
    if (filters?.role) queryParams.set('role', filters.role);
    if (filters?.location) queryParams.set('location', filters.location);
    if (filters?.minScore) queryParams.set('minScore', filters.minScore.toString());

    return this.request<EmployerMatch[]>(`/employer/matches?${queryParams.toString()}`);
  }

  /**
   * Fetch real-time job demand trends and skill freshness scores.
   */
  async getDemandTrends(region?: string): Promise<DemandTrend[]> {
    if (USE_MOCKS) {
      await simulateNetworkDelay(300);
      if (region && region !== 'all') {
        return MOCK_DEMAND_TRENDS.filter((t) =>
          t.region.toLowerCase().includes(region.toLowerCase())
        );
      }
      return MOCK_DEMAND_TRENDS;
    }
    const endpoint = region ? `/demand/trends?region=${encodeURIComponent(region)}` : '/demand/trends';
    return this.request<DemandTrend[]>(endpoint);
  }

  /**
   * Fetch tamper-evident progress ledger history.
   */
  async getLedgerHistory(learnerId: string = 'usr_10293'): Promise<ProgressLedgerEntry[]> {
    if (USE_MOCKS) {
      await simulateNetworkDelay(200);
      return MOCK_LEDGER_ENTRIES;
    }
    return this.request<ProgressLedgerEntry[]>(`/verification/ledger?learnerId=${encodeURIComponent(learnerId)}`);
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
