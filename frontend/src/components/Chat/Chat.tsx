import React, { useRef, useState } from "react";
import "./Chat.css";
import { QuestionInput } from "../QuestionInput";
import { ChatIntro } from "../ChatIntro/ChatIntro";
import { UserMessage } from "../UserMessage/UserMessage";
import { AssistantMessage } from "../AssistantMessage/AssistantMessage";
import { ChatHeader } from "../ChatHeader";
import { ChatRequest, AskResponse, ChatTurn, chatApi } from "../../api";

export const Chat: React.FC = () => {
  const currentQuestion = useRef("");
  const [chatHistory, setChatHistory] = useState<ChatTurn[]>([]);

  const handleSubmit = async (message: string) => {
    currentQuestion.current = message;

    // Here you would typically call your chatbot API and get the answer.
    // For this example, let's simulate this with a timeout function.

    const request: ChatRequest = {
      history: chatHistory,
    };
    const result: AskResponse = await chatApi(request);
    setChatHistory((prevChatHistory) => [
      ...prevChatHistory,
      { question: message, answer: result.answer },
    ]);
    console.log(result);

    setTimeout(() => {
      const answer = `Answer to "${message}"`; // replace this with real answer
      setChatHistory((prevChatHistory) => [
        ...prevChatHistory,
        { question: message, answer },
      ]);
    }, 1000);
  };

  const onExampleClick = (example: string) => {
    handleSubmit(example);
  };

  const handleClearChat = () => {
    setChatHistory([]);
    currentQuestion.current = "";
  };

  return (
    <div className="chat-container">
      <h1>Chat with our Virtual Assistant</h1>
      <div className="chat-window">
        <ChatHeader onClearChat={handleClearChat} />
        <div className="chat-content">
          {chatHistory.length === 0 ? (
            <ChatIntro onExampleClick={onExampleClick} />
          ) : (
            chatHistory.map((ChatTurn, index) => (
              <div key={index}>
                <UserMessage message={ChatTurn.question} />
                <AssistantMessage
                  message={ChatTurn.answer}
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
