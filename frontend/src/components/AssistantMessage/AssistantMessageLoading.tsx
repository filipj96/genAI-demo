import React from "react";
import "./AssistantMessage.css";
import { Spinner } from "@fluentui/react-components";

export const AssistantMessageLoading: React.FC = () => {
  return (
    <div className="assistant-message-loading">
        <Spinner size="extra-small" label="Thinking..." />
    </div>
  );
};
