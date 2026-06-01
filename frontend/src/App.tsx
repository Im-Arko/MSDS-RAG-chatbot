import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

interface Message {
  role: "user" | "assistant";
  content: string;
  time: string;
}

interface ChatSession {
  id: string;
  title: string;
  date: string;
  messages: Message[];
}

const QUICK_PROMPTS = [
  "Required PPE",
  "First aid — skin exposure",
  "First aid — inhalation",
  "Storage conditions",
  "Fire & explosion hazards",
  "Spill response",
  "Disposal requirements",
  "Reactivity & incompatibilities",
];

const EMPTY_CARDS = [
  {
    icon: "ti-shield-check",
    title: "PPE requirements",
    desc: "Ask about personal protective equipment needed for safe handling",
    prompt: "What PPE is required when handling this material?",
  },
  {
    icon: "ti-first-aid-kit",
    title: "First aid procedures",
    desc: "Get emergency response steps for exposure or ingestion",
    prompt: "What are the first aid procedures for skin and eye exposure?",
  },
  {
    icon: "ti-flame",
    title: "Fire & explosion hazards",
    desc: "Understand flammability, flash points, and firefighting measures",
    prompt: "What are the fire and explosion hazards? What extinguishing agents should be used?",
  },
  {
    icon: "ti-box",
    title: "Storage & handling",
    desc: "Safe storage conditions, temperature ranges, and incompatibilities",
    prompt: "What are the safe storage conditions and handling precautions?",
  },
];

const now = () =>
  new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

