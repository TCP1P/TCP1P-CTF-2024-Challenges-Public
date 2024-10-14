"use client"
import { useRouter } from 'next/navigation';
import React, { FormEvent, useState } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import { useAuth } from '../_utils/AuthContext';
import { getCSRF } from '../_utils/getCSRF';

export default function Register() {
    const router = useRouter()

    const auth = useAuth()

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        try {
            const data = new FormData()
            data.append("username", auth.username)
            data.append("password", auth.password)
            const headers = new Headers()
            headers.set("X-CSRF-Token", await getCSRF())
            const response = await fetch('/api/register', {
                method: 'POST',
                body: data,
                headers: headers
            });

            if (response.ok) {
                toast.info('Register Success.');
                router.push("/dashboard")
            } else {
                toast.error('Register failed. ' + await response.text());
            }
        } catch (error) {
            toast.error('Error during register. Please try again later.');
        }
    };

    return (
        <>
            <div className="grid h-screen">
                <form className="form-control w-full max-w-xs place-self-center text-center" onSubmit={handleSubmit}>
                    <h1 className='text-4xl'>Register</h1>
                    <div className="label">
                        <span className="label-text">Username</span>
                    </div>
                    <input
                        type="text"
                        placeholder="Type here"
                        className="input input-bordered w-full max-w-xs"
                        value={auth.username}
                        onChange={(e) => auth.setUsername(e.target.value)}
                    />

                    <div className="label mt-4">
                        <span className="label-text">Password</span>
                    </div>
                    <input
                        type="password"
                        placeholder="Enter your password"
                        className="input input-bordered w-full max-w-xs"
                        value={auth.password}
                        onChange={(e) => auth.setPassword(e.target.value)}
                    />

                    <button type="submit" className="btn mt-4">
                        Login
                    </button>
                    <p>Already have an account? <a className='link-primary' onClick={() => router.push("/login")}>Sign In</a></p>
                </form>
            </div>
            <ToastContainer position="bottom-right" />
        </>
    );
}
