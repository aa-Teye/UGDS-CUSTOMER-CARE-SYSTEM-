import { mockResponses } from '../data/mockResponses';
import { createStore } from './store';
import { simulateRequest } from './api';

export const responsesStore = createStore(mockResponses);

export async function fetchResponses() {
  return simulateRequest(responsesStore.getState());
}

export async function submitSurveyResponse(formData) {
  const response = {
    id: `response-${Date.now()}`,
    clinic: formData.visit.clinic,
    submittedAt: new Date().toISOString(),
    ...formData,
  };

  responsesStore.setState((responses) => [...responses, response]);

  return simulateRequest(response, { delay: 900 });
}
