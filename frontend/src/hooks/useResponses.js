import { useSyncExternalStore } from 'react';
import { responsesStore } from '../services/feedbackService';

// Subscribes to the mock feedback response store so a survey submission on
// the public /survey route immediately shows up on the Dashboard,
// Responses, and Analytics pages within the same session.
export function useResponses() {
  return useSyncExternalStore(responsesStore.subscribe, responsesStore.getState);
}
