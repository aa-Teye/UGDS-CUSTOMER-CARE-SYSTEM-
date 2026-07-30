import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import EmptyState from '../common/EmptyState';

export default function ChartCard({ title, description, height = 280, isEmpty, emptyMessage, children }) {
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
      <Box sx={{ mt: 2, height }}>
        {isEmpty ? (
          <EmptyState title="Not enough data yet" description={emptyMessage} />
        ) : (
          children
        )}
      </Box>
    </Paper>
  );
}
