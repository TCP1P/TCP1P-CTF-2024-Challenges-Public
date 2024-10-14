"use client"
import { FormEvent, useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import { getCSRF } from "../_utils/getCSRF";

export default function Page() {
    const [note, setNote] = useState<string>('');
    const [password, setPassword] = useState<string>('');

    const onSave = async () => {
        try {
            const data = new FormData()
            data.append("note", note)
            data.append("password", password)
            const headers = new Headers()
            headers.set("X-CSRF-Token", await getCSRF())
            const response = await fetch('/api/note/set', {
                method: 'POST',
                body: data,
                headers: headers
            });

            if (response.ok) {
                toast.info('Succesfully save note');
            } else {
                toast.error('Failed to save note');
            }
        } catch (error) {
            toast.error('Error during saving note. Please try again later.');
        }
    }
    const onLoad = async () => {
        try {
            const data = new FormData()
            data.append("password", password)
            const headers = new Headers()
            headers.set("X-CSRF-Token", await getCSRF())
            const response = await fetch('/api/note/get', {
                method: 'POST',
                body: data,
                headers: headers
            });

            if (response.ok) {
                toast.info("Here's your note! "+await response.text());
            } else {
                toast.error('Failed to load note');
            }
        } catch (error) {
            toast.error('Error during loading note. Please try again later.');
        }
    }
    return (
        <>
            <div className='grid'>
                <div className="flex flex-row h-screen mx-10 place-self-center">
                    <form className="form-control w-full max-w-xs place-self-center text-center">
                        <h1 className="text-4xl">Save your note!</h1>
                        <label className="form-control w-full max-w-xs">
                            <div className="label">
                                <span className="label-text">Note</span>
                            </div>
                            <input
                                type="text"
                                className="input input-bordered w-full max-w-xs"
                                placeholder="Enter your note"
                                value={note}
                                onChange={(e) => setNote(e.target.value)}
                            />
                        </label>
                        <label className="form-control w-full max-w-xs mt-4">
                            <div className="label">
                                <span className="label-text">Password</span>
                            </div>
                            <input
                                type="password"
                                placeholder="Enter The Password"
                                className="input input-bordered w-full max-w-xs"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </label>
                        <button type="button" className="btn mt-4" onClick={onSave}>
                            Save
                        </button>
                        <button type="button" className="btn mt-4" onClick={onLoad}>
                            Load
                        </button>
                    </form>
                </div>
            </div>

            <ToastContainer position="bottom-right" />
        </>
    );
}
