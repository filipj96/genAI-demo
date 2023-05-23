import React, { useState } from "react";
import { Button, Textarea } from "@fluentui/react-components";
import { SendFilled } from "@fluentui/react-icons";
import "./QuestionInput.css";

interface QuestionInputProps {
  onSubmit: (message: string) => void;
  placeholder?: string;
}

export const QuestionInput: React.FC<QuestionInputProps> = ({
  onSubmit,
  placeholder,
}) => {
  const [message, setMessage] = useState("");

  const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(event.target.value);
  };

  const onEnterPress = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      onSubmit(message);
      setMessage("");
    }
  };

  return (
    <div className="question-input">
      <Textarea
        placeholder={placeholder}
        value={message}
        onChange={handleChange}
        onKeyDown={onEnterPress}
        className="textarea"
      />
      <div className="questionInputButtonsContainer">
        <Button
          onClick={() => {
            onSubmit(message);
            setMessage("");
          }}
          className="send-button"
          icon={<SendFilled primaryFill="rgba(115, 118, 225, 1)"/>}
          appearance="transparent"
        />
      </div>
    </div>
  );
};
