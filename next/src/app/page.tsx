"use client";
import { unstable_noStore as noStore } from "next/cache";
import Link from "next/link";
import { useState } from "react";
import { CreatePost } from "~/app/_components/create-post";
import { api } from "~/trpc/server";

export default function Home() {
  noStore();
  const [ticker, setTicker] = useState("");

  const submitTicker = async () => {
    const res = await fetch(`http://localhost:8000/ticker`, {
      method: "POST",
      body: JSON.stringify({ ticker }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await res.json();
    console.log(data);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-[#2e026d] to-[#15162c] text-white">
      <div className="container flex flex-col items-center justify-center gap-12 px-4 py-16 ">
        <h1 className="text-5xl font-extrabold tracking-tight sm:text-[5rem]">
          Stock <span className="text-[hsl(280,100%,70%)]">Screener</span>
        </h1>
        <div className="flex flex-col items-center gap-2"></div>
        <div className="flex flex-col items-center gap-2">
          <div className="text-lg font-medium">Enter a company ticker:</div>
          <input
            type="text"
            placeholder="e.g., AAPL"
            className="w-full max-w-xs rounded-md bg-white p-2 text-black shadow-sm focus:ring focus:ring-[hsl(280,100%,70%)] focus:ring-opacity-50"
            onChange={(e) => setTicker(e.target.value)}
          />
          <button onClick={submitTicker}>Submit</button>
        </div>
      </div>
    </main>
  );
}
