import logo from "@/assets/business-optima-logo.png";

const ChatHeader = () => {
  return (
    <header className="chat-header">
      <div className="header-logo">
        <img src={logo} alt="Business Optima" className="logo-image" />
      </div>
      <div className="header-spacer" />
    </header>
  );
};

export default ChatHeader;
