import { useMemo, useState } from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import { Search } from 'lucide-react';
import PageHeader from '../../components/common/PageHeader';
import ResponsesTable from '../../components/tables/ResponsesTable';
import ResponseDetailDialog from '../../components/tables/ResponseDetailDialog';
import { useResponses } from '../../hooks/useResponses';

export default function ResponsesPage() {
  const responses = useResponses();
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [selectedResponse, setSelectedResponse] = useState(null);

  const filtered = useMemo(() => {
    const query = search.trim().toLowerCase();
    return [...responses]
      .filter((response) => !query || response.clinic.toLowerCase().includes(query))
      .sort((a, b) => new Date(b.submittedAt) - new Date(a.submittedAt));
  }, [responses, search]);

  const paginated = filtered.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);

  return (
    <Box>
      <PageHeader title="Feedback Responses" description="Every anonymous survey response submitted." />

      <Paper variant="outlined" sx={{ p: 2 }}>
        <TextField
          placeholder="Search by clinic"
          size="small"
          value={search}
          onChange={(event) => {
            setSearch(event.target.value);
            setPage(0);
          }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <Search size={16} />
                </InputAdornment>
              ),
            },
          }}
          sx={{ mb: 2, maxWidth: 360 }}
        />

        <ResponsesTable
          responses={paginated}
          page={page}
          rowsPerPage={rowsPerPage}
          totalCount={filtered.length}
          onPageChange={setPage}
          onRowsPerPageChange={(value) => {
            setRowsPerPage(value);
            setPage(0);
          }}
          onView={setSelectedResponse}
        />
      </Paper>

      <ResponseDetailDialog
        response={selectedResponse}
        open={Boolean(selectedResponse)}
        onClose={() => setSelectedResponse(null)}
      />
    </Box>
  );
}
