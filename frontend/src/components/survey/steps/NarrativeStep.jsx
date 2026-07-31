import { useFormContext } from 'react-hook-form';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';

export default function NarrativeStep() {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  return (
    <Stack spacing={2.5}>
      <Typography variant="body2" color="text.secondary">
        Tell us about your experience today. If something specific happened, let us know when and who was
        involved so we can follow up.
      </Typography>

      <TextField
        label="Your feedback / comment"
        multiline
        minRows={4}
        fullWidth
        error={Boolean(errors.narrative?.comment)}
        helperText={errors.narrative?.comment?.message}
        {...register('narrative.comment', { required: 'Please share your feedback' })}
      />

      <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
        <TextField
          label="Incident date (optional)"
          type="date"
          fullWidth
          slotProps={{ inputLabel: { shrink: true } }}
          {...register('narrative.incidentDate')}
        />
        <TextField
          label="Incident time (optional)"
          type="time"
          fullWidth
          slotProps={{ inputLabel: { shrink: true } }}
          {...register('narrative.incidentTime')}
        />
      </Stack>

      <TextField
        label="Staff involved (optional)"
        fullWidth
        {...register('narrative.staffInvolved')}
      />
    </Stack>
  );
}
