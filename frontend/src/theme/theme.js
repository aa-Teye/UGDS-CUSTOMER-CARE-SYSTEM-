import { createTheme } from '@mui/material/styles';

// University of Ghana Dental School brand palette.
// Primary = UGDS blue, supporting colors carry semantic meaning
// (green = positive, red = complaint/issue, orange = warning, grey = neutral).
export const ugdsPalette = {
  blue: {
    darkest: '#052C4F',
    dark: '#0B3D66',
    main: '#0B4F8A',
    light: '#3E7CB1',
    lightest: '#EAF2FA',
  },
  positive: '#2E7D32',
  complaint: '#C62828',
  warning: '#ED6C02',
  neutral: '#64748B',
};

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: ugdsPalette.blue.main,
      dark: ugdsPalette.blue.dark,
      light: ugdsPalette.blue.light,
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: ugdsPalette.blue.light,
      contrastText: '#FFFFFF',
    },
    success: {
      main: ugdsPalette.positive,
    },
    error: {
      main: ugdsPalette.complaint,
    },
    warning: {
      main: ugdsPalette.warning,
    },
    grey: {
      500: ugdsPalette.neutral,
    },
    background: {
      default: '#F4F7FB',
      paper: '#FFFFFF',
    },
    text: {
      primary: '#1A2733',
      secondary: '#54636F',
    },
    divider: '#E1E7EF',
  },
  shape: {
    borderRadius: 10,
  },
  typography: {
    fontFamily: '"Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    h1: { fontWeight: 700 },
    h2: { fontWeight: 700 },
    h3: { fontWeight: 700 },
    h4: { fontWeight: 700 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
    button: { fontWeight: 600 },
  },
  components: {
    MuiButton: {
      defaultProps: { disableElevation: true },
      styleOverrides: {
        root: { textTransform: 'none', borderRadius: 8 },
      },
    },
    MuiCard: {
      defaultProps: { elevation: 0 },
      styleOverrides: {
        root: {
          border: '1px solid #E1E7EF',
          borderRadius: 12,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: { backgroundImage: 'none' },
      },
    },
    MuiAppBar: {
      defaultProps: { color: 'inherit', elevation: 0 },
      styleOverrides: {
        root: { borderBottom: '1px solid #E1E7EF' },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: { fontWeight: 600 },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        head: { fontWeight: 700, color: '#54636F' },
      },
    },
  },
});

export default theme;
