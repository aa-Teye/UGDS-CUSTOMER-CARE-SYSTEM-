// Minimal observable store used to back the mock services. Components read
// it through useSyncExternalStore (see hooks/) so any mutation from one
// page (e.g. Send Feedback) is instantly reflected everywhere else (e.g.
// Dashboard) within the same session, mirroring how a real query cache
// would behave once these services are swapped for HTTP calls.
export function createStore(initialState) {
  let state = initialState;
  const listeners = new Set();

  return {
    getState: () => state,
    setState: (updater) => {
      state = typeof updater === 'function' ? updater(state) : updater;
      listeners.forEach((listener) => listener());
    },
    subscribe: (listener) => {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
  };
}
