import { useFormContext } from 'react-hook-form';
import Stack from '@mui/material/Stack';
import LikertField from '../LikertField';
import { ENVIRONMENT_QUESTIONS } from '../../../data/questionnaireConfig';

export default function EnvironmentStep() {
  const { control } = useFormContext();

  return (
    <Stack>
      {ENVIRONMENT_QUESTIONS.map((question) => (
        <LikertField key={question.key} name={`environment.${question.key}`} label={question.label} control={control} />
      ))}
    </Stack>
  );
}
