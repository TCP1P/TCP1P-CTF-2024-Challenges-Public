"use client"

import Image from 'next/image';
import React, { useState, ChangeEvent, FormEvent } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import { getCSRF } from '../_utils/getCSRF';

interface Props {
    imgBlob: string | null
}

export default function ImageUpload({ imgBlob }: Props) {
    const [file, setFile] = useState<File | null>(null);
    const [xorString, setXorString] = useState<string>('');
    const [resultImage, setResultImage] = useState<string | null>(imgBlob); // New state for result image URL

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            setFile(e.target.files[0]);
        }
    };

    const handleXorStringChange = (e: ChangeEvent<HTMLInputElement>) => {
        setXorString(e.target.value);
    };

    function fileToBase64(file: File, callback: (value: string)=>void) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function () {
            callback((reader?.result as string).split(',')[1]);
        };
        reader.onerror = function (error) {
            console.error('Error reading file:', error);
        };
    }

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        if (!file) {
            toast.error('Please select a file.');
            return;
        }

        try {
            fileToBase64(file, async (image)=>{
                const data = new FormData();
                const reader = new FileReader();
                data.append('image', image);
                data.append('xorString', xorString);
                const headers = new Headers()
                headers.set("X-CSRF-Token", await getCSRF())
                const response = await fetch('/api/image/xor', {
                    method: 'POST',
                    body: data,
                    headers: headers
                });

                if (response.ok) {
                    const resultData = await response.blob();
                    const blobUrl = URL.createObjectURL(resultData)
                    setResultImage(blobUrl);
                    await fetch("/image/setimgblob?imgBlob="+blobUrl)
                    toast.info('Image XOR operation successful.');
                } else {
                    toast.error(await response.text());
                }
            })
        } catch (error) {
            console.error('Error during image XOR operation:', error);
            toast.error('Error during image XOR operation. Please try again later.');
        }
    };

    return (
        <>
            <div className='grid'>
                <div className="flex flex-row h-screen mx-10 place-self-center">
                    <form className="form-control w-full max-w-xs place-self-center text-center" onSubmit={handleSubmit}>
                        <h1 className="text-4xl">XOR Image</h1>
                        <label className="form-control w-full max-w-xs">
                            <div className="label">
                                <span className="label-text">Pick a file</span>
                            </div>
                            <input
                                type="file"
                                accept="image/*"
                                onChange={handleFileChange}
                                className="file-input file-input-bordered w-full max-w-xs"
                            />
                        </label>
                        <label className="form-control w-full max-w-xs mt-4">
                            <div className="label">
                                <span className="label-text">XOR String</span>
                            </div>
                            <input
                                type="text"
                                placeholder="Enter XOR String"
                                value={xorString}
                                onChange={handleXorStringChange}
                                className="input input-bordered w-full max-w-xs"
                            />
                        </label>
                        <button type="submit" className="btn mt-4">
                            XOR Image
                        </button>
                    </form>
                    <div className='divider divider-horizontal'></div>
                    <div className='card w-96 bg-base-100 shadow-xl artboard artboard-horizontal phone-1 border border-slate-400 max-w-xs place-self-center text-center'>
                        {resultImage && (
                            <div className="w-full place-self-center text-center">
                                <h2 className="text-2xl">Result Image:</h2>
                                <Image src={resultImage} width={400} height={400} alt='Result'></Image>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            <ToastContainer position="bottom-right" />
        </>
    );
}
