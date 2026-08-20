import {
  Roadmap,
  RoadmapNode,
  GradingResult,
  EmployerMatch,
  DemandTrend,
  SkillGapDiagnosis,
  ProgressLedgerEntry,
} from './types';

export const MOCK_DIAGNOSIS: SkillGapDiagnosis = {
  learnerId: 'usr_10293',
  targetRole: 'Data Analyst & Automation Specialist',
  currentSkills: ['Basic Excel', 'Python Fundamentals', 'SQL Queries'],
  missingSkills: ['Advanced Data Transformation (Pandas)', 'Automated ETL Pipelines', 'Dashboarding (PowerBI/Tableau)', 'LLM Integration'],
  matchPercentage: 42,
  summary: 'Strong foundational logic and basic Python skills. Requires targeted upskilling in data transformation pipelines and automated reporting demanded by 84% of current regional job openings.',
  recommendedFocus: [
    'Pandas Data Wrangling & Cleaning',
    'SQL Complex Joins & Window Functions',
    'Automated Workflow Scripts',
  ],
};

export const MOCK_ROADMAP_NODES: RoadmapNode[] = [
  {
    id: 'node_sql_advanced',
    title: 'Advanced SQL & Window Functions',
    description: 'Master analytical queries, aggregations, and window functions for enterprise dataset querying.',
    category: 'Database & Analytics',
    status: 'verified',
    prerequisites: [],
    estimatedHours: 8,
    difficulty: 'intermediate',
    citation: {
      id: 'cit_job_001',
      jobTitle: 'Data Analyst (Mid-Level)',
      company: 'TechCorp Logistics',
      location: 'Bengaluru / Remote',
      postingUrl: 'https://careers.techcorp.example/jobs/4821',
      relevanceExcerpt: 'Requires fluency in complex SQL joins, subqueries, and windowing functions (OVER, PARTITION BY).',
      demandCount: 142,
      postedDate: '2 days ago',
    },
    microProject: {
      id: 'proj_sql_01',
      title: 'Analyze Monthly Active Customer Retention',
      description: 'Write SQL queries using window functions to calculate month-over-month retention metrics on a mock database.',
      instructions: [
        'Use standard PostgreSQL syntax.',
        'Compute rolling 3-month total sales per customer cohort.',
        'Filter out soft-deleted customer accounts.',
      ],
      starterCode: `-- Write your query below
SELECT
  customer_id,
  order_date,
  -- TODO: Calculate rolling retention window
FROM sales_records;`,
      rubricCriteria: [
        'Correct usage of PARTITION BY and ORDER BY in window syntax',
        'Proper handling of NULL values in rolling sums',
        'Query runtime optimization',
      ],
    },
  },
  {
    id: 'node_pandas_wrangling',
    title: 'Pandas Data Transformation',
    description: 'Clean, reshape, and aggregate multi-source datasets with Python Pandas.',
    category: 'Data Engineering',
    status: 'unlocked',
    prerequisites: ['node_sql_advanced'],
    estimatedHours: 12,
    difficulty: 'intermediate',
    citation: {
      id: 'cit_job_002',
      jobTitle: 'Junior Data Engineer',
      company: 'OmniData Solutions',
      location: 'Mysuru / Hybrid',
      postingUrl: 'https://omnidata.example/careers/de-102',
      relevanceExcerpt: 'Must demonstrate ability to automate CSV and API data ingestion pipelines using Python Pandas.',
      demandCount: 98,
      postedDate: '1 day ago',
    },
    microProject: {
      id: 'proj_pandas_01',
      title: 'Automated CSV ETL & Normalization Script',
      description: 'Build a Python function to ingest messy CSV inventory files, handle missing values, and output normalized JSON data.',
      instructions: [
        'Load input_inventory.csv into Pandas DataFrame.',
        'Fill missing prices with category median.',
        'Export result to formatted JSON struct.',
      ],
      starterCode: `import pandas as pd

def process_inventory(file_path: str) -> str:
    # TODO: Load CSV, clean data, return JSON string
    df = pd.read_csv(file_path)
    return df.to_json()`,
      rubricCriteria: [
        'Implements median imputation for missing numeric values',
        'Validates data schema before export',
        'Error handling for corrupted input rows',
      ],
    },
  },
  {
    id: 'node_dashboard_bi',
    title: 'Executive KPI Dashboarding',
    description: 'Design dynamic visual analytics dashboards tailored for business stakeholders.',
    category: 'Business Intelligence',
    status: 'locked',
    prerequisites: ['node_pandas_wrangling'],
    estimatedHours: 10,
    difficulty: 'intermediate',
    citation: {
      id: 'cit_job_003',
      jobTitle: 'Business Intelligence Specialist',
      company: 'Karnataka AgriTech',
      location: 'Hubballi',
      postingUrl: 'https://karnatakaagri.example/jobs/bi-44',
      relevanceExcerpt: 'Candidates must submit verified work showing creation of executive dashboards tracking operational metrics.',
      demandCount: 64,
      postedDate: '3 days ago',
    },
    microProject: {
      id: 'proj_bi_01',
      title: 'Supply Chain Delay Dashboard Spec',
      description: 'Construct a structured layout and data mapping file for a real-time supply chain delay tracker.',
      instructions: [
        'Map raw metrics to chart types (time-series, geo-map, KPI cards).',
        'Define alert thresholds for delay metrics > 15%.',
      ],
      starterCode: `// Dashboard Layout Schema
{
  "title": "Supply Chain Performance",
  "components": []
}`,
      rubricCriteria: [
        'Appropriate selection of visual chart types for time-series data',
        'Clear metric threshold definitions',
        'Stakeholder UX responsiveness',
      ],
    },
  },
  {
    id: 'node_llm_automation',
    title: 'AI Workflow & LLM Integration',
    description: 'Integrate LLMs via APIs into automation pipelines to handle unstructured data summarization.',
    category: 'AI & Automation',
    status: 'locked',
    prerequisites: ['node_pandas_wrangling'],
    estimatedHours: 15,
    difficulty: 'advanced',
    citation: {
      id: 'cit_job_004',
      jobTitle: 'AI Automation Associate',
      company: 'NextGen Services',
      location: 'Bengaluru',
      postingUrl: 'https://nextgenservices.example/careers/ai-assoc',
      relevanceExcerpt: 'Experience integrating LLM APIs for automated document parsing and customer inquiry categorization.',
      demandCount: 115,
      postedDate: '5 hours ago',
    },
    microProject: {
      id: 'proj_llm_01',
      title: 'Structured Customer Review Classifier',
      description: 'Create an automated pipeline that calls an LLM endpoint to classify customer review sentiment and extract actionable tags.',
      instructions: [
        'Construct structured prompt enforcing JSON output format.',
        'Implement retry logic for API rate limits.',
        'Extract key entity tags (product, bug, praise).',
      ],
      starterCode: `async function classifyReview(text: string) {
  // TODO: Call LLM API with structured prompt
  return { sentiment: 'positive', tags: [] };
}`,
      rubricCriteria: [
        'Strict JSON schema validation on LLM output',
        'Prompt robustness against malformed input text',
        'API error fallback mechanism',
      ],
    },
  },
];

