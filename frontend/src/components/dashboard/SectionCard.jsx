import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

export default function SectionCard({ title, description, action, children, sx }) {
  return (
    <Paper variant="outlined" sx={{ p: 2.5, height: '100%', ...sx }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
        <Box>
          <Typography variant="subtitle1" fontWeight={700}>
            {title}
          </Typography>
          {description && (
            <Typography variant="caption" color="text.secondary">
              {description}
            </Typography>
          )}
        </Box>
        {action}
      </Box>
      {children}
    </Paper>
  );
}
