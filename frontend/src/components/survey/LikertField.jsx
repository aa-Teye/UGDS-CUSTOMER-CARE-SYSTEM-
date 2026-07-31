import { Controller } from 'react-hook-form';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import ToggleButton from '@mui/material/ToggleButton';
import FormHelperText from '@mui/material/FormHelperText';
import { LIKERT_SCALE } from '../../data/questionnaireConfig';

export default function LikertField({ name, label, control }) {
  return (
    <Controller
      name={name}
      control={control}
      rules={{ required: 'Please select a rating' }}
      render={({ field, fieldState }) => (
        <Box sx={{ py: 1.25 }}>
          <Typography variant="body2" fontWeight={500} sx={{ mb: 1 }}>
            {label}
          </Typography>
          <ToggleButtonGroup
            exclusive
            fullWidth
            size="small"
            value={field.value || null}
            onChange={(_event, value) => {
              if (value !== null) field.onChange(value);
            }}
          >
            {LIKERT_SCALE.map((option) => (
              <ToggleButton key={option.value} value={option.value} sx={{ py: 1 }}>
                {option.value}
              </ToggleButton>
            ))}
          </ToggleButtonGroup>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 0.5 }}>
            <Typography variant="caption" color="text.secondary">
              Strongly Disagree
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Strongly Agree
            </Typography>
          </Box>
          {fieldState.error && <FormHelperText error>{fieldState.error.message}</FormHelperText>}
        </Box>
      )}
    />
  );
}
