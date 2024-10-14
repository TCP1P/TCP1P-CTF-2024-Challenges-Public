"use client"
import React, { createContext, useContext, ReactNode, useState } from 'react';

interface AuthContextProps {
  username: string;
  password: string;
  setUsername: React.Dispatch<React.SetStateAction<string>>;
  setPassword: React.Dispatch<React.SetStateAction<string>>;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  return (
    <AuthContext.Provider value={{ username, password, setUsername, setPassword }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
