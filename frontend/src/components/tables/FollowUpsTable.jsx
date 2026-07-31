import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Link from '@mui/material/Link';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';
import { Phone } from 'lucide-react';
import EmptyState from '../common/EmptyState';
import { formatDate } from '../../utils/formatters';
import { getScoreColor } from '../../utils/scoreColor';

export default function FollowUpsTable({ requests, onView }) {
  if (requests.length === 0) {
    return (
      <EmptyState
        icon={Phone}
        title="No follow-up requests"
        description="When a patient asks to be contacted and leaves a number, it will appear here."
      />
    );
  }

  return (
    <TableContainer sx={{ overflowX: 'auto' }}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Date</TableCell>
            <TableCell>Clinic</TableCell>
            <TableCell>Rating</TableCell>
            <TableCell>Phone number</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {requests.map((response) => {
            const rating = response.generalSatisfaction?.happyWithServices;
            return (
              <TableRow key={response.id} hover>
                <TableCell>{formatDate(response.submittedAt)}</TableCell>
                <TableCell>{response.clinic}</TableCell>
                <TableCell>
                  <Chip
                    label={`${rating}/5`}
                    size="small"
                    color={getScoreColor(rating) === 'grey' ? 'default' : getScoreColor(rating)}
                  />
                </TableCell>
                <TableCell>
                  <Link
                    component="button"
                    type="button"
                    underline="hover"
                    onClick={() => onView(response)}
                    sx={{ display: 'inline-flex', alignItems: 'center', gap: 0.75, fontWeight: 600, fontSize: 13 }}
                  >
                    <Box sx={{ display: 'inline-flex' }}>
                      <Phone size={14} />
                    </Box>
                    {response.generalSatisfaction.contactPhone}
                  </Link>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
