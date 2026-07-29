import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import { Stethoscope } from 'lucide-react';

export default function BrandMark({ size = 'medium', light = false }) {
  const iconBox = size === 'large' ? 52 : 36;
  const iconSize = size === 'large' ? 28 : 20;
  const titleVariant = size === 'large' ? 'h5' : 'subtitle1';

  return (
    <Stack direction="row" spacing={1.5} alignItems="center">
      <Box
        sx={{
          width: iconBox,
          height: iconBox,
          borderRadius: 2,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          bgcolor: light ? 'rgba(255,255,255,0.15)' : 'primary.main',
          color: '#fff',
          flexShrink: 0,
        }}
      >
        <Stethoscope size={iconSize} />
      </Box>
      <Box textAlign="left">
        <Typography variant={titleVariant} fontWeight={700} color={light ? '#fff' : 'text.primary'} lineHeight={1.1}>
          UGDS
        </Typography>
        <Typography variant="caption" color={light ? 'rgba(255,255,255,0.75)' : 'text.secondary'}>
          Patient Experience Feedback
        </Typography>
      </Box>
    </Stack>
  );
}
