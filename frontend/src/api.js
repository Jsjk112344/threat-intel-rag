import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const ingestCVEs = async (daysBack = 30, maxResults = 100) => {
  const response = await axios.post(`${API_BASE_URL}/api/ingest`, {
    days_back: daysBack,
    max_results: maxResults
  });
  return response.data;
};

export const queryThreats = async (query) => {
  const response = await axios.post(`${API_BASE_URL}/api/query`, {
    query: query
  });
  return response.data;
};