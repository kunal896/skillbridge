export type NodeStatus = 'locked' | 'unlocked' | 'verified';

export type SkillDifficulty = 'beginner' | 'intermediate' | 'advanced';

export interface Citation {
  id: string;
  jobTitle: string;
  company: string;
  location: string;
  postingUrl: string;
  relevanceExcerpt: string;
  demandCount?: number;
  postedDate?: string;
}

export interface MicroProject {
  id: string;
  title: string;
  description: string;
  instructions: string[];
  starterCode?: string;
  rubricCriteria: string[];
}

export interface RoadmapNode {
  id: string;
  title: string;
  description: string;
  category: string;
  status: NodeStatus;
  prerequisites: string[]; // Node IDs required to unlock
  citation?: Citation;
  estimatedHours: number;
  difficulty: SkillDifficulty;
  microProject: MicroProject;
}

export interface Roadmap {
  id: string;
  targetRole: string;
  learnerId: string;
  createdAt: string;
  nodes: RoadmapNode[];
}

export interface RubricCriterionResult {
  criterion: string;
  score: number;
  maxScore: number;
  feedback: string;
}

export interface GradingResult {
  nodeId: string;
  passed: boolean;
  score: number; // 0 to 100
  feedback: string;
  rubricBreakdown: RubricCriterionResult[];
  timestamp: string;
  ledgerHash: string; // Tamper-evident verification hash
}

export interface ProgressLedgerEntry {
  id: string;
  nodeId: string;
  nodeTitle: string;
  verifiedAt: string;
  score: number;
  hash: string;
  previousHash: string;
}

export interface EmployerMatch {
  id: string;
  learnerId: string;
  learnerName: string;
  targetRole: string;
  verifiedSkills: string[];
  overallMatchScore: number; // percentage
  location: string;
  readinessStatus: 'ready' | 'reskilling' | 'near_ready';
  verificationBadgeCount: number;
  avatarUrl?: string;
  lastActive: string;
}

export interface DemandTrend {
  skill: string;
  demandCount: number;
  growthPercentage: number;
  region: string;
  freshnessScore: number; // 0-100 indicator of how recently active postings were updated
  topCompanies: string[];
  trendHistory: Array<{ date: string; count: number }>;
}

export interface SkillGapDiagnosis {
  learnerId: string;
  targetRole: string;
  currentSkills: string[];
  missingSkills: string[];
  matchPercentage: number;
  summary: string;
  recommendedFocus: string[];
}

export type SupportedLanguage = 'en' | 'kn';
