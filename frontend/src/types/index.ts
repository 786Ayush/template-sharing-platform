export interface User {
  id: string;
  email: string;
  username: string;
  role: 'admin' | 'user';
  created_at: string;
}

export interface Template {
  _id: string;
  title: string;
  description: string;
  image_url: string;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

export interface TemplateState {
  templates: Template[];
  selectedTemplate: Template | null;
  loading: boolean;
  error: string | null;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  role: 'admin' | 'user';
}

export interface CreateTemplateData {
  title: string;
  description: string;
  image: File;
}

export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}
