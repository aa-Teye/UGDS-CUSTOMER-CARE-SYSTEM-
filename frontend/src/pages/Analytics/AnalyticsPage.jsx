import Box from '@mui/material/Box';
import PageHeader from '../../components/common/PageHeader';
import ChartCard from '../../components/charts/ChartCard';
import SatisfactionTrendChart from '../../components/charts/SatisfactionTrendChart';
import HorizontalBarChart from '../../components/charts/HorizontalBarChart';
import MeterCard from '../../components/charts/MeterCard';
import { useFeedbackAnalytics } from '../../hooks/useFeedbackAnalytics';
import { formatScore } from '../../utils/formatters';

export default function AnalyticsPage() {
  const {
    responses,
    summary,
    qualityOfCareBreakdown,
    affordabilityScores,
    environmentScores,
    clinicPerformance,
    satisfactionTrend,
  } = useFeedbackAnalytics();

  const clinicRatingData = clinicPerformance.map((clinic) => ({ label: clinic.clinic, value: clinic.avgSatisfaction }));

  return (
    <Box>
      <PageHeader title="Analytics" description="Deeper trends across every dimension of the questionnaire." />

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', lg: '2fr 1fr' }, gap: 3, mb: 3 }}>
        <ChartCard
          title="Satisfaction Trend"
          description="Average weekly satisfaction score"
          isEmpty={satisfactionTrend.length === 0}
          emptyMessage="Trend appears once responses span more than one week."
        >
          <SatisfactionTrendChart data={satisfactionTrend} />
        </ChartCard>
        <MeterCard
          title="Recommendation Rate"
          description="Patients who would recommend the clinic"
          percent={summary.recommendationRate}
        />
      </Box>

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', lg: '1fr 1fr' }, gap: 3, mb: 3 }}>
        <ChartCard
          title="Ratings by Clinic"
          description="Average satisfaction score per unit (1-5)"
          height={Math.max(clinicRatingData.length * 34, 160)}
          isEmpty={clinicRatingData.length === 0}
          emptyMessage="Clinic ratings appear once feedback is submitted."
        >
          <HorizontalBarChart data={clinicRatingData} domain={[0, 5]} colorMode="status" valueLabel={(v) => `${formatScore(v)}/5`} />
        </ChartCard>

        <ChartCard
          title="Quality of Care Scores"
          description="Full breakdown of every Quality of Care question"
          height={Math.max(qualityOfCareBreakdown.length * 34, 160)}
          isEmpty={responses.length === 0}
          emptyMessage="Scores appear once feedback is submitted."
        >
          <HorizontalBarChart
            data={qualityOfCareBreakdown.map((q) => ({ label: q.label, value: q.score }))}
            domain={[0, 5]}
            colorMode="status"
            valueLabel={(v) => `${formatScore(v)}/5`}
          />
        </ChartCard>
      </Box>

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', lg: '1fr 1fr' }, gap: 3 }}>
        <ChartCard
          title="Environment Scores"
          description="Clinic cleanliness and waiting area comfort"
          height={Math.max(environmentScores.length * 34, 120)}
          isEmpty={responses.length === 0}
          emptyMessage="Scores appear once feedback is submitted."
        >
          <HorizontalBarChart
            data={environmentScores.map((q) => ({ label: q.label, value: q.score }))}
            domain={[0, 5]}
            colorMode="status"
            valueLabel={(v) => `${formatScore(v)}/5`}
          />
        </ChartCard>

        <ChartCard
          title="Affordability Scores"
          description="Cost, transparency, and payment satisfaction"
          height={Math.max(affordabilityScores.length * 34, 120)}
          isEmpty={responses.length === 0}
          emptyMessage="Scores appear once feedback is submitted."
        >
          <HorizontalBarChart
            data={affordabilityScores.map((q) => ({ label: q.label, value: q.score }))}
            domain={[0, 5]}
            colorMode="status"
            valueLabel={(v) => `${formatScore(v)}/5`}
          />
        </ChartCard>
      </Box>
    </Box>
  );
}
