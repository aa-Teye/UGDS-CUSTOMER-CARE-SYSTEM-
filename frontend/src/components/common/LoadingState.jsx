import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';

export default function LoadingState({ message = 'Loading…', minHeight = 240 }) {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 1.5,
        minHeight,
        color: 'text.secondary',
      }}
    >
      <CircularProgress size={28} />
      <Typography variant="body2">{message}</Typography>
    </Box>
  );
}
