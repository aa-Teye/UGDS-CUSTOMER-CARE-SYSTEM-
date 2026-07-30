import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Chip from '@mui/material/Chip';
import EmptyState from '../common/EmptyState';

export default function CommonIssuesList({
  issues,
  emptyTitle = 'No recurring issues',
  emptyDescription = 'No question area has multiple low ratings yet.',
  chipColor = 'error',
}) {
  if (issues.length === 0) {
    return <EmptyState title={emptyTitle} description={emptyDescription} />;
  }

  return (
    <Box>
      {issues.map((issue) => (
        <Box
          key={issue.label}
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            py: 1,
            borderBottom: '1px solid',
            borderColor: 'divider',
            '&:last-of-type': { borderBottom: 'none' },
          }}
        >
          <Typography variant="body2">{issue.label}</Typography>
          <Chip label={`${issue.count} report${issue.count === 1 ? '' : 's'}`} size="small" color={chipColor} variant="outlined" />
        </Box>
      ))}
    </Box>
  );
}
