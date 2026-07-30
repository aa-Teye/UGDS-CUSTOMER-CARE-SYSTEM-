import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import LinearProgress from '@mui/material/LinearProgress';
import { formatScore } from '../../utils/formatters';
import { getScoreColor } from '../../utils/scoreColor';

export default function QualityScoreBar({ label, score }) {
  const color = getScoreColor(score);
  const percent = score ? (score / 5) * 100 : 0;

  return (
    <Box sx={{ mb: 1.75 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
        <Typography variant="body2">{label}</Typography>
        <Typography variant="body2" fontWeight={700}>
          {formatScore(score)}/5
        </Typography>
      </Box>
      <LinearProgress
        variant="determinate"
        value={percent}
        color={color === 'grey' ? undefined : color}
        sx={{ height: 6, borderRadius: 3, bgcolor: 'action.hover' }}
      />
    </Box>
  );
}
