import { useState } from 'react';
import { useForm, FormProvider } from 'react-hook-form';
import { AnimatePresence, motion } from 'framer-motion';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import { ChevronLeft, ChevronRight, Send } from 'lucide-react';
import SurveyProgress from './SurveyProgress';
import { SURVEY_STEPS } from '../../data/questionnaireConfig';
import { STEP_FIELD_NAMES, buildDefaultValues } from './surveyFormConfig';

import AboutYouStep from './steps/AboutYouStep';
import VisitInfoStep from './steps/VisitInfoStep';
import NarrativeStep from './steps/NarrativeStep';
import AffordabilityStep from './steps/AffordabilityStep';
import QualityOfCareStep from './steps/QualityOfCareStep';
import EnvironmentStep from './steps/EnvironmentStep';
import GeneralSatisfactionStep from './steps/GeneralSatisfactionStep';

const STEP_COMPONENTS = {
  aboutYou: AboutYouStep,
  visitInfo: VisitInfoStep,
  narrative: NarrativeStep,
  affordability: AffordabilityStep,
  qualityOfCare: QualityOfCareStep,
  environment: EnvironmentStep,
  generalSatisfaction: GeneralSatisfactionStep,
};

export default function SurveyForm({ onSubmit, submitting }) {
  const [stepIndex, setStepIndex] = useState(0);
  const methods = useForm({ defaultValues: buildDefaultValues() });
  const { handleSubmit, trigger } = methods;

  const step = SURVEY_STEPS[stepIndex];
  const StepComponent = STEP_COMPONENTS[step.id];
  const isLastStep = stepIndex === SURVEY_STEPS.length - 1;

  const handleNext = async () => {
    const valid = await trigger(STEP_FIELD_NAMES[step.id]);
    if (valid) setStepIndex((prev) => Math.min(prev + 1, SURVEY_STEPS.length - 1));
  };

  const handleBack = () => setStepIndex((prev) => Math.max(prev - 1, 0));

  return (
    <FormProvider {...methods}>
      <SurveyProgress stepIndex={stepIndex} />
      <Paper variant="outlined" sx={{ p: { xs: 2.5, sm: 3.5 } }}>
        <AnimatePresence mode="wait">
          <motion.div
            key={step.id}
            initial={{ opacity: 0, x: 16 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -16 }}
            transition={{ duration: 0.2 }}
          >
            <StepComponent />
          </motion.div>
        </AnimatePresence>

        <Stack direction="row" justifyContent="space-between" sx={{ mt: 3 }}>
          <Button startIcon={<ChevronLeft size={16} />} onClick={handleBack} disabled={stepIndex === 0 || submitting}>
            Back
          </Button>
          {isLastStep ? (
            <Button
              variant="contained"
              endIcon={<Send size={16} />}
              onClick={handleSubmit(onSubmit)}
              disabled={submitting}
            >
              {submitting ? 'Submitting…' : 'Submit Feedback'}
            </Button>
          ) : (
            <Button variant="contained" endIcon={<ChevronRight size={16} />} onClick={handleNext}>
              Next
            </Button>
          )}
        </Stack>
      </Paper>
    </FormProvider>
  );
}