export const MOCK_ROADMAP: Roadmap = {
  id: 'map_001',
  targetRole: 'Data Analyst & Automation Specialist',
  learnerId: 'usr_10293',
  createdAt: '2026-08-15T09:30:00Z',
  nodes: MOCK_ROADMAP_NODES,
};

export const MOCK_GRADING_RESULT: GradingResult = {
  nodeId: 'node_sql_advanced',
  passed: true,
  score: 92,
  feedback: 'Excellent work! Your window function correctly partitioned sales cohorts and optimized query execution time.',
  rubricBreakdown: [
    {
      criterion: 'Correct usage of PARTITION BY and ORDER BY syntax',
      score: 30,
      maxScore: 30,
      feedback: 'Flawless partition clause implementation.',
    },
    {
      criterion: 'Proper handling of NULL values in rolling sums',
      score: 27,
      maxScore: 30,
      feedback: 'Handled NULL values gracefully using COALESCE.',
    },
    {
      criterion: 'Query runtime optimization',
      score: 35,
      maxScore: 40,
      feedback: 'Good index utilization, minor query formatting improvement suggested.',
    },
  ],
  timestamp: '2026-08-18T14:22:10Z',
  ledgerHash: '0x8f2a419c83b704e12e10a9bf8e0d4c5421a1900d72f1b40285a66911c4038a',
};

