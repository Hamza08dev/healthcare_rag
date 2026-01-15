interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

// Simple markdown to HTML converter for basic formatting
const markdownToHtml = (text: string): string => {
  // Split into lines for list processing
  const lines = text.split('\n');
  const processedLines: string[] = [];
  let inList = false;
  
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];
    const listMatch = line.match(/^[\*\-\+] (.+)$/);
    
    if (listMatch) {
      if (!inList) {
        processedLines.push('<ul>');
        inList = true;
      }
      // Process markdown inside list item
      let listContent = listMatch[1];
      // Bold: **text**
      listContent = listContent.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
      // Code: `text`
      listContent = listContent.replace(/`([^`]+)`/g, '<code>$1</code>');
      processedLines.push(`<li>${listContent}</li>`);
    } else {
      if (inList) {
        processedLines.push('</ul>');
        inList = false;
      }
      if (line.trim()) {
        // Process markdown in regular lines
        // Bold: **text**
        line = line.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        // Code: `text`
        line = line.replace(/`([^`]+)`/g, '<code>$1</code>');
        // Italic: *text* (but not if it's part of **)
        line = line.replace(/(?<!\*)\*([^*\n]+?)\*(?!\*)/g, '<em>$1</em>');
        processedLines.push(line);
      } else {
        processedLines.push('<br />');
      }
    }
  }
  
  if (inList) {
    processedLines.push('</ul>');
  }
  
  return processedLines.join('\n');
};

const ChatMessage = ({ role, content }: ChatMessageProps) => {
  const htmlContent = markdownToHtml(content);
  
  return (
    <div className={`chat-message chat-message-${role}`}>
      <div 
        className="message-content"
        dangerouslySetInnerHTML={{ __html: htmlContent }}
      />
    </div>
  );
};

export default ChatMessage;
