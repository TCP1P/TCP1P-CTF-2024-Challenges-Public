"use client"
import { useRouter } from "next/navigation"

export function Navbar() {
    const router = useRouter()
    const list = <>
    </>
    return (
        <div className="navbar fixed">
            <div className="navbar-start">
                <div className="dropdown">
                    <div tabIndex={0} role="button" className="btn btn-ghost lg:hidden">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h8m-8 6h16" /></svg>
                    </div>
                    <ul tabIndex={0} className="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
                        {list}
                    </ul>
                </div>
                <a className="btn btn-ghost text-xl" onClick={() => router.push("/")}>daisyUI</a>
            </div>
            <div className="navbar-center hidden lg:flex">
                <ul className="menu menu-horizontal px-1">
                    {list}
                </ul>
            </div>
            <div className="navbar-end">
                <a className="btn" onClick={() => router.push("/note")}>Note</a>
                <a className="btn" onClick={() => router.push("/image")}>Image</a>
                <a className="btn" onClick={() => router.push("/login")}>Login</a>
            </div>
        </div>
    )
}
