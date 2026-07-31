import { Controller, useFormContext } from 'react-hook-form';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import YesNoField from '../YesNoField';
import { CLINIC_OPTIONS } from '../../../data/questionnaireConfig';

export default function VisitInfoStep() {
  const { control } = useFormContext();

  return (
    <Stack spacing={2.5}>
      <Controller
        name="visit.clinic"
        control={control}
        rules={{ required: 'Please select the clinic/unit you visited' }}
        render={({ field, fieldState }) => (
          <TextField
            {...field}
            select
            label="Which unit(s) did you visit today?"
            fullWidth
            error={Boolean(fieldState.error)}
            helperText={fieldState.error?.message}
            slotProps={{ select: { native: true } }}
          >
            <option value="" disabled></option>
            {CLINIC_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </TextField>
        )}
      />

      <YesNoField name="visit.firstVisit" label="Is this your first visit to the clinic?" control={control} />
    </Stack>
  );
}
