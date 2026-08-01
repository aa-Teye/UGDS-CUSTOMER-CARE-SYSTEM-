import Box from '@mui/material/Box';
import { useNavigate } from 'react-router-dom';
import { Smile, MessageSquare, ThumbsUp, CalendarClock, MessageCircle, ThumbsDown, AlertCircle } from 'lucide-react';
import PageHeader from '../../components/common/PageHeader';
import StatCard from '../../components/dashboard/StatCard';
import SectionCard from '../../components/dashboard/SectionCard';
import QualityScoreBar from '../../components/dashboard/QualityScoreBar';
import ClinicPerformanceList from '../../components/dashboard/ClinicPerformanceList';
import CommentList from '../../components/dashboard/CommentList';
import CommonIssuesList from '../../components/dashboard/CommonIssuesList';
import { useFeedbackAnalytics } from '../../hooks/useFeedbackAnalytics';
import { formatScore, formatPercent } from '../../utils/formatters';

export default function DashboardPage() {
  const { summary, qualityOfCareHighlights, clinicPerformance, followUpsByClinic, insights } = useFeedbackAnalytics();
  const navigate = useNavigate();

  return (
    <Box>
      <PageHeader
        title="Dashboard Overview"
        description="Anonymous patient experience at a glance, drawn directly from submitted feedback."
      />

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr 1fr', sm: 'repeat(2,1fr)', lg: 'repeat(4,1fr)' }, gap: 2, mb: 3 }}>
        <StatCard icon={Smile} label="Average Satisfaction" value={formatScore(summary.avgSatisfaction)} suffix="/5" />
        <StatCard icon={MessageSquare} label="Total Responses" value={summary.totalResponses} color="secondary" />
        <StatCard icon={ThumbsUp} label="Recommendation Rate" value={formatPercent(summary.recommendationRate)} color="success" />
        <StatCard
          icon={CalendarClock}
          label="Follow-up Requests"
          value={summary.followUpRequests}
          color="warning"
          onClick={() => navigate('/follow-ups')}
        />
      </Box>

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', lg: '1.4fr 1fr' }, gap: 3, mb: 3 }}>
        <SectionCard title="Service Quality Analysis" description="Average score per Quality of Care question (1-5)">
          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' }, columnGap: 3 }}>
            {qualityOfCareHighlights.map((metric) => (
              <QualityScoreBar key={metric.id} label={metric.label} score={metric.score} />
            ))}
          </Box>
        </SectionCard>

        <SectionCard title="Clinic Performance" description="Responses and average satisfaction by unit">
          <ClinicPerformanceList clinics={clinicPerformance} />
        </SectionCard>
      </Box>

      <SectionCard
        title="Follow-up Requests by Unit"
        description="Where patients asked to be followed up with — routed by unit, not by identity"
        sx={{ mb: 3 }}
      >
        <CommonIssuesList
          issues={followUpsByClinic}
          emptyTitle="No follow-up requests"
          emptyDescription="Units with pending follow-up requests will appear here."
          chipColor="warning"
        />
      </SectionCard>

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', lg: 'repeat(3,1fr)' }, gap: 3 }}>
        <SectionCard title="Recent Comments" description="Most recent submissions" action={<MessageCircle size={18} />}>
          <CommentList comments={insights.recentComments} emptyMessage="Feedback comments will show up here." />
        </SectionCard>
        <SectionCard title="Positive Feedback" description="Highest-rated responses" action={<ThumbsUp size={18} color="#2E7D32" />}>
          <CommentList comments={insights.positive} emptyMessage="No highly-rated comments yet." />
        </SectionCard>
        <SectionCard title="Complaints & Common Issues" description="Lowest-rated responses and recurring problem areas" action={<ThumbsDown size={18} color="#C62828" />}>
          <CommentList comments={insights.complaints} emptyMessage="No complaints reported." />
          <Box sx={{ mt: 2, pt: 2, borderTop: '1px solid', borderColor: 'divider' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.75, mb: 1 }}>
              <AlertCircle size={14} />
              <Box sx={{ typography: 'caption', fontWeight: 600 }}>Common Issues</Box>
            </Box>
            <CommonIssuesList issues={insights.commonIssues} />
          </Box>
        </SectionCard>
      </Box>
    </Box>
  );
}
