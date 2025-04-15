import api from './axiosfile';

interface UserSignIn {
  email: string;
  password: string;
}

interface UserSignUp {
  email: string;
  password: string;
  role: string;
  name?: string;
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
  name?: string;
}

export const signin = async (user: UserSignIn): Promise<SignInResponse> => {
  const response = await api.post<SignInResponse>('/signin', user);
  return response.data;
};

export const signup = async (user: UserSignUp): Promise<SignUpResponse> => {
  const response = await api.post<SignUpResponse>('/signup', user);
  return response.data;
};

export const getCurrentUser = async (email: string): Promise<User> => {
  const response = await api.get<User[]>('/users');
  const user = response.data.find((u) => u.email === email);
  if (!user) {
    throw new Error('User not found');
  }
  return user;
};