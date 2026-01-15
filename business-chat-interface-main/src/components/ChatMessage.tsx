interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

const ChatMessage = ({ role, content }: ChatMessageProps) => {
  return (
    <div className={`chat-message chat-message-${role}`}>
      <div className="message-content">
        {content}
      </div>
    </div>
  );
};

export default ChatMessage;
