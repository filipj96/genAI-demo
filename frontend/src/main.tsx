import React from "react";
import ReactDOM from "react-dom/client";
import { FluentProvider, teamsLightTheme, webLightTheme } from "@fluentui/react-components";
import { Chat } from "./components";
import "./index.css";

ReactDOM.createRoot(document.getElementById("app") as HTMLElement).render(
  <FluentProvider theme={webLightTheme}>
    <React.StrictMode>
      <Chat />
    </React.StrictMode>
  </FluentProvider>
);
