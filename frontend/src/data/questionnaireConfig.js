// Single source of truth for the UGDS patient feedback questionnaire.
// Survey steps, dashboard sections, and analytics charts all read from
// this file instead of hardcoding labels/options in components.

export const CLINIC_OPTIONS = [
  'Records',
  'Account',
  'Oral Diagnosis Clinic',
  'Cons. Clinic',
  "Student's Clinic",
  'Advance Cons. Clinic',
  "Resident's Clinic",
  'Periodontic Clinic',
  'Paedodotic Clinic',
  'Orthodontic Clinic',
  'Consultant Surgery 1',
  'Consultant Surgery 2',
  'X-Ray',
];

export const CATEGORY_OPTIONS = ['Patient', 'Staff', 'Patient Relative', 'Other'];

export const AGE_GROUP_OPTIONS = ['Under 18', '18-25', '26-35', '36-45', '46-55', '56-65', 'Above 65'];

export const GENDER_OPTIONS = ['Male', 'Female', 'Prefer not to say'];

export const EDUCATION_OPTIONS = [
  'No formal education',
  'Basic (JHS)',
  'Secondary (SHS)',
  'Tertiary',
  'Postgraduate',
];

export const YES_NO_OPTIONS = [
  { value: 'yes', label: 'Yes' },
  { value: 'no', label: 'No' },
];

// 5-point agreement scale used for every rating-style question so scores
// stay comparable and numeric (1-5) across sections and dashboard cards.
export const LIKERT_SCALE = [
  { value: 1, label: 'Strongly Disagree' },
  { value: 2, label: 'Disagree' },
  { value: 3, label: 'Neutral' },
  { value: 4, label: 'Agree' },
  { value: 5, label: 'Strongly Agree' },
];

export const AFFORDABILITY_QUESTIONS = [
  { key: 'costAffordable', label: 'Cost is affordable' },
  { key: 'costExplained', label: 'Cost was clearly explained' },
  { key: 'paymentOptionsSatisfactory', label: 'Payment options are satisfactory' },
];

export const QUALITY_OF_CARE_QUESTIONS = [
  { key: 'receptionistFriendly', label: 'Receptionist was friendly' },
  { key: 'diagnosisCorrect', label: 'Dental problems were diagnosed correctly' },
  { key: 'dentistRespectful', label: 'Dentist treated patient respectfully' },
  { key: 'treatmentOptionsExplained', label: 'Treatment options were explained' },
  { key: 'treatmentPlanExplained', label: 'Treatment plan was explained' },
  { key: 'staffEmpathy', label: 'Staff showed empathy' },
  { key: 'painManaged', label: 'Pain was managed effectively' },
  { key: 'treatmentSatisfactory', label: 'Treatment was satisfactory' },
  { key: 'cashierService', label: 'Cashier service was satisfactory' },
  { key: 'xrayService', label: 'X-ray service was satisfactory' },
];

export const ENVIRONMENT_QUESTIONS = [
  { key: 'clinicCleanliness', label: 'Clinic cleanliness' },
  { key: 'waitingAreaComfort', label: 'Waiting area comfort' },
];

// Headline Quality of Care KPIs shown on the dashboard. Each maps to one or
// more of the full question keys above so the dashboard only ever shows
// scores that trace back to an actual questionnaire answer.
export const DASHBOARD_QUALITY_METRICS = [
  { id: 'receptionistFriendliness', label: 'Receptionist Friendliness', keys: ['receptionistFriendly'] },
  { id: 'dentistProfessionalism', label: 'Dentist Professionalism', keys: ['dentistRespectful'] },
  { id: 'diagnosisSatisfaction', label: 'Diagnosis Satisfaction', keys: ['diagnosisCorrect'] },
  {
    id: 'treatmentExplanation',
    label: 'Treatment Explanation',
    keys: ['treatmentOptionsExplained', 'treatmentPlanExplained'],
  },
  { id: 'painManagement', label: 'Pain Management', keys: ['painManaged'] },
  { id: 'staffEmpathy', label: 'Staff Empathy', keys: ['staffEmpathy'] },
];

export const SURVEY_STEPS = [
  { id: 'aboutYou', label: 'About You' },
  { id: 'visitInfo', label: 'Visit Information' },
  { id: 'narrative', label: 'Your Feedback' },
  { id: 'affordability', label: 'Affordability' },
  { id: 'qualityOfCare', label: 'Quality of Care' },
  { id: 'environment', label: 'Environment' },
  { id: 'generalSatisfaction', label: 'General Satisfaction' },
];
