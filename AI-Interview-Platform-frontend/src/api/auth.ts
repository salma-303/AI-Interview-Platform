import api from './axiosfile';

interface UserSignIn {
  email: string;
  password: string;
}

interface UserSignUp {
  email: string;
  password: string;
  role: string;
}

interface SignInResponse {
  access_token: string;
  token_type: string;
}

interface SignUpResponse {
  message: string;
}

interface User {
  id: string;
  email: string;
  role: string;
}

export const signin = async (user: UserSignIn): Promise<SignInResponse> => {
  try {
    const response = await api.post<SignInResponse>('/signin', user);
    return response.data;
  } catch (error: any) {
    console.error(`Login failed: ${error.response?.data?.detail || error.message}`);
    throw error;
  }
};

export const signup = async (user: UserSignUp): Promise<SignUpResponse> => {
  try {
    const response = await api.post<SignUpResponse>('/signup', user);
    return response.data;
  } catch (error: any) {
    console.error(`Signup failed: ${error.response?.data?.detail || error.message}`);
    throw error;
  }
};

export const getCurrentUser = async (email: string): Promise<User> => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No token found in localStorage');
    }
    const response = await api.get<User[]>('/users', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const user = response.data.find((u) => u.email === email);
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  } catch (error: any) {
    console.error(`Get user failed: ${error.response?.data?.detail || error.message}`);
    throw error;
  }
};