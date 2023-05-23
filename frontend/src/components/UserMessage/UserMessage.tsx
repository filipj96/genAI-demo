import React from "react";
import "./UserMessage.css";

interface UserMessageProps {
  message: string;
}

export const UserMessage: React.FC<UserMessageProps> = ({ message }) => {
  return (
    <div className="user-message">
      <p className="user-message-content">{message}</p>
    </div>
  );
};
