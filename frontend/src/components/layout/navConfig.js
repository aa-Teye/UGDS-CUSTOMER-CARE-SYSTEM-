import { LayoutDashboard, MessageSquare, BarChart3, Phone } from 'lucide-react';

export const NAV_ITEMS = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/analytics', label: 'Analytics', icon: BarChart3 },
  { to: '/responses', label: 'Responses', icon: MessageSquare },
  { to: '/follow-ups', label: 'Follow-up Requests', icon: Phone },
];
