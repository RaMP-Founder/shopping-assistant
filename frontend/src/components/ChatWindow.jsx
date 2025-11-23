import React, { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import ProductCard from "./ProductCard";

export default function ChatWindow({ onClose }){
  const [messages, setMessages] = useState([
    { sender: "assistant", text: "Welcome. Tell me your skin concern or the product you want." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatRef = useRef(null);

  useEffect(() => {
    chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async () => {
    const text = input.trim();
    if(!text) return;
    setMessages(prev => [...prev, { sender: "user", text }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: "web_user_premium", user_message: text })
      });
      const data = await res.json();

      setMessages(prev => [
        ...prev,
        { sender: "assistant", text: data.assistant_message || "Sorry, I could not fetch results." },
        ...(data.products || []).map(p => ({ sender: "product", product: p }))
      ]);
    } catch (e) {
      console.error(e);
      setMessages(prev => [...prev, { sender: "assistant", text: "Server error, try again later." }]);
    }

    setLoading(false);
  };

  return (
    <motion.div
      className="fixed bottom-24 right-6 w-[420px] h-[640px] rounded-xl z-50"
      initial={{ opacity: 0, y: 30, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 30 }}
    >
      <div className="flex flex-col h-full rounded-xl overflow-hidden" style={{ boxShadow: "0 20px 60px rgba(4,2,12,0.6)" }}>
        <div className="chat-header px-4 py-3 flex items-center justify-between">
          <div>
            <div className="text-white font-semibold">Luxury Skinshop Assistant</div>
            <div className="text-xs text-white/80">Curated picks just for you</div>
          </div>
          <div>
            <button onClick={onClose} className="text-white/90 px-3 py-1 rounded hover:bg-white/10">Close</button>
          </div>
        </div>

        <div ref={chatRef} className="flex-1 overflow-y-auto p-4 chat-scroll" style={{ background: "linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.005))" }}>
          <div className="space-y-3">
            {messages.map((m, i) => (
              m.sender === "product" ? (
                <ProductCard key={i} product={m.product} premium />
              ) : (
                <div key={i} className={m.sender === "user" ? "ml-auto max-w-[78%]" : "max-w-[78%]"}>
                  <div className={m.sender === "user" ? "bubble-user" : "bubble-assistant"}>
                    {m.text}
                  </div>
                </div>
              )
            ))}
          </div>
        </div>

        <div className="p-4 bg-[#07040b] border-t border-white/5">
          <div className="flex gap-3">
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => { if(e.key === "Enter") sendMessage(); }}
              placeholder="Try: anti aging serum for 30 year old"
              className="flex-1 rounded-full px-4 py-2 bg-white/3 placeholder:text-white/60 outline-none"
            />
            <button onClick={sendMessage} className="btn-gold px-4 py-2 rounded-full">
              {loading ? "..." : "Search"}
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
