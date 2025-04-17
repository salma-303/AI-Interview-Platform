import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { useAuth } from '@/contexts/AuthContext';
import { useToast } from '@/components/ui/use-toast';

import '@/components/ui/auth.css';

const signUpSchema = z.object({
  email: z.string().email({ message: 'Please enter a valid email address' }).min(1, { message: 'Email is required' }),
  password: z.string().min(6, { message: 'Password must be at least 6 characters' }),
  confirmPassword: z.string(),
  role: z.enum(['admin', 'user'], { message: 'Please select a role' }),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

interface SignUpFormValues {
  email: string;
  password: string;
  confirmPassword: string;
  role: 'admin' | 'user';
}

const SignUp: React.FC = () => {
  const { registerUser, loading } = useAuth();
  const { toast } = useToast();

  const form = useForm<SignUpFormValues>({
    resolver: zodResolver(signUpSchema),
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
      role: 'user',
    },
    mode: 'onSubmit',
  });

  const onSubmit = async (data: SignUpFormValues) => {
    try {
      console.log('Submitting sign-up with:', { email: data.email, role: data.role });
      await registerUser(data.email, data.password, data.role);
      // Toast and navigation handled in AuthContext
    } catch (error: any) {
      console.error('Sign-up error:', error.response?.data || error.message);
      toast({
        title: 'Registration failed',
        description: error.response?.data?.detail || error.message || 'Could not create account',
        variant: 'destructive',
      });
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold">AI Interviewer</h1>
          <p className="text-sm text-muted-foreground mt-2">Create your account to get started</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-xl">Sign Up</CardTitle>
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
                        <Input type="password" placeholder="Create a password" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="confirmPassword"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Confirm Password</FormLabel>
                      <FormControl>
                        <Input type="password" placeholder="Confirm your password" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="role"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Role</FormLabel>
                      <FormControl>
                        <select
                          value={field.value}
                          onChange={(e) => field.onChange(e.target.value as 'admin' | 'user')}
                          className="w-full p-2 border rounded"
                        >
                          <option value="user">Employee</option>
                          <option value="admin">HR Recruiter</option>
                        </select>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? 'Creating account...' : 'Create Account'}
                </Button>
              </form>
            </Form>

            <div className="mt-6 text-center text-sm">
              Already have an account?{' '}
              <Link to="/signin" className="font-medium text-primary hover:underline">
                Sign in
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default SignUp;