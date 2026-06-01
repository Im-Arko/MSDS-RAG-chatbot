import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const QUICK_PROMPTS = [
  "What PPE is required?",
  "First aid for skin exposure",
  "Storage & handling precautions",
  "Fire & explosion hazards",
  "Disposal requirements",
  "Spill response procedure",
];

const SendIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13" />
    <polygon points="22 2 15 22 11 13 2 9 22 2" />
  </svg>
);

const ShieldIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
  </svg>
);

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "MSDS Assistant online. Ask me anything about hazardous materials — safety data, handling, PPE requirements, first aid, storage, or disposal.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const autoResize = () => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 120) + "px";
  };

  const sendMessage = async (text?: string) => {
    const query = (text ?? input).trim();
    if (!query || loading) return;

    const userMessage: Message = { role: "user", content: query };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");
    if (textareaRef.current) textareaRef.current.style.height = "42px";
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/ask", {
        query,
        history: updatedMessages,
      });

      const answer = response.data.answer;

      setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

      let streamedText = "";
      const words = answer.split(" ");

      for (let i = 0; i < words.length; i++) {
        streamedText += words[i] + " ";
        await new Promise((r) => setTimeout(r, 20));
        setMessages((prev) => {
          const copy = [...prev];
          copy[copy.length - 1].content = streamedText;
          return copy;
        });
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Connection error — could not reach the MSDS server. Please try again." },
      ]);
    }

    setLoading(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app-shell">
      <div className="chat-container">

        {/* HEADER */}
        <div className="chat-header">
          <div className="header-icon">
            <ShieldIcon />
          </div>
          <div className="header-text">
            <div className="header-title">MSDS Assistant</div>
            <div className="header-subtitle">Material Safety Data Sheet · AI Query System</div>
          </div>
          <div className="status-badge">
            <span className="status-dot" />
            Online
          </div>
        </div>

        {/* QUICK PROMPTS */}
        <div className="quick-prompts">
          {QUICK_PROMPTS.map((p) => (
            <button key={p} className="quick-chip" onClick={() => sendMessage(p)}>
              {p}
            </button>
          ))}
        </div>

        {/* MESSAGES */}
        <div className="messages-area">
          {messages.map((msg, i) => (
            <div key={i} className={`message-row ${msg.role === "user" ? "user" : ""}`}>
              <div className={`message-avatar ${msg.role === "user" ? "user-av" : "ai"}`}>
                {msg.role === "user" ? "YOU" : "AI"}
              </div>
              <div className="message-content">
                <div className="message-label">
                  {msg.role === "user" ? "Operator" : "MSDS Agent"}
                </div>
                <div className={`bubble ${msg.role === "user" ? "user-bubble" : "ai-bubble"}`}>
                  {msg.content}
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="loading-row">
              <div className="loading-dots">
                <span /><span /><span />
              </div>
              <span className="loading-text">Querying safety database...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* INPUT */}
        <div className="input-area">
          <div className="input-row">
            <textarea
              ref={textareaRef}
              className="input-field"
              placeholder="Ask about hazards, PPE, first aid, storage, disposal..."
              value={input}
              onChange={(e) => { setInput(e.target.value); autoResize(); }}
              onKeyDown={handleKeyDown}
              rows={1}
            />
            <button
              className="send-btn"
              onClick={() => sendMessage()}
              disabled={!input.trim() || loading}
              aria-label="Send message"
            >
              <SendIcon />
            </button>
          </div>
          <div className="input-meta">
            <span className="input-hint">Enter to send · Shift+Enter for newline</span>
            <span className="char-count">{input.length} chars</span>
          </div>
        </div>

      </div>
    </div>
  );
}
