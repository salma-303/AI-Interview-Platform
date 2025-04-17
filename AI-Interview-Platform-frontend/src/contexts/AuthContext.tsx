import React, { createContext, useState, useContext, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { useToast } from '@/components/ui/use-toast';
import { signin, signup, getCurrentUser } from '@/api/auth';

interface User {
  id: string;
  email: string;
  role: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  registerUser: (email: string, password: string, role: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      const data = await signin({ email, password });
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('email', email);

      const userData = await getCurrentUser(email);
      const user: User = {
        id: userData.id,
        email: userData.email,
        role: userData.role,
      };

      localStorage.setItem('user', JSON.stringify(user));
      setUser(user);

      toast({
        title: 'Login successful',
        description: `Welcome back!`,
      });

      navigate(user.role === 'admin' ? '/dashboard-hr' : '/dashboard');
    } catch (error: any) {
      toast({
        title: 'Login failed',
        description: error.response?.data?.detail || 'Invalid credentials',
        variant: 'destructive',
      });
      console.error('Login error:', error);
    } finally {
      setLoading(false);
    }
  };

  const registerUser = async (email: string, password: string, role: string) => {
    try {
      setLoading(true);

      // Call signup
      await signup({ email, password, role });

      // Auto-login after signup
      const signInData = await signin({ email, password });
      localStorage.setItem('token', signInData.access_token);
      localStorage.setItem('email', email);

      const userData = await getCurrentUser(email);
      const user: User = {
        id: userData.id,
        email: userData.email,
        role: userData.role,
      };

      localStorage.setItem('user', JSON.stringify(user));
      setUser(user);

      toast({
        title: 'Registration successful',
        description: `Welcome!`,
      });

      navigate(user.role === 'admin' ? '/dashboard-hr' : '/dashboard');
    } catch (error: any) {
      toast({
        title: 'Registration failed',
        description: error.response?.data?.detail || 'Could not create account',
        variant: 'destructive',
      });
      console.error('Registration error:', error);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    localStorage.removeItem('email');
    navigate('/signin');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, registerUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};