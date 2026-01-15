import { useState, useRef } from "react";
import { Plus, ArrowUp } from "lucide-react";

interface ChatInputProps {
  onSend: (message: string) => void;
  onFileUpload?: (file: File) => void;
  disabled?: boolean;
}

const ChatInput = ({ onSend, onFileUpload, disabled }: ChatInputProps) => {
  const [message, setMessage] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = () => {
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleFileClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && onFileUpload) {
      // Validate file type
      const suffix = file.name.toLowerCase().split(".").pop();
      if (suffix && ["pdf", "docx", "txt"].includes(suffix)) {
        onFileUpload(file);
      } else {
        alert("Please upload a PDF, DOCX, or TXT file.");
      }
      // Reset input
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  return (
    <div className="chat-input-container">
      <div className="chat-input-card">
        <textarea
          className="chat-textarea"
          placeholder="Ask anything"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          disabled={disabled}
        />
        <div className="chat-input-actions">
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx,.txt"
            style={{ display: "none" }}
            onChange={handleFileChange}
          />
          <button
            className="attach-btn"
            type="button"
            onClick={handleFileClick}
            aria-label="Attach file"
            disabled={disabled}
          >
            <Plus size={20} />
          </button>
          <button
            className="send-btn"
            type="button"
            onClick={handleSubmit}
            disabled={!message.trim() || disabled}
            aria-label="Send message"
          >
            <ArrowUp size={18} />
          </button>
        </div>
      </div>
      <p className="chat-disclaimer">
        AI can make mistakes. Please double-check responses.
      </p>
    </div>
  );
};

export default ChatInput;
