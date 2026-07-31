import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import LinearProgress from '@mui/material/LinearProgress';
import { SURVEY_STEPS } from '../../data/questionnaireConfig';

export default function SurveyProgress({ stepIndex }) {
  const total = SURVEY_STEPS.length;
  const percent = ((stepIndex + 1) / total) * 100;

  return (
    <Box sx={{ mb: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.75 }}>
        <Typography variant="caption" color="text.secondary" fontWeight={600}>
          Step {stepIndex + 1} of {total}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          {SURVEY_STEPS[stepIndex].label}
        </Typography>
      </Box>
      <LinearProgress variant="determinate" value={percent} sx={{ height: 6, borderRadius: 3 }} />
    </Box>
  );
}
