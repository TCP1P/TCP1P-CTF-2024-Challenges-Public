"use client"
import React, { useState } from 'react';

export default function Home() {
  const [payload, setPayload] = useState('');
  const [flashMessage, setFlashMessage] = useState('');

  const submitPayload = async () => {
    try {
      const response = await fetch('/api/payload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ payload }),
      });

      if (response.ok) {
        setFlashMessage('Payload submitted successfully!');
      } else {
        setFlashMessage('Failed to submit payload. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting payload:', error);
      setFlashMessage('An error occurred. Please try again later.');
    }
  };

  return (
    <main className="flex flex-col w-full border-opacity-50 min-h-screen">
      <div className="grid place-items-center min-h-screen">
        <div className="hero min-h-screen bg-base-200">
          <div className="hero-content text-center">
            <div className="max-w-md">
              <div className="flex flex-col gap-2">
                <h1 className="text-5xl font-bold">Add your payload here</h1>
                <input
                  type="text"
                  placeholder="Your Payload"
                  className="input input-bordered input-primary w-full max-w-full"
                  value={payload}
                  onChange={(e) => setPayload(e.target.value)}
                />
                <button className="btn btn-outline btn-primary" onClick={submitPayload}>
                  Submit
                </button>
                {flashMessage && <div>{flashMessage}</div>}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
