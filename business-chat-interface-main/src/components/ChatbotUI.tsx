import { useState } from "react";
import ChatHeader from "@/components/ChatHeader";
import ChatInput from "@/components/ChatInput";
import ChatMessage from "@/components/ChatMessage";
import ChatWelcome from "@/components/ChatWelcome";
import "./ChatbotUI.css";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

// Get API URL from environment variable, fallback to localhost for development
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const ChatbotUI = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [docName, setDocName] = useState<string | null>(null);

  const handleFileUpload = async (file: File) => {
    setIsUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);
      if (sessionId) {
        formData.append("session_id", sessionId);
      }

      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to upload document");
      }

      const data = await response.json();
      setSessionId(data.session_id);
      setDocName(data.doc_name);
      setMessages([]); // Clear messages when new document is uploaded
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to upload document");
      console.error("Upload error:", err);
    } finally {
      setIsUploading(false);
    }
  };

  const handleSend = async (content: string) => {
    if (!sessionId) {
      setError("Please upload a document first.");
      return;
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: content,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to get response");
      }

      const data = await response.json();
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message");
      // Remove user message on error
      setMessages((prev) => prev.filter((msg) => msg.id !== userMessage.id));
      console.error("Chat error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const hasMessages = messages.length > 0;

  return (
    <div className={`chatbot-container ${hasMessages ? 'has-messages' : 'welcome-state'}`}>
      <ChatHeader />
      {error && (
        <div style={{
          padding: "12px",
          margin: "12px",
          backgroundColor: "#fee",
          color: "#c33",
          borderRadius: "8px",
          fontSize: "14px"
        }}>
          {error}
        </div>
      )}
      {isUploading && (
        <div style={{
          padding: "12px",
          margin: "12px",
          backgroundColor: "#eef",
          color: "#336",
          borderRadius: "8px",
          fontSize: "14px"
        }}>
          Processing document...
        </div>
      )}
      {hasMessages ? (
        <>
          <main className="chat-main">
            <div className="chat-messages">
              {messages.map((msg) => (
                <ChatMessage key={msg.id} role={msg.role} content={msg.content} />
              ))}
              {isLoading && (
                <ChatMessage
                  role="assistant"
                  content="Thinking..."
                />
              )}
            </div>
          </main>
          <ChatInput
            onSend={handleSend}
            onFileUpload={handleFileUpload}
            disabled={isLoading || isUploading}
          />
        </>
      ) : (
        <div className="welcome-centered">
          <ChatWelcome />
          {docName && (
            <div style={{
              padding: "12px",
              margin: "12px 0",
              backgroundColor: "#efe",
              color: "#363",
              borderRadius: "8px",
              fontSize: "14px"
            }}>
              Document loaded: {docName}
            </div>
          )}
          <ChatInput
            onSend={handleSend}
            onFileUpload={handleFileUpload}
            disabled={isLoading || isUploading}
          />
        </div>
      )}
    </div>
  );
};

export default ChatbotUI;
