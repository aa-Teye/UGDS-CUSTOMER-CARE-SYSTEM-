import {
  CLINIC_OPTIONS,
  CATEGORY_OPTIONS,
  AGE_GROUP_OPTIONS,
  GENDER_OPTIONS,
  EDUCATION_OPTIONS,
  AFFORDABILITY_QUESTIONS,
  QUALITY_OF_CARE_QUESTIONS,
  ENVIRONMENT_QUESTIONS,
} from './questionnaireConfig';
import { createSeededRandom, pick, pickWeighted, randomInt } from '../utils/random';

const POSITIVE_COMMENTS = [
  'The dentist was very professional and explained everything clearly.',
  'I was attended to quickly and the staff were friendly.',
  'Very satisfied with the treatment. The clinic was clean and welcoming.',
  'Great experience overall, the receptionist made me feel comfortable.',
  'The pain management during my procedure was excellent.',
];

const NEUTRAL_COMMENTS = [
  'The service was okay, but the waiting area could be more comfortable.',
  'Treatment was fine, though I had to wait longer than expected.',
  'Average experience, nothing particularly bad but nothing outstanding either.',
];

const NEGATIVE_COMMENTS = [
  'I waited a very long time before being attended to.',
  'The cost of treatment was not explained to me beforehand.',
  'I experienced significant pain during the procedure that was not well managed.',
  'Staff at the front desk were dismissive of my concerns.',
  'The waiting area was overcrowded and uncomfortable.',
];

const RESPONSE_COUNT = 45;
const DAY_MS = 24 * 60 * 60 * 1000;

// Each submission is fully anonymous — there is no link back to a patient
// record, only the survey answers themselves.
function randomLikertInBand(random, band) {
  if (band === 'low') return randomInt(random, 1, 2);
  if (band === 'mid') return randomInt(random, 3, 4);
  return randomInt(random, 4, 5);
}

function buildScoreGroup(random, band, questions) {
  return questions.reduce((acc, question) => {
    acc[question.key] = randomLikertInBand(random, band);
    return acc;
  }, {});
}

function generateResponses() {
  const random = createSeededRandom(20240915);

  return Array.from({ length: RESPONSE_COUNT }, (_, index) => {
    const band = pickWeighted(random, [
      { value: 'high', weight: 55 },
      { value: 'mid', weight: 30 },
      { value: 'low', weight: 15 },
    ]);

    const commentPool = band === 'high' ? POSITIVE_COMMENTS : band === 'mid' ? NEUTRAL_COMMENTS : NEGATIVE_COMMENTS;
    const clinic = pick(random, CLINIC_OPTIONS);
    const daysAgo = randomInt(random, 0, 45);
    const submittedAt = new Date(Date.now() - daysAgo * DAY_MS).toISOString();
    const happyWithServices = randomLikertInBand(random, band);
    const followUpRequested = pick(random, ['yes', 'no']);

    return {
      id: `response-${index + 1}`,
      clinic,
      submittedAt,
      aboutYou: {
        category: pick(random, CATEGORY_OPTIONS),
        ageGroup: pick(random, AGE_GROUP_OPTIONS),
        gender: pick(random, GENDER_OPTIONS),
        education: pick(random, EDUCATION_OPTIONS),
      },
      visit: {
        clinic,
        firstVisit: pick(random, ['yes', 'no']),
      },
      narrative: {
        comment: pick(random, commentPool),
        incidentDate: submittedAt,
        incidentTime: `${randomInt(random, 8, 16)}:${pick(random, ['00', '15', '30', '45'])}`,
        staffInvolved: band === 'low' ? pick(random, ['Front Desk', 'Dental Assistant', 'Duty Nurse']) : '',
      },
      affordability: buildScoreGroup(random, band, AFFORDABILITY_QUESTIONS),
      qualityOfCare: buildScoreGroup(random, band, QUALITY_OF_CARE_QUESTIONS),
      environment: buildScoreGroup(random, band, ENVIRONMENT_QUESTIONS),
      generalSatisfaction: {
        happyWithServices,
        recommendClinic: happyWithServices >= 3 ? 'yes' : 'no',
        followUpRequested,
        contactPhone: followUpRequested === 'yes' ? `+2332${randomInt(random, 10000000, 99999999)}` : '',
      },
    };
  });
}

export const mockResponses = generateResponses();
