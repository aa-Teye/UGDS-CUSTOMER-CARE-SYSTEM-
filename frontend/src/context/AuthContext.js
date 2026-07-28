import { createContext, createElement, useContext, useEffect, useMemo, useState } from 'react';
import { mockUsers } from '../data/mockUsers';

const AuthContext = createContext(null);
const STORAGE_KEY = 'ugds_auth_user';

function readStoredUser() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

// Mock authentication: validates against the demo account roster in
// data/mockUsers.js. Swapping in a real backend later only means replacing
// the body of `login` with an API call — the context surface stays the same.
export function AuthProvider({ children }) {
  const [user, setUser] = useState(readStoredUser);

  useEffect(() => {
    if (user) {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(user));
    } else {
      window.localStorage.removeItem(STORAGE_KEY);
    }
  }, [user]);

  const login = ({ username, password }) => {
    const match = mockUsers.find(
      (candidate) =>
        candidate.username.toLowerCase() === username.trim().toLowerCase() && candidate.password === password,
    );

    if (!match) {
      return { success: false, message: 'Invalid username or password.' };
    }

    const safeUser = { id: match.id, name: match.name, username: match.username };
    setUser(safeUser);
    return { success: true, user: safeUser };
  };

  const logout = () => setUser(null);

  const value = useMemo(() => ({ user, login, logout }), [user]);

  return createElement(AuthContext.Provider, { value }, children);
}

export function useAuthContext() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
}
