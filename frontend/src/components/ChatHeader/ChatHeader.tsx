import React from "react";
import { Button } from "@fluentui/react-components";
import { BroomRegular } from "@fluentui/react-icons";
import "./ChatHeader.css";

interface ChatHeaderProps {
  onClearChat: () => void;
}

export const ChatHeader: React.FC<ChatHeaderProps> = ({ onClearChat }) => {
  return (
    <div className="chat-header">
      <p>Virtual Assistant</p>
      <Button onClick={onClearChat} icon={<BroomRegular />} />
    </div>
  );
};
