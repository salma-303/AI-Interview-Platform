import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Plus, Trash, UserPlus, VideoOff, Video, FilePlus, FileMinus } from "lucide-react";

const DashboardHR: React.FC = () => {
  const [jobs, setJobs] = useState([
    { id: 1, title: "Software Engineer", brief: "Develop and maintain web applications." },
    { id: 2, title: "Data Scientist", brief: "Analyze data to provide business insights." },
  ]);

  const [users, setUsers] = useState([
    { id: 1, name: "John Doe", role: "Employee" },
    { id: 2, name: "Jane Smith", role: "HR Recruiter" },
  ]);

  const [cameraEnabled, setCameraEnabled] = useState(true);

  const addJob = () => {
    const newJob = { id: Date.now(), title: "New Job", brief: "Job description here." };
    setJobs([...jobs, newJob]);
  };

  const deleteJob = (id: number) => {
    setJobs(jobs.filter(job => job.id !== id));
  };

  const addUser = () => {
    const newUser = { id: Date.now(), name: "New User", role: "Employee" };
    setUsers([...users, newUser]);
  };

  const deleteUser = (id: number) => {
    setUsers(users.filter(user => user.id !== id));
  };

  const toggleCamera = () => {
    setCameraEnabled(!cameraEnabled);
  };

  return (
    <div className="page-container">
      <h1 className="page-title">HR Dashboard</h1>

      {/* Job Management Section */}
      <div className="mb-8">
        <h2 className="text-xl font-bold mb-4">Manage Jobs</h2>
        <Button onClick={addJob} className="mb-4">
          <Plus className="mr-2" /> Add Job
        </Button>
        <div className="grid grid-cols-1 gap-4">
          {jobs.map(job => (
            <Card key={job.id}>
              <CardHeader>
                <CardTitle>{job.title}</CardTitle>
                <CardDescription>{job.brief}</CardDescription>
              </CardHeader>
              <CardFooter>
                <Button size="sm" variant="destructive" onClick={() => deleteJob(job.id)}>
                  <Trash className="mr-2" /> Delete Job
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>

      {/* User Management Section */}
      <div className="mb-8">
        <h2 className="text-xl font-bold mb-4">Manage Users</h2>
        <Button onClick={addUser} className="mb-4">
          <UserPlus className="mr-2" /> Add User
        </Button>
        <div className="grid grid-cols-1 gap-4">
          {users.map(user => (
            <Card key={user.id}>
              <CardHeader>
                <CardTitle>{user.name}</CardTitle>
                <CardDescription>Role: {user.role}</CardDescription>
              </CardHeader>
              <CardFooter>
                <Button size="sm" variant="destructive" onClick={() => deleteUser(user.id)}>
                  <Trash className="mr-2" /> Delete User
                </Button>
                {user.role !== "HR Recruiter" && (
                  <Button size="sm" className="ml-2">
                    <UserPlus className="mr-2" /> Promote to Admin
                  </Button>
                )}
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>

      {/* Settings Section */}
      <div className="mb-8">
        <h2 className="text-xl font-bold mb-4">Settings</h2>
        <Card>
          <CardHeader>
            <CardTitle>Interview Camera</CardTitle>
            <CardDescription>
              {cameraEnabled ? "Camera is enabled for interviews." : "Camera is disabled for interviews."}
            </CardDescription>
          </CardHeader>
          <CardFooter>
            <Button onClick={toggleCamera}>
              {cameraEnabled ? <VideoOff className="mr-2" /> : <Video className="mr-2" />}
              {cameraEnabled ? "Disable Camera" : "Enable Camera"}
            </Button>
          </CardFooter>
        </Card>
      </div>

      {/* CV Management Section */}
      <div className="mb-8">
        <h2 className="text-xl font-bold mb-4">Manage CVs</h2>
        <Button className="mb-4">
          <FilePlus className="mr-2" /> Add CV
        </Button>
        <Button variant="destructive" className="ml-4">
          <FileMinus className="mr-2" /> Remove CV
        </Button>
      </div>
    </div>
  );
};

export default DashboardHR;