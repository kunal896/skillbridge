'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { apiClient } from '../../lib/api-client';
import { Roadmap, RoadmapNode } from '../../lib/types';
import { LoadingState } from '../../components/shared/LoadingState';
import { EmptyState } from '../../components/shared/EmptyState';
import {
  CheckCircle2,
  Lock,
  PlayCircle,
  ExternalLink,
  Clock,
  ArrowRight,
} from 'lucide-react';

const STATUS_STYLES: Record<
  RoadmapNode['status'],
  { badge: string; badgeText: string; border: string; icon: React.ReactNode }
> = {
  verified: {
    badge: '#c6f0d4',
    badgeText: '#067340',
    border: '#c6f0d4',
    icon: <CheckCircle2 className="w-4 h-4" />,
  },
  unlocked: {
    badge: '#fff8ec',
    badgeText: '#c45500',
    border: '#f5c887',
    icon: <PlayCircle className="w-4 h-4" />,
  },
  locked: {
    badge: '#e9ebed',
    badgeText: '#565959',
    border: '#d5d9d9',
    icon: <Lock className="w-4 h-4" />,
  },
};

export default function RoadmapPage() {
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    apiClient
      .getRoadmap()
      .then((data) => {
        if (!cancelled) setRoadmap(data);
      })
      .catch((err: any) => {
        if (!cancelled) setError(err?.message || 'Failed to load your roadmap.');
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return <LoadingState message="Building your cited skill roadmap…" />;
  }

  if (error) {
    return (
      <EmptyState
        title="Couldn't load your roadmap"
        description={error}
        actionLabel="Start over"
        onAction={() => (window.location.href = '/onboarding')}
      />
    );
  }

  if (!roadmap || roadmap.nodes.length === 0) {
    return (
      <EmptyState
        title="No roadmap yet"
        description="Complete the skill gap diagnosis first to generate a cited roadmap."
        actionLabel="Start diagnosis"
        onAction={() => (window.location.href = '/onboarding')}
      />
    );
  }

  return (
    <div className="space-y-8 py-4">
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <span
          className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold"
          style={{ backgroundColor: '#fff8ec', color: '#c45500', border: '1px solid #f5c887' }}
        >
          Cited Skill Roadmap
        </span>
        <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight" style={{ color: '#0f1111' }}>
          {roadmap.targetRole}
        </h1>
        <p className="text-sm" style={{ color: '#565959' }}>
          Every step below is grounded in retrieved job-market evidence — not a generic course list.
        </p>
      </div>

      <div className="max-w-3xl mx-auto space-y-4">
        {roadmap.nodes.map((node, i) => {
          const style = STATUS_STYLES[node.status];
          const isLast = i === roadmap.nodes.length - 1;
          return (
            <div key={node.id} className="relative pl-10">
              {!isLast && (
                <div
                  className="absolute left-4 top-9 bottom-[-1rem] w-0.5"
                  style={{ backgroundColor: '#d5d9d9' }}
                />
              )}
              <div
                className="absolute left-0 top-1 flex items-center justify-center w-8 h-8 rounded-full border-2"
                style={{ backgroundColor: style.badge, borderColor: style.border, color: style.badgeText }}
              >
                {style.icon}
              </div>

              <div
                className="rounded-xl border p-5 space-y-3"
                style={{ backgroundColor: '#fff', borderColor: '#d5d9d9', boxShadow: '0 1px 6px rgba(0,0,0,0.05)' }}
              >
                <div className="flex flex-wrap items-start justify-between gap-2">
                  <div>
                    <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: '#565959' }}>
                      Step {i + 1} · {node.category}
                    </span>
                    <h3 className="text-base font-bold" style={{ color: '#0f1111' }}>
                      {node.title}
                    </h3>
                  </div>
                  <span
                    className="px-2.5 py-1 rounded text-[11px] font-bold uppercase tracking-wide"
                    style={{ backgroundColor: style.badge, color: style.badgeText }}
                  >
                    {node.status}
                  </span>
                </div>

                <p className="text-sm leading-relaxed" style={{ color: '#565959' }}>
                  {node.description}
                </p>

                <div className="flex items-center gap-4 text-xs" style={{ color: '#565959' }}>
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    {node.estimatedHours}h · {node.difficulty}
                  </span>
                </div>

                {node.citation && (
                  <a
                    href={node.citation.postingUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-start gap-2 p-3 rounded-lg border text-xs"
                    style={{ backgroundColor: '#edf6fb', borderColor: '#b8d5f5', color: '#007fa3' }}
                  >
                    <ExternalLink className="w-3.5 h-3.5 mt-0.5 flex-shrink-0" />
                    <span>
                      <strong>{node.citation.jobTitle}</strong> @ {node.citation.company} ·{' '}
                      {node.citation.demandCount ?? 0} similar postings — "{node.citation.relevanceExcerpt}"
                    </span>
                  </a>
                )}

                {node.status === 'unlocked' && (
                  <Link
                    href={`/roadmap/${node.id}`}
                    className="inline-flex items-center gap-1.5 text-xs font-bold"
                    style={{ color: '#c45500' }}
                  >
                    Start micro-project
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
