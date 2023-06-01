import React from "react";
import "./ChatIntro.css";

interface ChatIntroProps {
  onExampleClick: (example: string) => void;
}

export const ChatIntro: React.FC<ChatIntroProps> = ({ onExampleClick }) => {
  const examples = [
    "Ett rött vin som passar till grillat lamm",
    "Ett franskt balkongvin, rött",
    "Ett gott vin från Spanien",
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
