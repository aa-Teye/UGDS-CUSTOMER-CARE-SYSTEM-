import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import { Outlet } from 'react-router-dom';
import BrandMark from '../common/BrandMark';

export default function PublicLayout() {
  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ bgcolor: 'primary.main', py: 2 }}>
        <Container maxWidth="sm">
          <BrandMark light />
        </Container>
      </Box>
      <Container maxWidth="sm" sx={{ flex: 1, py: { xs: 3, sm: 5 } }}>
        <Outlet />
      </Container>
    </Box>
  );
}
