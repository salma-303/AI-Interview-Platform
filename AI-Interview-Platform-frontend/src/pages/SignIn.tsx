import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { signin } from '@/api/auth';
import { useToast } from '@/components/ui/use-toast';
import { useAuth } from '@/contexts/AuthContext';

import '@/components/ui/auth.css';

// Define schema with strict validation
const signInSchema = z.object({
  email: z.string().email({ message: 'Please enter a valid email address' }).min(1, { message: 'Email is required' }),
  password: z.string().min(6, { message: 'Password must be at least 6 characters' }),
});

// Explicitly define form type to avoid inference issues
interface SignInFormValues {
  email: string;
  password: string;
}

const SignIn: React.FC = () => {
  const { toast } = useToast();
  const { login } = useAuth();

  const form = useForm<SignInFormValues>({
    resolver: zodResolver(signInSchema),
    defaultValues: {
      email: '',
      password: '',
    },
    mode: 'onSubmit',
  });

  const onSubmit = async (data: SignInFormValues) => {
    try {
      const res = await signin(data);
      console.log(`Logged in as ${data.email}. Token: ${res.access_token.slice(0, 20)}...`);
      await login(data.email, data.password);
      toast({
        title: 'Success',
        description: 'Signed in successfully!',
      });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Sign-in failed. Please try again.';
      toast({
        title: 'Error',
        description: errorMessage,
        variant: 'destructive',
      });
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

                <Button type="submit" className="w-full">
                  Sign In
                </Button>
              </form>
            </Form>

            <div className="mt-6 text-center text-sm">
              Don't have an account?{' '}
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