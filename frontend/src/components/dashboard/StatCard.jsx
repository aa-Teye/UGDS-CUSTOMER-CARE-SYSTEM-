import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

export default function StatCard({ icon: Icon, label, value, suffix, color = 'primary', onClick }) {
  return (
    <Paper
      variant="outlined"
      onClick={onClick}
      sx={{
        p: 2.5,
        display: 'flex',
        flexDirection: 'column',
        gap: 1,
        height: '100%',
        cursor: onClick ? 'pointer' : 'default',
        transition: 'border-color 0.15s, box-shadow 0.15s',
        '&:hover': onClick ? { borderColor: 'primary.main', boxShadow: 1 } : undefined,
      }}
    >
      <Box
        sx={{
          width: 36,
          height: 36,
          borderRadius: 2,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          bgcolor: `${color}.main`,
          color: '#fff',
          opacity: 0.9,
        }}
      >
        <Icon size={18} />
      </Box>
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
      <Typography variant="h4" fontWeight={700}>
        {value}
        {suffix && (
          <Typography component="span" variant="h6" color="text.secondary" fontWeight={600}>
            {' '}
            {suffix}
          </Typography>
        )}
      </Typography>
    </Paper>
  );
}
