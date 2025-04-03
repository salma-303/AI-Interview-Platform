
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { ArrowLeft, Download, Share2 } from "lucide-react";
import { 
  Accordion, 
  AccordionContent, 
  AccordionItem, 
  AccordionTrigger 
} from "@/components/ui/accordion";

const Results: React.FC = () => {
  const navigate = useNavigate();
  
  const skillScores = [
    { name: "Communication", score: 85 },
    { name: "Technical Knowledge", score: 92 },
    { name: "Problem Solving", score: 78 },
    { name: "Cultural Fit", score: 88 },
    { name: "Leadership", score: 72 }
  ];
  
  const questionFeedback = [
    {
      question: "Tell me about yourself and your background.",
      feedback: "Strong introduction with clear articulation of relevant experience. Could benefit from more concise delivery and focus on recent achievements."
    },
    {
      question: "What are your greatest strengths and how have you applied them in your work?",
      feedback: "Excellent examples provided that demonstrate both technical and soft skills. The connection between strengths and outcomes was well established."
    },
    {
      question: "Can you describe a challenging situation you faced at work and how you handled it?",
      feedback: "Good use of the STAR method to structure your response. Consider emphasizing the measurable results more clearly to showcase impact."
    },
    {
      question: "Why are you interested in this position?",
      feedback: "Demonstrated good research about the role and company. Could further highlight alignment between personal career goals and company mission."
    },
    {
      question: "Where do you see yourself in 5 years?",
      feedback: "Showed ambition while remaining realistic. Response could be strengthened by connecting long-term goals more explicitly to the current role."
    }
  ];
  
  const handleBack = () => {
    navigate('/dashboard');
  };
  
  const handleDownload = () => {
    // In a real app, this would generate and download a PDF report
    alert("In a real application, this would download a PDF of the interview results.");
  };
  
  const handleShare = () => {
    // In a real app, this would open a sharing dialog
    alert("In a real application, this would open options to share the results.");
  };
  
  // Calculate overall score (average of all skill scores)
  const overallScore = Math.round(
    skillScores.reduce((sum, skill) => sum + skill.score, 0) / skillScores.length
  );
  
  return (
    <div className="page-container">
      <Button variant="ghost" onClick={handleBack} className="mb-4">
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Dashboard
      </Button>
      
      <div className="flex justify-between items-center mb-6">
        <h1 className="page-title">Interview Results</h1>
        <div className="space-x-2">
          <Button variant="outline" onClick={handleDownload}>
            <Download className="h-4 w-4 mr-2" />
            Download Report
          </Button>
          <Button variant="outline" onClick={handleShare}>
            <Share2 className="h-4 w-4 mr-2" />
            Share Results
          </Button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Overall Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col items-center justify-center">
              <div className="relative w-40 h-40 mb-4">
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-4xl font-bold">{overallScore}%</span>
                </div>
                <svg className="w-full h-full" viewBox="0 0 100 100">
                  <circle
                    className="text-muted stroke-current"
                    strokeWidth="10"
                    fill="transparent"
                    r="40"
                    cx="50"
                    cy="50"
                  />
                  <circle
                    className="text-primary stroke-current"
                    strokeWidth="10"
                    strokeLinecap="round"
                    fill="transparent"
                    r="40"
                    cx="50"
                    cy="50"
                    strokeDasharray={`${2 * Math.PI * 40}`}
                    strokeDashoffset={`${2 * Math.PI * 40 * (1 - overallScore / 100)}`}
                    transform="rotate(-90 50 50)"
                  />
                </svg>
              </div>
              <p className="text-xl font-semibold mb-2">
                {overallScore >= 90 
                  ? "Excellent" 
                  : overallScore >= 80 
                  ? "Very Good" 
                  : overallScore >= 70 
                  ? "Good" 
                  : overallScore >= 60 
                  ? "Satisfactory" 
                  : "Needs Improvement"}
              </p>
              <p className="text-center text-muted-foreground">
                Based on your responses and communication during the interview
              </p>
            </div>
          </CardContent>
        </Card>
        
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Skill Assessment</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {skillScores.map((skill) => (
                <div key={skill.name} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-medium">{skill.name}</span>
                    <span className="text-sm font-medium">{skill.score}%</span>
                  </div>
                  <Progress value={skill.score} className="h-2" />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
        
        <Card className="lg:col-span-3">
          <CardHeader>
            <CardTitle>Question Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <Accordion type="single" collapsible className="w-full">
              {questionFeedback.map((item, index) => (
                <AccordionItem key={index} value={`item-${index}`}>
                  <AccordionTrigger>
                    <span className="text-left font-medium">{item.question}</span>
                  </AccordionTrigger>
                  <AccordionContent>
                    <div className="p-4 bg-muted rounded-md">
                      <p className="text-sm">{item.feedback}</p>
                    </div>
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </CardContent>
        </Card>
        
        <Card className="lg:col-span-3">
          <CardHeader>
            <CardTitle>Summary & Recommendations</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <p>
                You demonstrated strong communication skills and technical knowledge throughout the interview. 
                Your responses were generally well-structured and showcased relevant experience.
              </p>
              <p className="font-semibold">Strengths:</p>
              <ul className="list-disc list-inside space-y-1 ml-4">
                <li>Excellent articulation of technical concepts</li>
                <li>Strong examples of past achievements</li>
                <li>Good understanding of role requirements</li>
                <li>Positive attitude and engagement</li>
              </ul>
              <p className="font-semibold mt-4">Areas for Improvement:</p>
              <ul className="list-disc list-inside space-y-1 ml-4">
                <li>Be more concise in responses to behavioral questions</li>
                <li>Further highlight measurable impacts and outcomes</li>
                <li>Provide more specific examples when discussing leadership experience</li>
              </ul>
              <p className="mt-4">
                Overall, your performance in this interview was strong. Continue focusing on highlighting 
                specific achievements with measurable results and consider practicing more concise delivery 
                for future interviews.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Results;
