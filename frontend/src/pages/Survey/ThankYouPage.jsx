import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { motion } from 'framer-motion';
import { CheckCircle2 } from 'lucide-react';

export default function ThankYouPage() {
  return (
    <Box sx={{ textAlign: 'center', py: 6 }}>
      <motion.div
        initial={{ scale: 0.6, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: 'spring', stiffness: 200, damping: 14 }}
      >
        <Box
          sx={{
            width: 72,
            height: 72,
            borderRadius: '50%',
            bgcolor: 'success.main',
            color: '#fff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            mx: 'auto',
            mb: 3,
          }}
        >
          <CheckCircle2 size={36} />
        </Box>
      </motion.div>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 1 }}>
        Thank you for your feedback!
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ maxWidth: 360, mx: 'auto' }}>
        Your response has been submitted and will help us improve the quality of care at UGDS. You may now
        close this window.
      </Typography>
    </Box>
  );
}
