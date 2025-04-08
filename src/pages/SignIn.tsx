/*
import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useAuth } from '@/contexts/AuthContext';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';

const signInSchema = z.object({
  email: z.string().email({ message: "Please enter a valid email address" }),
  password: z.string().min(1, { message: "Password is required" }),
});

type SignInFormValues = z.infer<typeof signInSchema>;

const SignIn: React.FC = () => {
  const { login, loading } = useAuth();
  const form = useForm<SignInFormValues>({
    resolver: zodResolver(signInSchema),
    defaultValues: {
      email: "",
      password: ""
    }
  });

  const onSubmit = async (data: SignInFormValues) => {
    await login(data.email, data.password);
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold">AI Interviewer</h1>
          <p className="text-sm text-muted-foreground mt-2">Sign in to your account</p>
        </div>
        
        <Card>
          <CardHeader>
            <CardTitle className="text-xl">Sign In</CardTitle>
          </CardHeader>
          <CardContent>
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Email</FormLabel>
                      <FormControl>
                        <Input type="email" placeholder="Enter your email" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Password</FormLabel>
                      <FormControl>
                        <Input type="password" placeholder="Enter your password" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? "Signing in..." : "Sign In"}
                </Button>
              </form>
            </Form>
            
            <div className="mt-6 text-center text-sm">
              Don't have an account?{" "}
              <Link to="/signup" className="font-medium text-primary hover:underline">
                Sign up
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default SignIn;
*/

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useAuth } from '@/contexts/AuthContext';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import '@/components/ui/auth.css'; // Import the new CSS file
import '../@/public/logo.ico';

const signInSchema = z.object({
  email: z.string().email({ message: "Please enter a valid email address" }),
  password: z.string().min(1, { message: "Password is required" }),
});

type SignInFormValues = z.infer<typeof signInSchema>;

const SignIn: React.FC = () => {
  const { login, loading, getUserRole } = useAuth();
  const navigate = useNavigate();
  const form = useForm<SignInFormValues>({
    resolver: zodResolver(signInSchema),
    defaultValues: {
      email: "",
      password: ""
    }
  });

  const onSubmit = async (data: SignInFormValues) => {
    await login(data.email, data.password);
    const role = getUserRole(); // Fetch the user's role after login
    console.log("User role:", role); // Debugging: Check the role value
    if (role === "HR Recruiter") {
      console.log("Navigating to HR Dashboard");
      navigate("/Dashboard_HR"); // Navigate to HR Dashboard
    } else {
      console.log("Navigating to Regular Dashboard");
      navigate("/Dashboard"); // Navigate to regular Dashboard
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold">AI Interviewer</h1>
          <p className="text-sm text-muted-foreground mt-2">Sign in to your account</p>
        </div>
        
        <Card>
          <CardHeader>
            <CardTitle className="text-xl">Sign In</CardTitle>
          </CardHeader>
          <CardContent>
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Email</FormLabel>
                      <FormControl>
                        <Input type="email" placeholder="Enter your email" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Password</FormLabel>
                      <FormControl>
                        <Input type="password" placeholder="Enter your password" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? "Signing in..." : "Sign In"}
                </Button>
              </form>
            </Form>
            
            <div className="mt-6 text-center text-sm">
              Don't have an account?{" "}
              <Link to="/signup" className="font-medium text-primary hover:underline">
                Sign up
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default SignIn;