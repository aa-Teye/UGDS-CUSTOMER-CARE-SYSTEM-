import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import EmptyState from '../common/EmptyState';
import { formatDate } from '../../utils/formatters';
import { getScoreColor } from '../../utils/scoreColor';

export default function CommentList({ comments, emptyMessage }) {
  if (comments.length === 0) {
    return <EmptyState title="No comments yet" description={emptyMessage} />;
  }

  return (
    <Stack spacing={1.5}>
      {comments.map((response) => {
        const score = response.generalSatisfaction?.happyWithServices;
        return (
          <Box key={response.id} sx={{ p: 1.5, borderRadius: 2, bgcolor: 'action.hover' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
              <Typography variant="caption" color="text.secondary">
                {response.clinic}
              </Typography>
              <Chip
                label={`${score}/5`}
                size="small"
                color={getScoreColor(score) === 'grey' ? 'default' : getScoreColor(score)}
                sx={{ height: 20 }}
              />
            </Box>
            <Typography variant="body2">{response.narrative.comment}</Typography>
            <Typography variant="caption" color="text.secondary">
              {formatDate(response.submittedAt)}
            </Typography>
          </Box>
        );
      })}
    </Stack>
  );
}
