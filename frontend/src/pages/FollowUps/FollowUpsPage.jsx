import { useMemo, useState } from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import PageHeader from '../../components/common/PageHeader';
import FollowUpsTable from '../../components/tables/FollowUpsTable';
import ResponseDetailDialog from '../../components/tables/ResponseDetailDialog';
import { useResponses } from '../../hooks/useResponses';

export default function FollowUpsPage() {
  const responses = useResponses();
  const [selectedResponse, setSelectedResponse] = useState(null);

  const requests = useMemo(
    () =>
      responses
        .filter((response) => response.generalSatisfaction?.followUpRequested === 'yes' && response.generalSatisfaction?.contactPhone)
        .sort((a, b) => new Date(b.submittedAt) - new Date(a.submittedAt)),
    [responses],
  );

  return (
    <Box>
      <PageHeader
        title="Follow-up Requests"
        description="Patients who asked to be contacted and left a number — everyone else stays anonymous."
      />

      <Paper variant="outlined" sx={{ p: 2 }}>
        <FollowUpsTable requests={requests} onView={setSelectedResponse} />
      </Paper>

      <ResponseDetailDialog
        response={selectedResponse}
        open={Boolean(selectedResponse)}
        onClose={() => setSelectedResponse(null)}
        showContact
      />
    </Box>
  );
}
