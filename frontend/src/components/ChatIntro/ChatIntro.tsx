import React from "react";
import "./ChatIntro.css";

interface ChatIntroProps {
  onExampleClick: (example: string) => void;
}

export const ChatIntro: React.FC<ChatIntroProps> = ({ onExampleClick }) => {
  const examples = [
    "Recommend a french wine made from the Pinot Noir grape",
    "I want a wine that goes well with steak",
  ];

  return (
    <div>
      <p>Welcome! Feel free to ask our Virtual Assistant anything.</p>
      <p>Here are some examples of questions you can ask:</p>
      <ul>
        {examples.map((example, index) => (
          <li
            className="intro-question-list-item"
            key={index}
            onClick={() => onExampleClick(example)}
          >
            <div className="intro-question-container">
              <p className="intro-question">{example}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};