const HISTORY: ChatSession[] = [
  { id: "1", title: "Hydrochloric acid — PPE & storage", date: "Today", messages: [] },
  { id: "2", title: "Sodium hydroxide first aid", date: "Today", messages: [] },
  { id: "3", title: "Acetone fire hazards", date: "Yesterday", messages: [] },
  { id: "4", title: "Methanol disposal requirements", date: "Yesterday", messages: [] },
  { id: "5", title: "Chlorine gas exposure limits", date: "Mon 26 May", messages: [] },
];

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeId, setActiveId] = useState("new");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const autoResize = () => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 140) + "px";
  };

  const sendMessage = async (text?: string) => {
    const query = (text ?? input).trim();
    if (!query || loading) return;

    const userMsg: Message = { role: "user", content: query, time: now() };
    const updated = [...messages, userMsg];
    setMessages(updated);
    setInput("");
    if (textareaRef.current) textareaRef.current.style.height = "44px";
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/ask", {
        query,
        history: updated,
      });

      const answer = response.data.answer;
      const aiMsg: Message = { role: "assistant", content: "", time: now() };
      setMessages((prev) => [...prev, aiMsg]);

      let streamed = "";
      for (const word of answer.split(" ")) {
        streamed += word + " ";
        await new Promise((r) => setTimeout(r, 20));
        setMessages((prev) => {
          const copy = [...prev];
          copy[copy.length - 1] = { ...copy[copy.length - 1], content: streamed };
          return copy;
        });
      }
    } catch (error) {
      let errorMessage = "Connection error — could not reach the MSDS server. Please try again.";

      if (axios.isAxiosError(error)) {
        if (error.response) {
          const status = error.response.status;
          const serverDetail =
            typeof error.response.data?.detail === "string"
              ? error.response.data.detail
              : typeof error.response.data?.message === "string"
              ? error.response.data.message
              : undefined;
          errorMessage = `Server error ${status}${serverDetail ? `: ${serverDetail}` : "."}`;
        } else if (error.request) {
          errorMessage = "Network error — MSDS server did not respond. Check the backend and try again.";
        } else if (error.message) {
          errorMessage = `Request error — ${error.message}`;
        }
      } else if (error instanceof Error) {
        errorMessage = `Unexpected error — ${error.message}`;
      }

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: errorMessage, time: new Date().toLocaleTimeString(), },
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

  const newChat = () => {
    setMessages([]);
    setActiveId("new");
  };

  return (
    <div className="app">

      {/* ── TOP BAR ── */}
      <header className="topbar">
        <div className="topbar-logo">
          <div className="logo-stripe" />
          <div>
            <div className="logo-text">MSDS·AI</div>
            <div className="logo-sub">Safety Data Assistant</div>
          </div>
        </div>
        <div className="topbar-center">
          <span className="topbar-session">
            {messages.length > 0
              ? `${messages.filter((m) => m.role === "user").length} queries this session`
              : "New session"}
          </span>
        </div>
        <div className="topbar-right">
          <div className="status-pill">
            <span className="pulse-dot" />
            System online
          </div>
          <button className="topbar-btn" title="Settings" aria-label="Settings">
            <i className="ti ti-settings" aria-hidden="true" />
          </button>
          <button className="topbar-btn" title="Help" aria-label="Help">
            <i className="ti ti-help" aria-hidden="true" />
          </button>
        </div>
      </header>

      {/* ── SIDEBAR ── */}
      <aside className="sidebar">
        <div className="sidebar-section-label">Actions</div>
        <button className="new-chat-btn" onClick={newChat}>
          <i className="ti ti-plus" aria-hidden="true" />
          New query session
        </button>

        <div className="sidebar-divider" />
        <div className="sidebar-section-label">Recent sessions</div>

        <nav className="chat-history">
          {HISTORY.map((h) => (
            <div
              key={h.id}
              className={`history-item ${activeId === h.id ? "active" : ""}`}
              onClick={() => setActiveId(h.id)}
            >
              <i className="ti ti-message history-icon" aria-hidden="true" />
              <div className="history-text">
                <div className="history-title">{h.title}</div>
                <div className="history-date">{h.date}</div>
              </div>
            </div>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-footer-item">
            <i className="ti ti-database" aria-hidden="true" />
            MSDS Database
          </div>
          <div className="sidebar-footer-item">
            <i className="ti ti-upload" aria-hidden="true" />
            Upload SDS file
          </div>
          <div className="sidebar-footer-item">
            <i className="ti ti-settings" aria-hidden="true" />
            Preferences
          </div>
        </div>
      </aside>

      {/* ── MAIN ── */}
      <main className="main">

        {/* Context / quick-prompt bar */}
        <div className="context-bar">
          <span className="context-bar-label">Quick:</span>
          <div className="quick-chips">
            {QUICK_PROMPTS.map((p) => (
              <button key={p} className="chip" onClick={() => sendMessage(p)}>
                {p}
              </button>
            ))}
          </div>
        </div>

        {/* Messages */}
        <div className="messages-wrap">
          {messages.length === 0 ? (
            <div className="empty-state">
              <div className="empty-hero">
                <div className="empty-icon">
                  <img src="assets\favicon.png" alt="" />
                </div>
                <div>
                  <div className="empty-title">MSDS Safety Assistant</div>
                  <div className="empty-sub">AI · Material Safety Data Sheet query system · v2.0</div>
                </div>
              </div>
              <div className="empty-grid">
                {EMPTY_CARDS.map((c) => (
                  <div key={c.title} className="empty-card" onClick={() => sendMessage(c.prompt)}>
                    <div className="empty-card-icon">
                      <i className={`ti ${c.icon}`} aria-hidden="true" />
                    </div>
                    <div className="empty-card-title">{c.title}</div>
                    <div className="empty-card-desc">{c.desc}</div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="messages-inner">
              {messages.map((msg, i) => (
                <div key={i} className={`msg-row ${msg.role === "user" ? "user" : ""}`}>
                  <div className={`msg-avatar ${msg.role === "user" ? "usr" : "ai"}`}>
                    {msg.role === "user" ? "YOU" : "AI"}
                  </div>
                  <div className="msg-body">
                    <div className="msg-meta">
                      <span className="msg-who">
                        {msg.role === "user" ? "Operator" : "MSDS Agent"}
                      </span>
                      <span className="msg-time">{msg.time}</span>
                    </div>
                    <div className={`bubble ${msg.role === "user" ? "user" : "ai"}`}>
                      {msg.content}
                    </div>
                  </div>
                </div>
              ))}

              {loading && (
                <div className="loading-indicator">
                  <div className="ldots">
                    <span /><span /><span />
                  </div>
                  <span className="loading-label">Querying safety database...</span>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input zone */}
        <div className="input-zone">
          <div className="input-inner">
            <div className="input-row">
              <textarea
                ref={textareaRef}
                className="input-field"
                placeholder="Ask about hazards, PPE, first aid, storage, disposal, or regulatory limits..."
                value={input}
                onChange={(e) => { setInput(e.target.value); autoResize(); }}
                onKeyDown={handleKeyDown}
                rows={1}
              />
              <button
                className="send-btn"
                onClick={() => sendMessage()}
                disabled={!input.trim() || loading}
                aria-label="Send"
              >
                <i className="ti ti-send" aria-hidden="true" />
              </button>
            </div>
            <div className="input-footer">
              <span className="input-hint">Enter to send · Shift+Enter for newline</span>
              <span className="input-hint">{input.length} chars</span>
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}
