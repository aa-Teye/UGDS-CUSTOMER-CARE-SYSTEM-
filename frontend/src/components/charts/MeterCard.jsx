import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import LinearProgress from '@mui/material/LinearProgress';
import { formatPercent } from '../../utils/formatters';

// A ratio against a fixed limit (0-100%) reads better as a meter than a
// two-slice pie: the fill communicates severity directly, at a glance.
export default function MeterCard({ title, description, percent, color = 'success' }) {
  return (
    <Paper variant="outlined" sx={{ p: 2.5, height: '100%' }}>
      <Typography variant="subtitle1" fontWeight={700}>
        {title}
      </Typography>
      {description && (
        <Typography variant="caption" color="text.secondary">
          {description}
        </Typography>
      )}
      <Typography variant="h3" fontWeight={700} sx={{ mt: 2, mb: 1.5 }}>
        {formatPercent(percent)}
      </Typography>
      <LinearProgress
        variant="determinate"
        value={Math.min(percent, 100)}
        color={color}
        sx={{ height: 10, borderRadius: 5, bgcolor: 'action.hover' }}
      />
    </Paper>
  );
}
