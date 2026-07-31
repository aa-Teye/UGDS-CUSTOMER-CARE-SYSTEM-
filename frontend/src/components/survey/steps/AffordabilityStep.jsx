import { useFormContext } from 'react-hook-form';
import Stack from '@mui/material/Stack';
import LikertField from '../LikertField';
import { AFFORDABILITY_QUESTIONS } from '../../../data/questionnaireConfig';

export default function AffordabilityStep() {
  const { control } = useFormContext();

  return (
    <Stack>
      {AFFORDABILITY_QUESTIONS.map((question) => (
        <LikertField key={question.key} name={`affordability.${question.key}`} label={question.label} control={control} />
      ))}
    </Stack>
  );
}
