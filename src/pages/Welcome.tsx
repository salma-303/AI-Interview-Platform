import React from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from '@/contexts/AuthContext';
import { useNavigate, Link } from 'react-router-dom';


const Welcome: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/signin');
  };

  if (!user) {
    return (
        
            <div className="auth-container">
              <div className="auth-card">
                <div className="text-center mb-6">
                  <h1 className="text-3xl font-bold">AI Interviewer Platform</h1>
                  <p className="text-sm text-muted-foreground mt-2">
                    Prepare for your next interview with our AI-powered platform.
                  </p>
                </div>
      
                <Card>
                  <CardContent className="space-y-4">
                    <Button asChild>
                      <Link to="/signin" className="w-full">Sign In</Link>
                    </Button>
                    <Button asChild variant="outline">
                      <Link to="/signup" className="w-full">Sign Up</Link>
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </div>
          
    );
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold">Welcome, {user.email}!</h1>
          <p className="text-sm text-muted-foreground mt-2">
            You are now logged in.
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-xl">Your Account</CardTitle>
          </CardHeader>
          <CardContent>
            <p>
              Email: {user.email}
            </p>
            <Button className="mt-4 w-full" onClick={handleLogout}>
              Logout
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Welcome;