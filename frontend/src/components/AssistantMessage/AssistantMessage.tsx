import React from "react";
import "./AssistantMessage.css";
import { assistantAnswerParser, ParsedAnswer } from "./AssistantAnswerParser"

interface AssistantMessageProps {
  message: string;
  onFollowUpClick?: (followUpQuestions: string) => void;
}

export const AssistantMessage: React.FC<AssistantMessageProps> = ({
  message,
  onFollowUpClick,
}) => {
  const parsedAnswer: ParsedAnswer = assistantAnswerParser(message)

  return (
    <div className="assistant-message">
      <div className="assistant-message-content">
        {parsedAnswer.parsedAnswer}
        {parsedAnswer.followupQuestions && parsedAnswer.followupQuestions.length > 0 && (
          <div className="follow-up-questions">
            <span>Follow up questions: </span>
            {parsedAnswer.followupQuestions.map((followUpQuestion, index) => (
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
