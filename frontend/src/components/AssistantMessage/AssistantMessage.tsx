import React from "react";
import "./AssistantMessage.css";

interface AssistantMessageProps {
  message: string;
  followUpQuestions?: string[]; // Optional prop for follow-up questions
  onFollowUpClick?: (followUpQuestions: string) => void; // Callback when a follow-up question is clicked
}

export const AssistantMessage: React.FC<AssistantMessageProps> = ({
  message,
  followUpQuestions,
  onFollowUpClick,
}) => {
  return (
    <div className="assistant-message">
      <div className="assistant-message-content">
        {message}
        {followUpQuestions && followUpQuestions.length > 0 && (
          <div className="follow-up-questions">
            <span>Follow up questions: </span>
            {followUpQuestions.map((followUpQuestion, index) => (
              <p
                key={index}
                className="follow-up-question"
                onClick={() => onFollowUpClick?.(followUpQuestion)}
              >
                {followUpQuestion}
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
