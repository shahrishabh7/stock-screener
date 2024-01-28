"use client";
import {
  useMutation,
  QueryClient,
  QueryClientProvider,
  useQuery,
} from "@tanstack/react-query";
import { unstable_noStore as noStore } from "next/cache";
import { useState } from "react";
import { formatHeader } from "~/utils/headingFormatter";

const queryClient = new QueryClient();

interface TickerAnalysis {
  [key: string]: string;
}

export default function Home() {
  noStore();
  const [ticker, setTicker] = useState("");
  const [tickerAnalysis, setTickerAnalysis] = useState(null);

  const mutation = useMutation(
    ({ ticker }) => {
      return fetch(`http://localhost:8000/mock/ticker`, {
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
      <main className="bg--w flex min-h-screen flex-col items-center justify-center text-white">
        <div className="container flex flex-col items-center justify-center gap-12 px-4 py-16 ">
          <h1 className="text-5xl font-extrabold tracking-tight text-black sm:text-[5rem]">
            Stock <span className="text-[hsl(284,7%,71%)]">Screener</span>
          </h1>
          <div className="flex flex-col items-center gap-2"></div>
          <div className="flex flex-col items-center gap-2">
            <div className="text-lg font-medium text-black">
              Enter a company ticker:
            </div>
            <input
              type="text"
              placeholder="e.g., AAPL"
              className="focus:black w-full	 max-w-xs rounded-md bg-gray-200 p-2 text-black shadow-sm focus:ring focus:ring-opacity-50"
              onChange={(e) => setTicker(e.target.value)}
            />
            <button
              className="my-2 rounded-lg bg-gray-200 px-4 py-2 text-black"
              onClick={submitTicker}
            >
              Submit
            </button>
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
          <div className="text-left">
            {tickerAnalysis &&
              Object.entries(tickerAnalysis as TickerAnalysis).map(
                ([key, value]) => (
                  <div key={key}>
                    <h2 className="mt-4 text-xl font-bold text-black">
                      {formatHeader(key)}
                    </h2>
                    <p className="text-gray-700">{value.toString()}</p>{" "}
                  </div>
                ),
              )}
          </div>
        </div>
      </main>
    </QueryClientProvider>
  );
}
