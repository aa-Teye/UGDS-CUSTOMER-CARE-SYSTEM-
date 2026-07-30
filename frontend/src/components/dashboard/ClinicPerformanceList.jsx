import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Chip from '@mui/material/Chip';
import EmptyState from '../common/EmptyState';
import { formatScore } from '../../utils/formatters';
import { getScoreColor } from '../../utils/scoreColor';

export default function ClinicPerformanceList({ clinics }) {
  if (clinics.length === 0) {
    return <EmptyState title="No clinic data yet" description="Clinic performance will appear once patients respond." />;
  }

  return (
    <Box>
      {clinics.map((clinic) => (
        <Box
          key={clinic.clinic}
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            py: 1.25,
            borderBottom: '1px solid',
            borderColor: 'divider',
            '&:last-of-type': { borderBottom: 'none' },
          }}
        >
          <Box>
            <Typography variant="body2" fontWeight={600}>
              {clinic.clinic}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {clinic.responseCount} response{clinic.responseCount === 1 ? '' : 's'}
            </Typography>
          </Box>
          <Chip
            label={`${formatScore(clinic.avgSatisfaction)}/5`}
            color={getScoreColor(clinic.avgSatisfaction) === 'grey' ? 'default' : getScoreColor(clinic.avgSatisfaction)}
            size="small"
          />
        </Box>
      ))}
    </Box>
  );
}
