import { useMemo } from 'react';
import { useResponses } from './useResponses';
import {
  computeSummaryMetrics,
  computeQualityOfCareScores,
  computeFullQualityOfCareBreakdown,
  computeAffordabilityScores,
  computeEnvironmentScores,
  computeClinicPerformance,
  computeFollowUpsByClinic,
  computeFeedbackInsights,
  computeSatisfactionTrend,
} from '../utils/aggregations';

// Runs every dashboard/analytics aggregation once per data change, memoized
// so chart-heavy pages don't recompute on unrelated re-renders.
export function useFeedbackAnalytics() {
  const responses = useResponses();

  return useMemo(
    () => ({
      responses,
      summary: computeSummaryMetrics(responses),
      qualityOfCareHighlights: computeQualityOfCareScores(responses),
      qualityOfCareBreakdown: computeFullQualityOfCareBreakdown(responses),
      affordabilityScores: computeAffordabilityScores(responses),
      environmentScores: computeEnvironmentScores(responses),
      clinicPerformance: computeClinicPerformance(responses),
      followUpsByClinic: computeFollowUpsByClinic(responses),
      insights: computeFeedbackInsights(responses),
      satisfactionTrend: computeSatisfactionTrend(responses),
    }),
    [responses],
  );
}
