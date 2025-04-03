
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Upload, Video, FileText, CheckCircle, LogOut } from "lucide-react";
import { useAuth } from '@/contexts/AuthContext';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const dashboardItems = [
    {
      title: "Upload CV",
      description: "Upload your resume for AI analysis before the interview",
      icon: <Upload className="h-10 w-10 text-primary" />,
      path: "/upload-cv",
      buttonText: "Upload CV"
    },
    {
      title: "Start Interview",
      description: "Begin your AI-powered interview session",
      icon: <Video className="h-10 w-10 text-primary" />,
      path: "/interview",
      buttonText: "Start Interview"
    },
    {
      title: "Interview Results",
      description: "View feedback and results from your previous interviews",
      icon: <CheckCircle className="h-10 w-10 text-primary" />,
      path: "/results",
      buttonText: "View Results"
    }
  ];

  return (
    <div className="page-container">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="text-muted-foreground">Welcome, {user?.name || 'User'}!</p>
        </div>
        <Button variant="outline" onClick={logout}>
          <LogOut className="h-4 w-4 mr-2" />
          Sign Out
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {dashboardItems.map((item, index) => (
          <Card key={index} className="h-full">
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                {item.icon}
              </div>
              <CardTitle>{item.title}</CardTitle>
              <CardDescription>{item.description}</CardDescription>
            </CardHeader>
            <CardFooter>
              <Button 
                className="w-full" 
                onClick={() => navigate(item.path)}
              >
                {item.buttonText}
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
