// Shared async-simulation helper. Every mock service resolves through this
// function so the async shape (Promise, latency, failure) already matches
// what a real FastAPI call via fetch/axios will look like — when the
// backend exists, only the body of each service function changes; call
// sites in hooks/components stay the same.
const DEFAULT_DELAY_MS = 500;

export function simulateRequest(data, { delay = DEFAULT_DELAY_MS, shouldFail = false, errorMessage } = {}) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (shouldFail) {
        reject(new Error(errorMessage || 'Request failed'));
        return;
      }
      resolve(data);
    }, delay);
  });
}
