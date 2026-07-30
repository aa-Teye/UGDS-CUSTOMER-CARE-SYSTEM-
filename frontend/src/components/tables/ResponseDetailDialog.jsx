import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';
import { X } from 'lucide-react';
import {
  AFFORDABILITY_QUESTIONS,
  QUALITY_OF_CARE_QUESTIONS,
  ENVIRONMENT_QUESTIONS,
  LIKERT_SCALE,
} from '../../data/questionnaireConfig';
import { formatDateTime } from '../../utils/formatters';

function likertLabel(value) {
  return LIKERT_SCALE.find((option) => option.value === value)?.label ?? '—';
}

function yesNoLabel(value) {
  return value === 'yes' ? 'Yes' : value === 'no' ? 'No' : '—';
}

function QARow({ label, value }) {
  return (
    <Stack direction="row" justifyContent="space-between" sx={{ py: 0.75 }}>
      <Typography variant="body2" color="text.secondary" sx={{ maxWidth: '65%' }}>
        {label}
      </Typography>
      <Typography variant="body2" fontWeight={600}>
        {value}
      </Typography>
    </Stack>
  );
}

function Section({ title, children }) {
  return (
    <Box sx={{ mb: 3 }}>
      <Typography variant="subtitle2" fontWeight={700} sx={{ mb: 1 }}>
        {title}
      </Typography>
      {children}
      <Divider sx={{ mt: 2 }} />
    </Box>
  );
}

export default function ResponseDetailDialog({ response, open, onClose, showContact = false }) {
  if (!response) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <Box>
          <Typography variant="h6" fontWeight={700}>
            {response.clinic}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Submitted {formatDateTime(response.submittedAt)}
          </Typography>
        </Box>
        <IconButton onClick={onClose} size="small">
          <X size={18} />
        </IconButton>
      </DialogTitle>
      <DialogContent dividers>
        <Section title="About You">
          <QARow label="Category" value={response.aboutYou.category} />
          <QARow label="Age group" value={response.aboutYou.ageGroup} />
          <QARow label="Gender" value={response.aboutYou.gender} />
          <QARow label="Education level" value={response.aboutYou.education} />
        </Section>

        <Section title="Visit Information">
          <QARow label="Clinic/unit visited" value={response.visit.clinic} />
          <QARow label="First visit?" value={yesNoLabel(response.visit.firstVisit)} />
        </Section>

        <Section title="Feedback Narrative">
          <Typography variant="body2" sx={{ mb: 1.5 }}>
            {response.narrative.comment}
          </Typography>
          <QARow label="Incident date" value={response.narrative.incidentDate?.slice(0, 10) || '—'} />
          <QARow label="Incident time" value={response.narrative.incidentTime || '—'} />
          <QARow label="Staff involved" value={response.narrative.staffInvolved || '—'} />
        </Section>

        <Section title="Affordability">
          {AFFORDABILITY_QUESTIONS.map((question) => (
            <QARow key={question.key} label={question.label} value={likertLabel(response.affordability[question.key])} />
          ))}
        </Section>

        <Section title="Quality of Care">
          {QUALITY_OF_CARE_QUESTIONS.map((question) => (
            <QARow key={question.key} label={question.label} value={likertLabel(response.qualityOfCare[question.key])} />
          ))}
        </Section>

        <Section title="Environment">
          {ENVIRONMENT_QUESTIONS.map((question) => (
            <QARow key={question.key} label={question.label} value={likertLabel(response.environment[question.key])} />
          ))}
        </Section>

        <Box>
          <Typography variant="subtitle2" fontWeight={700} sx={{ mb: 1 }}>
            General Satisfaction
          </Typography>
          <QARow label="Happy with services?" value={likertLabel(response.generalSatisfaction.happyWithServices)} />
          <QARow label="Would recommend clinic?" value={yesNoLabel(response.generalSatisfaction.recommendClinic)} />
          <QARow label="Follow-up requested?" value={yesNoLabel(response.generalSatisfaction.followUpRequested)} />
          {showContact && response.generalSatisfaction.contactPhone && (
            <QARow label="Contact phone" value={response.generalSatisfaction.contactPhone} />
          )}
        </Box>
      </DialogContent>
    </Dialog>
  );
}
