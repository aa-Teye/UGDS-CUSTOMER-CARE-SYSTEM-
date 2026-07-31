import { useFormContext } from 'react-hook-form';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import LikertField from '../LikertField';
import { QUALITY_OF_CARE_QUESTIONS } from '../../../data/questionnaireConfig';

export default function QualityOfCareStep() {
  const { control } = useFormContext();

  return (
    <Stack>
      {QUALITY_OF_CARE_QUESTIONS.map((question, index) => (
        <div key={question.key}>
          <LikertField name={`qualityOfCare.${question.key}`} label={question.label} control={control} />
          {index < QUALITY_OF_CARE_QUESTIONS.length - 1 && <Divider sx={{ my: 0.5 }} />}
        </div>
      ))}
    </Stack>
  );
}
