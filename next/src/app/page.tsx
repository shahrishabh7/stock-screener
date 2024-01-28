"use client";
import {
  useMutation,
  QueryClient,
  QueryClientProvider,
  useQuery,
} from "@tanstack/react-query";
import { unstable_noStore as noStore } from "next/cache";
import { useState } from "react";

const queryClient = new QueryClient();

interface TickerAnalysis {
  [key: string]: string;
}

export default function Home() {
  noStore();
  const [ticker, setTicker] = useState("");
  const [tickerAnalysis, setTickerAnalysis] = useState(null);
  console.log("tickerAnalysis", tickerAnalysis);

  const mutation = useMutation(
    ({ ticker }) => {
      return fetch(`http://localhost:8000/ticker`, {
        method: "POST",
        body: JSON.stringify({ ticker }),
        headers: {
          "Content-Type": "application/json",
        },
      }).then((res) => res.json());
    },
    {
      onSuccess: (data) => {
        console.log("Success:", data);
        setTickerAnalysis(data);
      },
      onError: (error) => {
        console.error("Error:", error);
      },
    },
  );

  const submitTicker = () => {
    mutation.mutate({ ticker });
  };

  return (
    <QueryClientProvider client={queryClient}>
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
            {mutation.isLoading ? (
              <div>Loading...</div>
            ) : (
              <>
                {mutation.isError ? (
                  <div>An error occurred: {mutation.error}</div>
                ) : null}
                {mutation.isSuccess ? <div>Submitted successfully!</div> : null}
              </>
            )}
          </div>
          {tickerAnalysis &&
            Object.entries(tickerAnalysis as TickerAnalysis).map(
              ([key, value]) => (
                <div key={key}>
                  <h2 className="mt-4 text-xl font-bold">{key}</h2>
                  <p>{value.toString()}</p>{" "}
                </div>
              ),
            )}
        </div>
      </main>
    </QueryClientProvider>
  );
}
