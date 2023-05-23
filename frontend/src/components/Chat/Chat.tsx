import React, { useRef, useState } from "react";
import "./Chat.css";
import { QuestionInput } from "../QuestionInput";
import { ChatIntro } from "../ChatIntro/ChatIntro";
import { UserMessage } from "../UserMessage/UserMessage";
import { AssistantMessage } from "../AssistantMessage/AssistantMessage";
import { ChatHeader } from "../ChatHeader";

interface ChatPair {
  question: string;
  answer: string;
  followUpQuestions?: string[]; // Now an array, optional follow up question, probably should be a part of a answer object
}

export const Chat: React.FC = () => {
  const currentQuestion = useRef("");
  const [chatHistory, setChatHistory] = useState<ChatPair[]>([]);

  const handleSubmit = (message: string) => {
    currentQuestion.current = message;

    // Here you would typically call your chatbot API and get the answer.
    // For this example, let's simulate this with a timeout function.
    setTimeout(() => {
      const answer = `Answer to "${message}"`; // replace this with real answer
      const followUpQuestions = getFollowUpQuestions(message);
      setChatHistory((prevChatHistory) => [
        ...prevChatHistory,
        { question: message, answer, followUpQuestions },
      ]);
    }, 1000);
  };

  const handleClearChat = () => {
    setChatHistory([]);
    currentQuestion.current = "";
  };

  const getFollowUpQuestions = (question: string) => {
    // Mock logic for generating follow-up questions based on the user's question
    if (question.toLowerCase().includes("weather")) {
      return [
        "Would you like to know tomorrow's weather as well?",
        "How about the weather for the next week?",
        "Today?",
      ];
    }
    return undefined;
  };

  return (
    <div className="chat-container">
      <h1>Chat with our Virtual Assistant</h1>
      <div className="chat-window">
        <ChatHeader onClearChat={handleClearChat} />
        <div className="chat-content">
          {chatHistory.length === 0 ? (
            <ChatIntro onExampleClick={handleSubmit} />
          ) : (
            chatHistory.map((chatPair, index) => (
              <div key={index}>
                <UserMessage message={chatPair.question} />
                <AssistantMessage
                  message={chatPair.answer}
                  followUpQuestions={chatPair.followUpQuestions}
                  onFollowUpClick={handleSubmit}
                />
              </div>
            ))
          )}
        </div>
        <QuestionInput
          onSubmit={handleSubmit}
          placeholder="Ask your question here"
        />
      </div>
    </div>
  );
};
