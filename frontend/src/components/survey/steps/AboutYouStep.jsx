import { Controller, useFormContext } from 'react-hook-form';
import Stack from '@mui/material/Stack';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';
import TextField from '@mui/material/TextField';
import FormHelperText from '@mui/material/FormHelperText';
import { CATEGORY_OPTIONS, AGE_GROUP_OPTIONS, GENDER_OPTIONS, EDUCATION_OPTIONS } from '../../../data/questionnaireConfig';

export default function AboutYouStep() {
  const { control } = useFormContext();

  return (
    <Stack spacing={2.5}>
      <Controller
        name="aboutYou.category"
        control={control}
        rules={{ required: 'Please select a category' }}
        render={({ field, fieldState }) => (
          <FormControl error={Boolean(fieldState.error)}>
            <FormLabel sx={{ fontWeight: 600, fontSize: 14, color: 'text.primary' }}>
              Which category best describes you?
            </FormLabel>
            <RadioGroup {...field} row>
              {CATEGORY_OPTIONS.map((option) => (
                <FormControlLabel key={option} value={option} control={<Radio size="small" />} label={option} />
              ))}
            </RadioGroup>
            {fieldState.error && <FormHelperText>{fieldState.error.message}</FormHelperText>}
          </FormControl>
        )}
      />

      <Controller
        name="aboutYou.ageGroup"
        control={control}
        rules={{ required: 'Please select your age group' }}
        render={({ field, fieldState }) => (
          <TextField
            {...field}
            select
            label="Age group"
            fullWidth
            error={Boolean(fieldState.error)}
            helperText={fieldState.error?.message}
            slotProps={{ select: { native: true } }}
          >
            <option value="" disabled></option>
            {AGE_GROUP_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </TextField>
        )}
      />

      <Controller
        name="aboutYou.gender"
        control={control}
        rules={{ required: 'Please select your gender' }}
        render={({ field, fieldState }) => (
          <FormControl error={Boolean(fieldState.error)}>
            <FormLabel sx={{ fontWeight: 600, fontSize: 14, color: 'text.primary' }}>Gender</FormLabel>
            <RadioGroup {...field} row>
              {GENDER_OPTIONS.map((option) => (
                <FormControlLabel key={option} value={option} control={<Radio size="small" />} label={option} />
              ))}
            </RadioGroup>
            {fieldState.error && <FormHelperText>{fieldState.error.message}</FormHelperText>}
          </FormControl>
        )}
      />

      <Controller
        name="aboutYou.education"
        control={control}
        rules={{ required: 'Please select your education level' }}
        render={({ field, fieldState }) => (
          <TextField
            {...field}
            select
            label="Education level"
            fullWidth
            error={Boolean(fieldState.error)}
            helperText={fieldState.error?.message}
            slotProps={{ select: { native: true } }}
          >
            <option value="" disabled></option>
            {EDUCATION_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </TextField>
        )}
      />
    </Stack>
  );
}
