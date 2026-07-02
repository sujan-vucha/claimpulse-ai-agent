import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.dispatchEvent(new Event('auth_unauthorized'));
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: async (username, password) => {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    const response = await api.post('/auth/login', params);
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },
  register: async (username, password, role, fullName) => {
    const response = await api.post('/auth/register', {
      username,
      password,
      role,
      full_name: fullName,
    });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },
  verifyToken: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

export const claimAPI = {
  verify: async (formData) => {
    const response = await api.post('/claims/verify', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  getAll: async () => {
    const response = await api.get('/claims');
    return response.data;
  },
  getById: async (id) => {
    const response = await api.get(`/claims/${id}`);
    return response.data;
  },
  runBatch: async (datasetName) => {
    const formData = new FormData();
    formData.append('dataset_name', datasetName);
    const response = await api.post('/claims/batch', formData);
    return response.data;
  },
  getAnalytics: async () => {
    const response = await api.get('/claims/analytics');
    return response.data;
  },
};

export default api;
