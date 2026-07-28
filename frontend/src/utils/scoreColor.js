import { ugdsPalette } from '../theme/theme';

// Consistent score -> semantic color mapping used across dashboard/analytics
// (green = good, orange = needs attention, red = poor) on a 1-5 scale.
export function getScoreColor(score) {
  if (score === null || score === undefined) return 'grey';
  if (score >= 4) return 'success';
  if (score >= 3) return 'warning';
  return 'error';
}

// Hex equivalents for chart marks (Recharts fills take raw color values, not
// MUI palette keys).
export function getScoreHex(score) {
  if (score === null || score === undefined) return '#C3C2B7';
  if (score >= 4) return ugdsPalette.positive;
  if (score >= 3) return ugdsPalette.warning;
  return ugdsPalette.complaint;
}
