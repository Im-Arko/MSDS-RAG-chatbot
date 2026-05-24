import {
  Box,
  Paper,
  Typography,
  TextField,
  IconButton,
  CircularProgress,
} from "@mui/material";

import SendIcon from "@mui/icons-material/Send";

import { useState } from "react";

import axios from "axios";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function App() {

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hello 👋 Ask me anything about your insurance policies.",
    },
  ]);

  const [input, setInput] = useState("");

  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {

    if (!input.trim()) return;

    const userMessage: Message = {
      role: "user",
      content: input,
    };

    const updatedMessages = [
      ...messages,
      userMessage,
    ];

    setMessages(updatedMessages);

    const currentInput = input;

    setInput("");

    setLoading(true);

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/ask",
        {
          query: currentInput,
          history: updatedMessages,
        }
      );

      const answer = response.data.answer;

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "",
        },
      ]);

      let streamedText = "";

      const words = answer.split(" ");

      for (let i = 0; i < words.length; i++) {

        streamedText += words[i] + " ";

        await new Promise((resolve) =>
          setTimeout(resolve, 20)
        );

        setMessages((prev) => {

          const copy = [...prev];

          copy[copy.length - 1].content =
            streamedText;

          return copy;
        });
      }

    } catch (error) {

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Something went wrong.",
        },
      ]);

      console.log(error);
    }

    setLoading(false);
  };

  const handleKeyDown = (
    e: React.KeyboardEvent
  ) => {

    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <Box
      sx={{
        height: "100vh",
        background: "#111827",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        p: 2,
      }}
    >
      <Paper
        sx={{
          width: "100%",
          maxWidth: "900px",
          height: "90vh",
          display: "flex",
          flexDirection: "column",
          background: "#1f2937",
          borderRadius: 4,
          overflow: "hidden",
        }}
      >

        {/* HEADER */}

        <Box
          sx={{
            p: 2,
            borderBottom: "1px solid #374151",
          }}
        >
          <Typography
            variant="h5"
            sx={{
              color: "white",
              fontWeight: "bold",
            }}
          >
            Insurance Policy Chatbot
          </Typography>

          <Typography
            sx={{
              color: "#9ca3af",
            }}
          >
            AI Powered Insurance Assistant
          </Typography>
        </Box>

        {/* CHAT AREA */}

        <Box
          sx={{
            flex: 1,
            overflowY: "auto",
            p: 2,
            display: "flex",
            flexDirection: "column",
            gap: 2,
          }}
        >
          {messages.map((message, index) => (

            <Box
              key={index}
              sx={{
                display: "flex",
                justifyContent:
                  message.role === "user"
                    ? "flex-end"
                    : "flex-start",
              }}
            >
              <Box
                sx={{
                  maxWidth: "75%",
                  px: 2,
                  py: 1.5,
                  borderRadius: 3,
                  background:
                    message.role === "user"
                      ? "#2563eb"
                      : "#374151",
                  color: "white",
                }}
              >
                {message.content}
              </Box>
            </Box>
          ))}

          {loading && (
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                gap: 2,
              }}
            >
              <CircularProgress size={20} />

              <Typography
                sx={{
                  color: "#9ca3af",
                }}
              >
                Generating response...
              </Typography>
            </Box>
          )}
        </Box>

        {/* INPUT */}

        <Box
          sx={{
            p: 2,
            borderTop: "1px solid #374151",
            display: "flex",
            gap: 2,
          }}
        >
          <TextField
            fullWidth
            placeholder="Ask about insurance..."
            value={input}
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={handleKeyDown}
            sx={{
              "& .MuiOutlinedInput-root": {
                color: "white",
                background: "#111827",
              },
            }}
          />

          <IconButton
            onClick={sendMessage}
            sx={{
              background: "#2563eb",
              color: "white",
              width: 55,
              height: 55,
              "&:hover": {
                background: "#1d4ed8",
              },
            }}
          >
            <SendIcon />
          </IconButton>
        </Box>
      </Paper>
    </Box>
  );
}