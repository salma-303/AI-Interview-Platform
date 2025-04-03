
import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { ArrowLeft, Mic, MicOff, Send, Video, VideoOff } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface Message {
  id: string;
  content: string;
  sender: 'ai' | 'user';
  timestamp: Date;
}

const mockQuestions = [
  "Tell me about yourself and your background.",
  "What are your greatest strengths and how have you applied them in your work?",
  "Can you describe a challenging situation you faced at work and how you handled it?",
  "Why are you interested in this position?",
  "Where do you see yourself in 5 years?",
  "Do you have any questions for me about the role or company?"
];

const Interview: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isVideoOn, setIsVideoOn] = useState(true);
  const [isAudioOn, setIsAudioOn] = useState(true);
  const [isInterviewStarted, setIsInterviewStarted] = useState(false);
  const [isInterviewEnded, setIsInterviewEnded] = useState(false);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();
  const navigate = useNavigate();
  
  useEffect(() => {
    if (isInterviewStarted && messages.length === 0) {
      // Add initial greeting
      setTimeout(() => {
        addMessage("Hello! I'm your AI interviewer today. I'll be asking you a series of questions to learn more about your skills and experience. Are you ready to begin?", 'ai');
      }, 1000);
    }
  }, [isInterviewStarted]);
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  const addMessage = (content: string, sender: 'ai' | 'user') => {
    const newMessage: Message = {
      id: Date.now().toString(),
      content,
      sender,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, newMessage]);
  };
  
  const handleSendMessage = () => {
    if (!inputValue.trim()) return;
    
    // Add user message
    addMessage(inputValue, 'user');
    setInputValue('');
    setIsLoading(true);
    
    // Simulate AI response
    setTimeout(() => {
      if (currentQuestionIndex < mockQuestions.length) {
        addMessage(mockQuestions[currentQuestionIndex], 'ai');
        setCurrentQuestionIndex(prev => prev + 1);
      } else {
        addMessage("Thank you for participating in this interview. We've now completed all the questions. I'll analyze your responses and provide feedback. You can end the interview now.", 'ai');
        setIsInterviewEnded(true);
      }
      setIsLoading(false);
    }, 1500);
  };
  
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };
  
  const startInterview = () => {
    setIsInterviewStarted(true);
    toast({
      title: "Interview Started",
      description: "Your AI interview session has begun.",
    });
  };
  
  const endInterview = () => {
    navigate('/results');
  };
  
  const handleBack = () => {
    navigate('/dashboard');
  };

  return (
    <div className="interview-container">
      <div className="interview-header">
        <div className="flex justify-between items-center">
          <Button variant="ghost" onClick={handleBack} className="p-2">
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <h1 className="text-xl font-semibold">AI Interview Session</h1>
          <div className="space-x-2">
            <Button 
              variant="outline" 
              size="icon" 
              onClick={() => setIsVideoOn(!isVideoOn)}
              className={!isVideoOn ? 'bg-muted' : ''}
            >
              {isVideoOn ? <Video className="h-4 w-4" /> : <VideoOff className="h-4 w-4" />}
            </Button>
            <Button 
              variant="outline" 
              size="icon"
              onClick={() => setIsAudioOn(!isAudioOn)}
              className={!isAudioOn ? 'bg-muted' : ''}
            >
              {isAudioOn ? <Mic className="h-4 w-4" /> : <MicOff className="h-4 w-4" />}
            </Button>
          </div>
        </div>
      </div>
      
      <div className="interview-content">
        {!isInterviewStarted ? (
          <Card className="max-w-2xl mx-auto p-6 mt-10">
            <div className="text-center space-y-4">
              <h2 className="text-2xl font-bold">Ready for Your Interview?</h2>
              <p className="text-muted-foreground">
                You'll be interviewed by our AI assistant who will ask questions related to your experience and skills.
              </p>
              <p className="text-muted-foreground">
                Make sure your camera and microphone are working properly before starting.
              </p>
              <Button onClick={startInterview} className="mt-4">
                Start Interview
              </Button>
            </div>
          </Card>
        ) : (
          <div className="flex flex-col md:flex-row gap-4 h-full">
            <div className="w-full md:w-3/5 h-full flex flex-col">
              <div className="message-container flex-1 overflow-y-auto">
                {messages.map((message) => (
                  <div 
                    key={message.id} 
                    className={`flex ${message.sender === 'ai' ? 'justify-start' : 'justify-end'} mb-4`}
                  >
                    {message.sender === 'ai' && (
                      <Avatar className="h-8 w-8 mr-2">
                        <AvatarFallback>AI</AvatarFallback>
                      </Avatar>
                    )}
                    <div 
                      className={`px-4 py-2 rounded-lg max-w-[80%] ${
                        message.sender === 'ai' 
                          ? 'bg-muted text-foreground' 
                          : 'bg-primary text-primary-foreground'
                      }`}
                    >
                      {message.content}
                    </div>
                    {message.sender === 'user' && (
                      <Avatar className="h-8 w-8 ml-2">
                        <AvatarFallback>You</AvatarFallback>
                      </Avatar>
                    )}
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>
              
              <div className="p-4 border-t">
                <div className="flex items-center gap-2">
                  <Input
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type your response here..."
                    disabled={isLoading || isInterviewEnded}
                  />
                  <Button 
                    onClick={handleSendMessage} 
                    disabled={!inputValue.trim() || isLoading || isInterviewEnded}
                    size="icon"
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
                {isInterviewEnded && (
                  <Button onClick={endInterview} className="w-full mt-4">
                    End Interview & View Results
                  </Button>
                )}
              </div>
            </div>
            
            <div className="w-full md:w-2/5 bg-black rounded-lg flex items-center justify-center relative">
              {isVideoOn ? (
                <div className="text-white text-center p-4">
                  <p>Camera Preview</p>
                  <p className="text-sm text-gray-400">(Webcam access would be requested here)</p>
                </div>
              ) : (
                <div className="text-white text-center p-4">
                  <VideoOff className="h-12 w-12 mx-auto mb-2 text-gray-500" />
                  <p>Camera is turned off</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Interview;
