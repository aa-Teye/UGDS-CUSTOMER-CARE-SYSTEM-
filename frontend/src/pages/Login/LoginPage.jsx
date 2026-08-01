import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useLocation, useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';
import Stack from '@mui/material/Stack';
import { motion } from 'framer-motion';
import { ShieldCheck, Stethoscope } from 'lucide-react';
import BrandMark from '../../components/common/BrandMark';
import { useAuth } from '../../hooks/useAuth';

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [authError, setAuthError] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({ defaultValues: { username: '', password: '' } });

  const onSubmit = async ({ username, password }) => {
    setAuthError('');
    const result = login({ username, password });
    if (!result.success) {
      setAuthError(result.message);
      return;
    }
    const redirectTo = location.state?.from?.pathname ?? '/dashboard';
    navigate(redirectTo, { replace: true });
  };

  return (
    <Box sx={{ minHeight: '100vh', display: 'flex' }}>
      <Box
        sx={{
          flex: 1,
          display: { xs: 'none', md: 'flex' },
          flexDirection: 'column',
          justifyContent: 'space-between',
          bgcolor: 'primary.dark',
          background: 'linear-gradient(160deg, #0B4F8A 0%, #052C4F 100%)',
          color: '#fff',
          p: 6,
        }}
      >
        <BrandMark size="large" light />
        <Box>
          <Stethoscope size={40} />
          <Typography variant="h4" fontWeight={700} sx={{ mt: 2, mb: 1 }}>
            Patient Experience Feedback Management
          </Typography>
          <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.8)', maxWidth: 420 }}>
            Collect, monitor, and act on anonymous patient feedback across every clinic to continuously improve
            the quality of care at UGDS.
          </Typography>
        </Box>
        <Stack direction="row" spacing={1} alignItems="center" sx={{ color: 'rgba(255,255,255,0.65)' }}>
          <ShieldCheck size={16} />
          <Typography variant="caption">Management access only</Typography>
        </Stack>
      </Box>

      <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', p: 3 }}>
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
          style={{ width: '100%', maxWidth: 400 }}
        >
          <Box sx={{ display: { xs: 'flex', md: 'none' }, justifyContent: 'center', mb: 3 }}>
            <BrandMark size="large" />
          </Box>
          <Paper variant="outlined" sx={{ p: 4 }}>
            <Typography variant="h5" fontWeight={700}>
              Welcome back
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Sign in to view anonymous patient feedback and insights.
            </Typography>

            {authError && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {authError}
              </Alert>
            )}

            <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
              <Stack spacing={2}>
                <TextField
                  label="Username"
                  type="text"
                  fullWidth
                  autoComplete="username"
                  error={Boolean(errors.username)}
                  helperText={errors.username?.message}
                  {...register('username', { required: 'Username is required' })}
                />
                <TextField
                  label="Password"
                  type="password"
                  fullWidth
                  autoComplete="current-password"
                  error={Boolean(errors.password)}
                  helperText={errors.password?.message}
                  {...register('password', { required: 'Password is required' })}
                />
                <Button type="submit" variant="contained" size="large" disabled={isSubmitting} fullWidth>
                  {isSubmitting ? 'Signing in…' : 'Log In'}
                </Button>
              </Stack>
            </Box>
          </Paper>
        </motion.div>
      </Box>
    </Box>
  );
}
