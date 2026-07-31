import { Controller } from 'react-hook-form';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import ToggleButton from '@mui/material/ToggleButton';
import FormHelperText from '@mui/material/FormHelperText';
import { YES_NO_OPTIONS } from '../../data/questionnaireConfig';

export default function YesNoField({ name, label, control }) {
  return (
    <Controller
      name={name}
      control={control}
      rules={{ required: 'Please choose an option' }}
      render={({ field, fieldState }) => (
        <Box sx={{ py: 1.25 }}>
          <Typography variant="body2" fontWeight={500} sx={{ mb: 1 }}>
            {label}
          </Typography>
          <ToggleButtonGroup
            exclusive
            size="small"
            value={field.value || null}
            onChange={(_event, value) => {
              if (value !== null) field.onChange(value);
            }}
          >
            {YES_NO_OPTIONS.map((option) => (
              <ToggleButton key={option.value} value={option.value} sx={{ px: 3 }}>
                {option.label}
              </ToggleButton>
            ))}
          </ToggleButtonGroup>
          {fieldState.error && <FormHelperText error>{fieldState.error.message}</FormHelperText>}
        </Box>
      )}
    />
  );
}
