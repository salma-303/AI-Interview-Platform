
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Upload, FileText, CheckCircle, ArrowLeft } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const UploadCV: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const { toast } = useToast();
  const navigate = useNavigate();

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      if (validateFile(droppedFile)) {
        setFile(droppedFile);
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      if (validateFile(selectedFile)) {
        setFile(selectedFile);
      }
    }
  };

  const validateFile = (file: File) => {
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const maxSize = 5 * 1024 * 1024; // 5MB
    
    if (!validTypes.includes(file.type)) {
      toast({
        title: "Invalid file type",
        description: "Please upload a PDF or Word document.",
        variant: "destructive",
      });
      return false;
    }
    
    if (file.size > maxSize) {
      toast({
        title: "File too large",
        description: "Please upload a file smaller than 5MB.",
        variant: "destructive",
      });
      return false;
    }
    
    return true;
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setIsUploading(true);
    
    // Simulate upload progress
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        const newProgress = prev + 10;
        if (newProgress >= 100) {
          clearInterval(interval);
          setIsUploading(false);
          setIsAnalyzing(true);
          
          // Simulate CV analysis
          setTimeout(() => {
            setIsAnalyzing(false);
            setIsComplete(true);
            toast({
              title: "CV uploaded successfully",
              description: "Your resume has been analyzed and is ready for the interview.",
            });
          }, 2000);
          
          return 100;
        }
        return newProgress;
      });
    }, 300);
  };

  const handleBack = () => {
    navigate('/dashboard');
  };

  const goToInterview = () => {
    navigate('/interview');
  };

  return (
    <div className="page-container">
      <Button variant="ghost" onClick={handleBack} className="mb-4">
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Dashboard
      </Button>
      
      <h1 className="page-title">Upload Your CV</h1>
      
      <Card className="max-w-3xl mx-auto">
        <CardHeader>
          <CardTitle>Resume Upload</CardTitle>
          <CardDescription>
            Upload your CV or resume so our AI can personalize your interview experience
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          {!isUploading && !isAnalyzing && !isComplete ? (
            <div 
              className={`border-2 border-dashed rounded-lg p-12 text-center ${isDragging ? 'border-primary bg-primary/5' : 'border-input'}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              <div className="flex flex-col items-center justify-center gap-4">
                <Upload className="h-12 w-12 text-muted-foreground" />
                <div>
                  <p className="font-medium">Drag and drop your resume here</p>
                  <p className="text-sm text-muted-foreground mt-1">
                    Supports PDF, DOC, DOCX (Max 5MB)
                  </p>
                </div>
                
                <div className="mt-2">
                  <input
                    type="file"
                    id="resume-upload"
                    accept=".pdf,.doc,.docx"
                    className="hidden"
                    onChange={handleFileChange}
                  />
                  <label htmlFor="resume-upload">
                    <Button variant="outline" size="sm" className="cursor-pointer" asChild>
                      <span>Browse files</span>
                    </Button>
                  </label>
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {isUploading && (
                <>
                  <div className="flex items-center gap-4 mb-2">
                    <FileText className="h-8 w-8 text-primary" />
                    <div className="flex-1">
                      <p className="font-medium">{file?.name}</p>
                      <p className="text-sm text-muted-foreground">
                        Uploading: {uploadProgress}%
                      </p>
                    </div>
                  </div>
                  <Progress value={uploadProgress} className="h-2" />
                </>
              )}
              
              {isAnalyzing && (
                <div className="flex items-center gap-4 py-2">
                  <div className="animate-spin">
                    <FileText className="h-8 w-8 text-primary" />
                  </div>
                  <div>
                    <p className="font-medium">Analyzing your resume...</p>
                    <p className="text-sm text-muted-foreground">
                      Our AI is extracting key information from your resume
                    </p>
                  </div>
                </div>
              )}
              
              {isComplete && (
                <div className="flex items-center gap-4 py-2">
                  <CheckCircle className="h-8 w-8 text-green-500" />
                  <div>
                    <p className="font-medium">Resume processed successfully!</p>
                    <p className="text-sm text-muted-foreground">
                      Your resume has been analyzed and is ready for the interview
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}
        </CardContent>
        
        <CardFooter className="flex justify-end gap-3">
          {!isUploading && !isAnalyzing && !isComplete && file && (
            <Button onClick={handleUpload}>
              Upload CV
            </Button>
          )}
          
          {isComplete && (
            <Button onClick={goToInterview}>
              Continue to Interview
            </Button>
          )}
        </CardFooter>
      </Card>
    </div>
  );
};

export default UploadCV;
