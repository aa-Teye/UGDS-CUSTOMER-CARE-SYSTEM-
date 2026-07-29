import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import { Menu as MenuIcon, LogOut, ChevronDown } from 'lucide-react';
import { NAV_ITEMS } from './navConfig';
import { useAuth } from '../../hooks/useAuth';
import { initials } from '../../utils/formatters';

export default function Topbar({ onMenuClick }) {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [anchorEl, setAnchorEl] = useState(null);

  const currentItem = NAV_ITEMS.find((item) => location.pathname.startsWith(item.to));

  const handleLogout = () => {
    setAnchorEl(null);
    logout();
    navigate('/login');
  };

  return (
    <AppBar position="sticky" sx={{ bgcolor: 'background.paper' }}>
      <Toolbar sx={{ gap: 1 }}>
        <IconButton onClick={onMenuClick} sx={{ display: { xs: 'inline-flex', md: 'none' } }}>
          <MenuIcon size={20} />
        </IconButton>
        <Typography variant="h6" fontWeight={700} sx={{ flex: 1 }}>
          {currentItem?.label ?? 'UGDS Feedback System'}
        </Typography>
        <Box
          onClick={(event) => setAnchorEl(event.currentTarget)}
          sx={{ display: 'flex', alignItems: 'center', gap: 1, cursor: 'pointer', px: 1, py: 0.5, borderRadius: 2, '&:hover': { bgcolor: 'action.hover' } }}
        >
          <Avatar sx={{ width: 34, height: 34, bgcolor: 'primary.light', fontSize: 14 }}>{initials(user?.name)}</Avatar>
          <Box sx={{ display: { xs: 'none', sm: 'block' }, textAlign: 'left' }}>
            <Typography variant="body2" fontWeight={600} lineHeight={1.2}>
              {user?.name}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Management / Dean
            </Typography>
          </Box>
          <ChevronDown size={16} />
        </Box>
        <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={() => setAnchorEl(null)}>
          <MenuItem onClick={handleLogout}>
            <ListItemIcon>
              <LogOut size={17} />
            </ListItemIcon>
            Log out
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
}
