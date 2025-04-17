import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Upload, Video, CheckCircle, LogOut } from "lucide-react";
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

  const jobs = [
    {
      id: 1,
      title: "Software Engineer",
      brief: "Develop and maintain web applications.",
      description: "We are looking for a Software Engineer to join our team. Responsibilities include developing and maintaining web applications, collaborating with cross-functional teams, and ensuring high performance and scalability."
    },
    {
      id: 2,
      title: "Data Scientist",
      brief: "Analyze data to provide business insights.",
      description: "As a Data Scientist, you will analyze large datasets to extract meaningful insights, build predictive models, and support data-driven decision-making processes."
    },
    {
      id: 3,
      title: "Product Manager",
      brief: "Oversee product development lifecycle.",
      description: "The Product Manager will oversee the product development lifecycle, define product requirements, and work closely with engineering and design teams to deliver high-quality products."
    }
  ];

  const [selectedJob, setSelectedJob] = useState<number | null>(null);

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

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
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

      {/* Job Browsing Section */}
      <div className="job-browsing-section">
  <h2 className="text-xl font-bold mb-4">Browse Jobs</h2>
  <div className="grid grid-cols-1 gap-4">
    {jobs.map(job => (
      <Card key={job.id} className="cursor-pointer">
        <CardHeader onClick={() => setSelectedJob(job.id)}>
          <CardTitle>{job.title}</CardTitle>
          <CardDescription>{job.brief}</CardDescription>
        </CardHeader>
        <CardFooter>
          <Button 
            size="sm" 
            className="ml-auto" 
            onClick={() => navigate("/upload-cv")}
          >
            Apply
          </Button>
        </CardFooter>
      </Card>
    ))}
  </div>

  {selectedJob !== null && (
    <div className="mt-6">
      <Card>
        <CardHeader>
          <CardTitle>{jobs.find(job => job.id === selectedJob)?.title}</CardTitle>
        </CardHeader>
        <CardContent>
          <p>{jobs.find(job => job.id === selectedJob)?.description}</p>
        </CardContent>
        <CardFooter>
          <Button className="w-full" onClick={() => alert("Applied for the job!")}>
            Apply
          </Button>
        </CardFooter>
      </Card>
    </div>
  )}
</div>
    </div>
  );
};

export default Dashboard;