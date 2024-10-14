"use client"
import { useRouter } from "next/navigation";

export default function Home() {
    const router = useRouter();

    return (
        <main className="flex flex-col w-full border-opacity-50 min-h-screen">
            <div className="hero min-h-screen bg-base-200">
                <div className="hero-content text-center">
                    <div className="max-w-md">
                        <h1 className="text-5xl font-bold">Hello there</h1>
                        <p className="py-6">Welcome to our XOR Image Processor! This innovative application allows users to perform bitwise XOR operations on images, introducing a layer of encryption and customization to your visual content.</p>
                        <button className="btn btn-primary" onClick={()=>router.push("/image")}>Get Started</button>
                    </div>
                </div>
            </div>
        </main>
    );
}
