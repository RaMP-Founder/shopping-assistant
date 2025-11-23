import React from "react";
import ChatWidget from "./components/ChatWidget";

export default function App(){
  return (
    <div className="min-h-screen flex items-start justify-center pt-20">
      <div className="w-full max-w-5xl px-6">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-extrabold text-white">Premium Skincare Assistant</h1>
          <p className="mt-2 text-gray-300">Luxury recommendations, curated for your skin</p>
        </div>
        <div className="bg-gradient-to-b from-[#0b0710] to-[#07050a] rounded-2xl p-8">
          <p className="text-gray-400">Click the floating chat button at bottom right to open the shopping assistant.</p>
        </div>
      </div>

      <ChatWidget />
    </div>
  );
}
