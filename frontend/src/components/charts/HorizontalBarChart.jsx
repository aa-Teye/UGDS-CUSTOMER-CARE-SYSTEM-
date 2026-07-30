import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell, LabelList, ResponsiveContainer } from 'recharts';
import { ugdsPalette } from '../../theme/theme';
import { getScoreHex } from '../../utils/scoreColor';

// Reusable horizontal bar chart. colorMode="status" tints each bar by score
// (green/orange/red, matching the dashboard's score-reading convention);
// colorMode="sequential" (the default) uses a single UGDS-blue hue, which is
// the correct choice whenever bars represent plain counts rather than scores.
export default function HorizontalBarChart({ data, domain, colorMode = 'sequential', valueLabel }) {
  const rowHeight = 34;
  const chartHeight = Math.max(data.length * rowHeight, 120);

  return (
    <ResponsiveContainer width="100%" height={chartHeight}>
      <BarChart data={data} layout="vertical" margin={{ top: 4, right: 28, bottom: 4, left: 4 }}>
        <CartesianGrid horizontal={false} stroke="#E1E0D9" />
        <XAxis type="number" domain={domain} hide />
        <YAxis
          type="category"
          dataKey="label"
          width={170}
          tick={{ fontSize: 12, fill: '#52514E' }}
          axisLine={false}
          tickLine={false}
        />
        <Tooltip
          formatter={(value) => [valueLabel ? valueLabel(value) : value, '']}
          contentStyle={{ borderRadius: 8, border: '1px solid #E1E7EF', fontSize: 13 }}
        />
        <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={16}>
          {data.map((entry) => (
            <Cell key={entry.label} fill={colorMode === 'status' ? getScoreHex(entry.value) : ugdsPalette.blue.main} />
          ))}
          <LabelList
            dataKey="value"
            position="right"
            formatter={(value) => (valueLabel ? valueLabel(value) : value)}
            style={{ fontSize: 12, fill: '#52514E', fontWeight: 600 }}
          />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
