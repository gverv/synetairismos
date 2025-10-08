
// frontend/src/index.js
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




function PaymentButtons() {
  const handlePayment = () => alert("Πληρωμή συμπληρώθηκε!");
  return (
    <div className="d-flex flex-column flex-md-row gap-2 mt-2">
      <button type="button" className="btn btn-primary" onClick={handlePayment}>
        Πληρωμή
      </button>
      <button type="submit" className="btn btn-success">
        Αποθήκευση
      </button>
    </div>
  );
}

// const container = document.getElementById("react-payment-form");
// if (container) {
//   const root = createRoot(container);
//   root.render(<PaymentButtons />);
// }

