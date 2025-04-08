import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useToast } from "@/hooks/use-toast";

interface User {
  id: string;
  email: string;
  name: string;
  role: string; // Add role property
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  register: (email: string, password: string, name: string, role: string) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  getUserRole: () => string | null; // Add getUserRole function
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { toast } = useToast();

  useEffect(() => {
    // Check if user is stored in localStorage
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const register = async (email: string, password: string, name: string, role: string) => {
    try {
      setLoading(true);
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API delay

      const newUser = { id: Date.now().toString(), email, name, role };
      localStorage.setItem('user', JSON.stringify(newUser));
      setUser(newUser);

      toast({
        title: "Registration successful",
        description: "Your account has been created.",
      });

      navigate(role === "HR Recruiter" ? '/dashboard-hr' : '/dashboard');
    } catch (error) {
      toast({
        title: "Registration failed",
        description: "Something went wrong. Please try again.",
        variant: "destructive",
      });
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API delay

      // Mock user data
      const mockUser = { id: '1', email, name: email.split('@')[0], role: email.includes("hr") ? "HR Recruiter" : "Employee" };
      localStorage.setItem('user', JSON.stringify(mockUser));
      setUser(mockUser);

      toast({
        title: "Login successful",
        description: "Welcome back!",
      });

      navigate(mockUser.role === "HR Recruiter" ? '/dashboard-hr' : '/dashboard');
    } catch (error) {
      toast({
        title: "Login failed",
        description: "Invalid email or password.",
        variant: "destructive",
      });
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('user');
    setUser(null);
    navigate('/login');
    toast({
      title: "Logged out",
      description: "You have been logged out successfully.",
    });
  };

  const getUserRole = (): string | null => {
    return user?.role || null; // Return the user's role or null if not logged in
  };

  return (
    <AuthContext.Provider value={{ user, loading, register, login, logout, getUserRole }}>
      {children}
    </AuthContext.Provider>
  );
};