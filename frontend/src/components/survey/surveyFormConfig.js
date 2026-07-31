import {
  AFFORDABILITY_QUESTIONS,
  QUALITY_OF_CARE_QUESTIONS,
  ENVIRONMENT_QUESTIONS,
} from '../../data/questionnaireConfig';

// Field names react-hook-form should validate before advancing past each
// step, derived from the same question config the step components render.
export const STEP_FIELD_NAMES = {
  aboutYou: ['aboutYou.category', 'aboutYou.ageGroup', 'aboutYou.gender', 'aboutYou.education'],
  visitInfo: ['visit.clinic', 'visit.firstVisit'],
  narrative: ['narrative.comment'],
  affordability: AFFORDABILITY_QUESTIONS.map((question) => `affordability.${question.key}`),
  qualityOfCare: QUALITY_OF_CARE_QUESTIONS.map((question) => `qualityOfCare.${question.key}`),
  environment: ENVIRONMENT_QUESTIONS.map((question) => `environment.${question.key}`),
  generalSatisfaction: [
    'generalSatisfaction.happyWithServices',
    'generalSatisfaction.recommendClinic',
    'generalSatisfaction.followUpRequested',
    'generalSatisfaction.contactPhone',
  ],
};

export function buildDefaultValues(clinic = '') {
  return {
    aboutYou: { category: '', ageGroup: '', gender: '', education: '' },
    visit: { clinic, firstVisit: '' },
    narrative: { comment: '', incidentDate: '', incidentTime: '', staffInvolved: '' },
    affordability: Object.fromEntries(AFFORDABILITY_QUESTIONS.map((question) => [question.key, 0])),
    qualityOfCare: Object.fromEntries(QUALITY_OF_CARE_QUESTIONS.map((question) => [question.key, 0])),
    environment: Object.fromEntries(ENVIRONMENT_QUESTIONS.map((question) => [question.key, 0])),
    generalSatisfaction: { happyWithServices: 0, recommendClinic: '', followUpRequested: '', contactPhone: '' },
  };
}
