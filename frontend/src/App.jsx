// frontend/src/App.jsx
import React, { useState, useEffect, useRef } from "react";
import { createRoot } from "react-dom/client";
import { motion } from "framer-motion";

function App() {
  const isEdit =
    document.getElementById("react-payment-form")?.dataset.isEdit === "true";

  // αρχικές τιμές από Django hidden inputs
  const initialCost = parseFloat(document.getElementById("react_cost")?.value || 0);
  const initialPaid = parseFloat(document.getElementById("react_paid")?.value || 0);
  const initialRate = parseFloat(
    document.getElementById("react_collectorFeeRate")?.value || 0.03
  );
  const initialPaymentDate =
    document.getElementById("react_paymentDate")?.value || "";
  const initialReceiverId = parseInt(
    document.getElementById("react_receiver")?.value || 1
  );

  const [cost, setCost] = useState(initialCost);
  const [paid, setPaid] = useState(initialPaid);
  const [collectorFeeRate, setCollectorFeeRate] = useState(initialRate);
  const [collectorFee, setCollectorFee] = useState(initialCost * initialRate);
  const [balance, setBalance] = useState(initialPaid - initialCost);
  const [paymentDate, setPaymentDate] = useState(initialPaymentDate);
  const [receivers, setReceivers] = useState([]);
  const [receiverId, setReceiverId] = useState(initialReceiverId);
  const [notes, setNotes] = useState("");

  const saveBtnRef = useRef(null);
  const payBtnRef = useRef(null);

  // --- φορτώνει ποσοστό και εισπράκτορες ---
  useEffect(() => {
    fetch("/api/collector-fee-rate/")
      .then((r) => r.json())
      .then((data) => {
        if (data.collectorFeeRate) setCollectorFeeRate(parseFloat(data.collectorFeeRate));
      })
      .catch(() => {});

    fetch("/api/receivers/")
      .then((r) => r.json())
      .then((data) => {
        setReceivers(data);
        // ορίζουμε προεπιλεγμένο τον id=1
        if (data.some((r) => r.id === 1)) setReceiverId(1);
      })
      .catch(() => {});
  }, []);

  // --- υπολογισμοί ---
  useEffect(() => {
    const fee = cost * collectorFeeRate;
    setCollectorFee(fee);
    setBalance(paid - cost - fee);
  }, [cost, paid, collectorFeeRate]);

  // --- focus ---
  useEffect(() => {
    if (isEdit) payBtnRef.current?.focus();
    else saveBtnRef.current?.focus();
  }, [isEdit]);

  // --- tab order με Enter ---
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      const focusable = Array.from(
        document.querySelectorAll("button, input, textarea, select")
      ).filter((el) => !el.disabled);
      const index = focusable.indexOf(document.activeElement);
      const next = focusable[index + 1] || focusable[0];
      next.focus();
    }
  };

  // --- βοηθοί ---
  const todayStr = () => new Date().toISOString().split("T")[0];

  const handlePayment = () => {
    setPaid(cost); // πλήρωσε όλο το ποσό
    setPaymentDate(todayStr());
    setReceiverId(1);
    alert("Πληρωμή ολοκληρώθηκε!");
  };

  const handleSave = () => {
    alert("Αποθηκεύτηκε επιτυχώς!");
    // μετά από 1 δευτ επιστροφή
    setTimeout(() => window.history.back(), 1000);
  };

  // --- render ---
  return (
    <motion.div
      className="p-3 rounded-2xl shadow-sm bg-white"
      onKeyDown={handleKeyDown}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <form>
        <div className="container-fluid">
          {/* Αρ Απόδειξης & Αξία */}
          <div className="row mb-3">
            <div className="col-md-6">
              <label className="form-label">Αρ. Απόδειξης</label>
              <input type="text" className="form-control" readOnly value="" />
            </div>
            <div className="col-md-6">
              <label className="form-label">Αξία (€)</label>
              <input
                type="number"
                step="0.01"
                className="form-control"
                value={cost.toFixed(2)}
                onChange={(e) =>
                  setCost(parseFloat(e.target.value) || 0)
                }
              />
            </div>
          </div>

          {/* Πλήρωσε & Ισοζύγιο */}
          <div className="row mb-3">
            <div className="col-md-6">
              <label className="form-label">Πλήρωσε (€)</label>
              <input
                type="number"
                step="0.01"
                className="form-control"
                value={paid.toFixed(2)}
                onChange={(e) =>
                  setPaid(parseFloat(e.target.value) || 0)
                }
              />
            </div>
            <div className="col-md-6">
              <label className="form-label">Ισοζύγιο (€)</label>
              <input
                type="text"
                className="form-control"
                value={balance.toFixed(2)}
                readOnly
              />
            </div>
          </div>

          {/* Ημ/νία Πληρωμής & Εισπράκτορας */}
          <div className="row mb-3">
            <div className="col-md-4">
              <label className="form-label">Ημ/νία Πληρωμής</label>
              <input
                type="date"
                className="form-control"
                value={paymentDate ? paymentDate.split("T")[0] : ""}
                onChange={(e) => setPaymentDate(e.target.value)}
              />
            </div>
            <div className="col-md-8">
              <label className="form-label">Εισπράκτορας</label>
              <select
                className="form-select"
                value={receiverId}
                onChange={(e) => setReceiverId(parseInt(e.target.value))}
              >
                {receivers.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Ποσοστό & Αμοιβή Εισπράκτορα */}
          <div className="row mb-3">
            <div className="col-md-6">
              <label className="form-label">Ποσοστό Εισπράκτορα (%)</label>
              <input
                type="number"
                step="0.01"
                className="form-control"
                value={(collectorFeeRate * 100).toFixed(2)}
                onChange={(e) =>
                  setCollectorFeeRate(parseFloat(e.target.value) / 100 || 0)
                }
              />
            </div>
            <div className="col-md-6">
              <label className="form-label">Αμοιβή Εισπράκτορα (€)</label>
              <input
                type="text"
                className="form-control"
                value={collectorFee.toFixed(2)}
                readOnly
              />
            </div>
          </div>

          {/* Σημειώσεις */}
          <div className="row mb-3">
            <div className="col-12">
              <label className="form-label">Σημειώσεις</label>
              <textarea
                className="form-control"
                rows="2"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                style={{ resize: "none", overflowY: "auto" }}
              ></textarea>
            </div>
          </div>

          {/* Ποτισμός */}
          <div className="row mb-3">
            <div className="col-md-6">
              <label className="form-label">Ποτισμός</label>
              <input type="text" className="form-control" value="--" readOnly />
            </div>
          </div>

          {/* Κουμπιά */}
          <div className="d-flex justify-content-end gap-2">
            <button
              type="button"
              className="btn btn-success"
              onClick={handleSave}
              ref={saveBtnRef}
            >
              💾 Αποθήκευση
            </button>

            <button
              type="button"
              className="btn btn-primary"
              onClick={handlePayment}
              ref={payBtnRef}
            >
              💰 Πληρωμή
            </button>

            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => window.history.back()}
            >
              ↩ Επιστροφή
            </button>
          </div>
        </div>
      </form>
    </motion.div>
  );
}

const root = createRoot(document.getElementById("react-payment-form"));
root.render(<App />);
export default App;
