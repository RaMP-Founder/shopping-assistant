import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ChatWindow from "./ChatWindow";
import { MessageCircle } from "lucide-react";

export default function ChatWidget(){
  const [open, setOpen] = useState(false);

  return (
    <>
      <motion.button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 w-16 h-16 rounded-full z-50 shadow-xl flex items-center justify-center"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        whileHover={{ scale: 1.06 }}
        style={{ background: "linear-gradient(90deg,#4b0fb0,#7a2be6)" }}
        aria-label="Open chat"
      >
        <MessageCircle size={26} color="#fff" />
      </motion.button>

      <AnimatePresence>
        {open && (
          <ChatWindow onClose={() => setOpen(false)} />
        )}
      </AnimatePresence>
    </>
  );
}
