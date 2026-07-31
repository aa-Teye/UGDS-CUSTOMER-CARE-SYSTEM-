import { Controller, useFormContext, useWatch } from 'react-hook-form';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import LikertField from '../LikertField';
import YesNoField from '../YesNoField';

export default function GeneralSatisfactionStep() {
  const { control } = useFormContext();
  const followUpRequested = useWatch({ control, name: 'generalSatisfaction.followUpRequested' });

  return (
    <Stack>
      <LikertField name="generalSatisfaction.happyWithServices" label="Are you happy with the services received?" control={control} />
      <YesNoField name="generalSatisfaction.recommendClinic" label="Would you recommend this clinic to others?" control={control} />
      <YesNoField name="generalSatisfaction.followUpRequested" label="Would you like a follow-up regarding your visit?" control={control} />

      {followUpRequested === 'yes' && (
        <Controller
          name="generalSatisfaction.contactPhone"
          control={control}
          rules={{ required: followUpRequested === 'yes' ? 'A phone number is needed so we can reach you' : false }}
          render={({ field, fieldState }) => (
            <TextField
              {...field}
              label="Phone number"
              type="tel"
              fullWidth
              autoComplete="tel"
              error={Boolean(fieldState.error)}
              helperText={fieldState.error?.message ?? 'Only used to contact you about this visit — not stored with your answers publicly.'}
              sx={{ mt: 1 }}
            />
          )}
        />
      )}
      {followUpRequested !== 'yes' && (
        <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
          Answered "No" — your response stays fully anonymous.
        </Typography>
      )}
    </Stack>
  );
}
