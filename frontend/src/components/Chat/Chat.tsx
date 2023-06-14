import React, { useRef, useState } from "react";
import "./Chat.css";
import { QuestionInput } from "../QuestionInput";
import { ChatIntro } from "../ChatIntro/ChatIntro";
import { UserMessage } from "../UserMessage/UserMessage";
import { AssistantMessage, AssistantMessageLoading } from "../AssistantMessage";
import { ChatHeader } from "../ChatHeader";
import { ChatRequest, AskResponse, ChatTurn, chatApi } from "../../api";
import { Spinner } from "@fluentui/react-components";

export const Chat: React.FC = () => {
  const currentQuestion = useRef("");
  const [chatHistory, setChatHistory] = useState<ChatTurn[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSubmit = async (message: string) => {
    currentQuestion.current = message;
    setIsLoading(true);

    try {
      const history: ChatTurn[] = chatHistory.map((h) => ({
        question: h.question,
        answer: h.answer,
      }));

      const request: ChatRequest = {
        history: [...chatHistory, { question: message, answer: "" }],
      };

      const result: AskResponse = await chatApi(request);
      setChatHistory((prevChatHistory) => [
        ...prevChatHistory,
        { question: message, answer: result.answer },
      ]);

      // This is used for testing the frontend      
      /* setTimeout(() => {
        console.log(currentQuestion.current);
        console.log(isLoading);
        const answer = `Answer to "${message}"`; // replace this with real answer
        setChatHistory((prevChatHistory) => [
          ...prevChatHistory,
          { question: message, answer },
        ]);
        setIsLoading(false);
      }, 2000); */
    } 
    finally {
      setIsLoading(false);
    }
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
            <div>
            {chatHistory.map((ChatTurn, index) => (
              <div key={index}>
                <UserMessage message={ChatTurn.question} />
                <AssistantMessage
                  message={ChatTurn.answer}
                  onFollowUpClick={handleSubmit}
                />
              </div>
            ))}
            {isLoading && (
              <>
                <UserMessage message={currentQuestion.current} />
                <AssistantMessageLoading />
              </>
            )}
            </div>
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