export const MOCK_LEDGER_ENTRIES: ProgressLedgerEntry[] = [
  {
    id: 'ledg_001',
    nodeId: 'node_sql_advanced',
    nodeTitle: 'Advanced SQL & Window Functions',
    verifiedAt: '2026-08-18T14:22:10Z',
    score: 92,
    hash: '0x8f2a419c83b704e12e10a9bf8e0d4c5421a1900d72f1b40285a66911c4038a',
    previousHash: '0x00000000000000000000000000000000000000000000000000000000000000',
  },
];

export const MOCK_EMPLOYER_MATCHES: EmployerMatch[] = [
  {
    id: 'em_match_101',
    learnerId: 'usr_10293',
    learnerName: 'Ramesh Kumar',
    targetRole: 'Data Analyst & Automation Specialist',
    verifiedSkills: ['Advanced SQL', 'Data Normalization', 'Excel Automation'],
    overallMatchScore: 88,
    location: 'Bengaluru, Karnataka',
    readinessStatus: 'ready',
    verificationBadgeCount: 3,
    avatarUrl: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=200',
    lastActive: '10 mins ago',
  },
  {
    id: 'em_match_102',
    learnerId: 'usr_20411',
    learnerName: 'Priya Sharma',
    targetRole: 'Junior Data Engineer',
    verifiedSkills: ['Pandas Data Wrangling', 'SQL Queries', 'Python Scripting'],
    overallMatchScore: 82,
    location: 'Mysuru, Karnataka',
    readinessStatus: 'reskilling',
    verificationBadgeCount: 2,
    avatarUrl: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&q=80&w=200',
    lastActive: '1 hour ago',
  },
  {
    id: 'em_match_103',
    learnerId: 'usr_30922',
    learnerName: 'Anil Gowda',
    targetRole: 'AI Automation Associate',
    verifiedSkills: ['LLM Integration', 'Python API Automation', 'Advanced SQL', 'Pandas'],
    overallMatchScore: 94,
    location: 'Hubballi, Karnataka',
    readinessStatus: 'ready',
    verificationBadgeCount: 4,
    avatarUrl: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=200',
    lastActive: 'Just now',
  },
];

export const MOCK_DEMAND_TRENDS: DemandTrend[] = [
  {
    skill: 'Python Pandas & Data Wrangling',
    demandCount: 1420,
    growthPercentage: 28.4,
    region: 'Karnataka (Overall)',
    freshnessScore: 96,
    topCompanies: ['TechCorp', 'OmniData', 'Infosys', 'Wipro'],
    trendHistory: [
      { date: 'May', count: 980 },
      { date: 'Jun', count: 1100 },
      { date: 'Jul', count: 1250 },
      { date: 'Aug', count: 1420 },
    ],
  },
  {
    skill: 'SQL Window Functions & Aggregations',
    demandCount: 1890,
    growthPercentage: 15.2,
    region: 'Bengaluru Urban',
    freshnessScore: 92,
    topCompanies: ['TCS', 'Accenture', 'Amazon', 'Flipkart'],
    trendHistory: [
      { date: 'May', count: 1600 },
      { date: 'Jun', count: 1710 },
      { date: 'Jul', count: 1780 },
      { date: 'Aug', count: 1890 },
    ],
  },
  {
    skill: 'LLM API Integration & Prompting',
    demandCount: 860,
    growthPercentage: 64.8,
    region: 'Karnataka (Overall)',
    freshnessScore: 99,
    topCompanies: ['NextGen AI', 'Swiggy', 'PhonePe', 'Startup Hub'],
    trendHistory: [
      { date: 'May', count: 310 },
      { date: 'Jun', count: 480 },
      { date: 'Jul', count: 670 },
      { date: 'Aug', count: 860 },
    ],
  },
];
