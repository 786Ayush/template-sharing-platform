import axios, { AxiosResponse } from 'axios';
import { LoginCredentials, RegisterData, CreateTemplateData, ApiResponse, LoginResponse, Template } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
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
  login: async (credentials: LoginCredentials): Promise<LoginResponse> => {
    const response: AxiosResponse<LoginResponse> = await api.post('/auth/login', credentials);
    return response.data;
  },

  register: async (userData: RegisterData): Promise<ApiResponse> => {
    const response: AxiosResponse<ApiResponse> = await api.post('/auth/register', userData);
    return response.data;
  },
};

export const templateAPI = {
  getAll: async (): Promise<Template[]> => {
    const response: AxiosResponse<Template[]> = await api.get('/templates');
    return response.data;
  },

  getById: async (id: string): Promise<Template> => {
    const response: AxiosResponse<Template> = await api.get(`/templates/${id}`);
    return response.data;
  },

  create: async (templateData: CreateTemplateData): Promise<ApiResponse> => {
    const formData = new FormData();
    formData.append('title', templateData.title);
    formData.append('description', templateData.description);
    formData.append('image', templateData.image);

    const response: AxiosResponse<ApiResponse> = await api.post('/templates', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  update: async (id: string, templateData: Partial<CreateTemplateData>): Promise<ApiResponse> => {
    const formData = new FormData();
    if (templateData.title) formData.append('title', templateData.title);
    if (templateData.description) formData.append('description', templateData.description);
    if (templateData.image) formData.append('image', templateData.image);

    const response: AxiosResponse<ApiResponse> = await api.put(`/templates/${id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  delete: async (id: string): Promise<ApiResponse> => {
    const response: AxiosResponse<ApiResponse> = await api.delete(`/templates/${id}`);
    return response.data;
  },
};

export default api;
