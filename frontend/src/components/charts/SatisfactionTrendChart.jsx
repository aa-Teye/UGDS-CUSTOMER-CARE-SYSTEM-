import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ugdsPalette } from '../../theme/theme';

export default function SatisfactionTrendChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data} margin={{ top: 8, right: 12, bottom: 0, left: -12 }}>
        <CartesianGrid vertical={false} stroke="#E1E0D9" />
        <XAxis dataKey="week" tick={{ fontSize: 12, fill: '#898781' }} axisLine={{ stroke: '#C3C2B7' }} tickLine={false} />
        <YAxis
          domain={[0, 5]}
          tick={{ fontSize: 12, fill: '#898781' }}
          axisLine={false}
          tickLine={false}
          width={28}
        />
        <Tooltip
          formatter={(value) => [`${Number(value).toFixed(1)}/5`, 'Avg. satisfaction']}
          contentStyle={{ borderRadius: 8, border: '1px solid #E1E7EF', fontSize: 13 }}
        />
        <Line
          type="monotone"
          dataKey="avgSatisfaction"
          stroke={ugdsPalette.blue.main}
          strokeWidth={2}
          dot={{ r: 4, fill: ugdsPalette.blue.main, stroke: '#fff', strokeWidth: 2 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
