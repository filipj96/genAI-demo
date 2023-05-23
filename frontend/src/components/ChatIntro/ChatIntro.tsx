import React from "react";

interface ChatIntroProps {
  onExampleClick: (example: string) => void;
}

export const ChatIntro: React.FC<ChatIntroProps> = ({ onExampleClick }) => {
  const examples = [
    "What's the weather like today?",
    "How tall is Mount Everest?",
    "Who won the world series last year?",
  ];
  return (
    <div>
      <p>Welcome! Feel free to ask our Virtual Assistant anything.</p>
      <p>Here are some examples of questions you can ask:</p>
      <ul>
        {examples.map((example, index) => (
          <li
            key={index}
            onClick={() => onExampleClick(example)}
            style={{ cursor: "pointer" }}
          >
            {`"${example}"`}
          </li>
        ))}
      </ul>
    </div>
  );
};
