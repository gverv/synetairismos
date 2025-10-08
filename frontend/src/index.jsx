import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("react-payment-form");
  if (container) {
    const isEdit = container.dataset.isEdit === "true";
    const root = createRoot(container);
    root.render(<App isEdit={isEdit} />);
  }
});
