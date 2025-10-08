import React from "react";
import { createRoot } from "react-dom/client";

const PaymentButtons = ({ isEdit }) => {
  return (
    <div className="d-flex flex-column flex-md-row gap-2 mt-2">
      <button type="button" className="btn btn-primary" id="fillPayment">
        Πληρωμή
      </button>
      {isEdit ? (
        <button type="submit" className="btn btn-success">
          Ενημέρωση
        </button>
      ) : (
        <button type="submit" className="btn btn-success">
          Αποθήκευση
        </button>
      )}
    </div>
  );
};

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("react-payment-form");
  if (container) {
    const isEdit = !!container.dataset.isEdit;
    createRoot(container).render(<PaymentButtons isEdit={isEdit} />);
  }
});
