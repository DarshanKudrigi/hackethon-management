import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getProfile: () => api.get('/auth/me'),
  updateProfile: (data) => api.put('/auth/me', data),
};

export const eventsAPI = {
  getAll: () => api.get('/events/'),
  getById: (id) => api.get(`/events/${id}`),
  create: (data) => api.post('/events/', data),
  update: (id, data) => api.put(`/events/${id}`, data),
  delete: (id) => api.delete(`/events/${id}`),
};

export const registrationsAPI = {
  getMyRegistrations: () => api.get('/registrations/my'),
  register: (eventId) => api.post('/registrations/', { event_id: eventId }),
  cancel: (registrationId) => api.delete(`/registrations/${registrationId}`),
  getAll: () => api.get('/registrations/'),
};

export const teamsAPI = {
  getEventTeams: (eventId) => api.get(`/teams/event/${eventId}`),
  getById: (id) => api.get(`/teams/${id}`),
  create: (data) => api.post('/teams/', data),
  addMember: (teamId, userId) => api.post(`/teams/${teamId}/members`, { user_id: userId }),
  removeMember: (teamId, userId) => api.delete(`/teams/${teamId}/members/${userId}`),
};

export const projectsAPI = {
  getTeamProjects: (teamId) => api.get(`/projects/team/${teamId}`),
  getById: (id) => api.get(`/projects/${id}`),
  create: (data) => api.post('/projects/', data),
  update: (id, data) => api.put(`/projects/${id}`, data),
  delete: (id) => api.delete(`/projects/${id}`),
};

export const evaluationsAPI = {
  getByProject: (projectId) => api.get(`/evaluations/project/${projectId}`),
  create: (data) => api.post('/evaluations/', data),
  update: (id, data) => api.put(`/evaluations/${id}`, data),
};

export default api;
