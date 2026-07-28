import {
  DASHBOARD_QUALITY_METRICS,
  QUALITY_OF_CARE_QUESTIONS,
  AFFORDABILITY_QUESTIONS,
  ENVIRONMENT_QUESTIONS,
} from '../data/questionnaireConfig';

// All dashboard/analytics numbers are derived here from raw questionnaire
// answers, never hardcoded in components — this file is the single place
// that knows "what a score means".

function average(values) {
  const clean = values.filter((value) => typeof value === 'number' && !Number.isNaN(value));
  if (clean.length === 0) return null;
  return clean.reduce((sum, value) => sum + value, 0) / clean.length;
}

function averageOfKeys(responses, section, keys) {
  const values = responses.flatMap((response) => keys.map((key) => response[section]?.[key]));
  return average(values);
}

export function computeSummaryMetrics(responses) {
  const avgSatisfaction = average(responses.map((response) => response.generalSatisfaction?.happyWithServices));
  const recommendCount = responses.filter((response) => response.generalSatisfaction?.recommendClinic === 'yes').length;
  const recommendationRate = responses.length > 0 ? (recommendCount / responses.length) * 100 : 0;
  const followUpRequests = responses.filter((response) => response.generalSatisfaction?.followUpRequested === 'yes').length;

  return {
    avgSatisfaction,
    totalResponses: responses.length,
    recommendationRate,
    followUpRequests,
  };
}

export function computeQualityOfCareScores(responses) {
  return DASHBOARD_QUALITY_METRICS.map((metric) => ({
    id: metric.id,
    label: metric.label,
    score: averageOfKeys(responses, 'qualityOfCare', metric.keys),
  }));
}

export function computeFullQualityOfCareBreakdown(responses) {
  return QUALITY_OF_CARE_QUESTIONS.map((question) => ({
    key: question.key,
    label: question.label,
    score: averageOfKeys(responses, 'qualityOfCare', [question.key]),
  }));
}

export function computeAffordabilityScores(responses) {
  return AFFORDABILITY_QUESTIONS.map((question) => ({
    key: question.key,
    label: question.label,
    score: averageOfKeys(responses, 'affordability', [question.key]),
  }));
}

export function computeEnvironmentScores(responses) {
  return ENVIRONMENT_QUESTIONS.map((question) => ({
    key: question.key,
    label: question.label,
    score: averageOfKeys(responses, 'environment', [question.key]),
  }));
}

export function computeClinicPerformance(responses) {
  const byClinic = new Map();
  responses.forEach((response) => {
    const clinic = response.clinic;
    if (!byClinic.has(clinic)) byClinic.set(clinic, []);
    byClinic.get(clinic).push(response.generalSatisfaction?.happyWithServices);
  });

  return Array.from(byClinic.entries())
    .map(([clinic, scores]) => ({
      clinic,
      responseCount: scores.length,
      avgSatisfaction: average(scores),
    }))
    .sort((a, b) => b.responseCount - a.responseCount);
}

// Follow-up requests carry no patient identity, so the only way to act on
// one is to know which unit it concerns — this groups pending follow-ups by
// clinic so management can route them without ever seeing who asked.
export function computeFollowUpsByClinic(responses) {
  const counts = new Map();
  responses
    .filter((response) => response.generalSatisfaction?.followUpRequested === 'yes')
    .forEach((response) => {
      counts.set(response.clinic, (counts.get(response.clinic) ?? 0) + 1);
    });

  return Array.from(counts.entries())
    .map(([label, count]) => ({ label, count }))
    .sort((a, b) => b.count - a.count);
}

export function computeFeedbackInsights(responses, { limit = 5 } = {}) {
  const sorted = [...responses].sort((a, b) => new Date(b.submittedAt) - new Date(a.submittedAt));
  const withComment = sorted.filter((response) => response.narrative?.comment);

  const positive = withComment.filter((response) => response.generalSatisfaction?.happyWithServices >= 4);
  const complaints = withComment.filter((response) => response.generalSatisfaction?.happyWithServices <= 2);

  return {
    recentComments: withComment.slice(0, limit),
    positive: positive.slice(0, limit),
    complaints: complaints.slice(0, limit),
    commonIssues: computeCommonIssues(responses),
  };
}

// Ranks question areas by how often they were rated poorly (<=2), giving a
// factual "what's going wrong" list instead of relying on free-text parsing.
export function computeCommonIssues(responses, { limit = 5 } = {}) {
  const trackedQuestions = [
    ...QUALITY_OF_CARE_QUESTIONS.map((q) => ({ ...q, section: 'qualityOfCare' })),
    ...ENVIRONMENT_QUESTIONS.map((q) => ({ ...q, section: 'environment' })),
    ...AFFORDABILITY_QUESTIONS.map((q) => ({ ...q, section: 'affordability' })),
  ];

  const issues = trackedQuestions.map((question) => {
    const lowCount = responses.filter((response) => response[question.section]?.[question.key] <= 2).length;
    return { label: question.label, count: lowCount };
  });

  return issues
    .filter((issue) => issue.count > 0)
    .sort((a, b) => b.count - a.count)
    .slice(0, limit);
}

export function computeSatisfactionTrend(responses) {
  const weeks = new Map();
  responses.forEach((response) => {
    const date = new Date(response.submittedAt);
    const weekStart = new Date(date);
    weekStart.setDate(date.getDate() - date.getDay());
    weekStart.setHours(0, 0, 0, 0);
    const key = weekStart.toISOString();
    if (!weeks.has(key)) weeks.set(key, []);
    weeks.get(key).push(response.generalSatisfaction?.happyWithServices);
  });

  return Array.from(weeks.entries())
    .sort(([a], [b]) => new Date(a) - new Date(b))
    .map(([weekStart, scores]) => ({
      week: new Date(weekStart).toLocaleDateString('en-GB', { day: '2-digit', month: 'short' }),
      avgSatisfaction: average(scores),
      responses: scores.length,
    }));
}
