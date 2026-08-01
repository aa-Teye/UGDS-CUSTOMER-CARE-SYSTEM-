import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import SurveyForm from '../../components/survey/SurveyForm';
import { submitSurveyResponse } from '../../services/feedbackService';
import { useToast } from '../../hooks/useToast';

export default function SurveyPage() {
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (formData) => {
    setSubmitting(true);
    try {
      await submitSurveyResponse(formData);
      navigate('/survey/thank-you');
    } catch {
      showToast('Something went wrong submitting your feedback. Please try again.', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Box>
      <Box sx={{ mb: 3, textAlign: 'left' }}>
        <Typography variant="h5" fontWeight={700}>
          Patient Experience Feedback
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Your feedback is completely anonymous and helps us improve the quality of care at UGDS. This survey
          takes about 3 minutes.
        </Typography>
      </Box>
      <SurveyForm onSubmit={handleSubmit} submitting={submitting} />
    </Box>
  );
}
