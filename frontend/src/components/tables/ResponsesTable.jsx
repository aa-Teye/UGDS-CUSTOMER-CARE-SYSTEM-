import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TablePagination from '@mui/material/TablePagination';
import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { Eye } from 'lucide-react';
import EmptyState from '../common/EmptyState';
import { formatDate } from '../../utils/formatters';
import { getScoreColor } from '../../utils/scoreColor';

export default function ResponsesTable({ responses, page, rowsPerPage, totalCount, onPageChange, onRowsPerPageChange, onView }) {
  if (totalCount === 0) {
    return <EmptyState title="No responses yet" description="Submitted feedback will appear here." />;
  }

  return (
    <Box>
      <TableContainer sx={{ overflowX: 'auto' }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Date</TableCell>
              <TableCell>Clinic</TableCell>
              <TableCell>Rating</TableCell>
              <TableCell>Recommendation</TableCell>
              <TableCell>Comments</TableCell>
              <TableCell align="right">View</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {responses.map((response) => {
              const rating = response.generalSatisfaction?.happyWithServices;
              const recommends = response.generalSatisfaction?.recommendClinic === 'yes';
              return (
                <TableRow key={response.id} hover>
                  <TableCell>{formatDate(response.submittedAt)}</TableCell>
                  <TableCell>
                    <Typography variant="body2" fontWeight={600}>
                      {response.clinic}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={`${rating}/5`}
                      size="small"
                      color={getScoreColor(rating) === 'grey' ? 'default' : getScoreColor(rating)}
                    />
                  </TableCell>
                  <TableCell>
                    <Chip label={recommends ? 'Yes' : 'No'} size="small" variant="outlined" color={recommends ? 'success' : 'default'} />
                  </TableCell>
                  <TableCell sx={{ maxWidth: 260 }}>
                    <Typography variant="body2" noWrap title={response.narrative?.comment}>
                      {response.narrative?.comment}
                    </Typography>
                  </TableCell>
                  <TableCell align="right">
                    <IconButton size="small" onClick={() => onView(response)}>
                      <Eye size={16} />
                    </IconButton>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        component="div"
        count={totalCount}
        page={page}
        onPageChange={(_event, newPage) => onPageChange(newPage)}
        rowsPerPage={rowsPerPage}
        onRowsPerPageChange={(event) => onRowsPerPageChange(Number(event.target.value))}
        rowsPerPageOptions={[5, 10, 25]}
      />
    </Box>
  );
}
