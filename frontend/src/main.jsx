import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

const initialForm = {
  land_area_acres: "",
  crop_type: "",
  repayment_history_score: "",
  annual_income_band: "2–5L",
};

function formatError(errorBody) {
  if (!errorBody?.detail) {
    return "Something went wrong. Please try again.";
  }

  if (Array.isArray(errorBody.detail)) {
    return errorBody.detail
      .map((item) => {
        const field = item.loc?.slice(1).join(".") || "field";
        return `${field}: ${item.msg}`;
      })
      .join(" ");
  }

  return String(errorBody.detail);
}

function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function updateField(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  async function submitScore(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/score`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          land_area_acres: Number(form.land_area_acres),
          crop_type: form.crop_type,
          repayment_history_score: Number(form.repayment_history_score),
          annual_income_band: form.annual_income_band,
        }),
      });

      const body = await response.json();
      if (!response.ok) {
        throw new Error(formatError(body));
      }

      setResult(body);
    } catch (caughtError) {
      setError(caughtError.message || "Unable to reach the scoring service.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <section className="panel">
        <div className="heading">
          <p>SaakhSetu by Arbix AI</p>
          <h1>Farmer Credit Score</h1>
        </div>

        <form className="score-form" onSubmit={submitScore}>
          <label>
            Land area in acres
            <input
              name="land_area_acres"
              type="number"
              min="0.01"
              step="0.01"
              value={form.land_area_acres}
              onChange={updateField}
              required
            />
          </label>

          <label>
            Crop type
            <input
              name="crop_type"
              type="text"
              value={form.crop_type}
              onChange={updateField}
              required
            />
          </label>

          <label>
            Repayment history score
            <input
              name="repayment_history_score"
              type="number"
              min="0"
              max="100"
              step="1"
              value={form.repayment_history_score}
              onChange={updateField}
              required
            />
          </label>

          <label>
            Annual income band
            <select
              name="annual_income_band"
              value={form.annual_income_band}
              onChange={updateField}
            >
              <option value="<2L">&lt;2L</option>
              <option value="2–5L">2–5L</option>
              <option value="5–10L">5–10L</option>
              <option value=">10L">&gt;10L</option>
            </select>
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Scoring..." : "Calculate score"}
          </button>
        </form>

        {error ? <div className="message error">{error}</div> : null}

        {result ? (
          <section className="result">
            <div>
              <span>Score</span>
              <strong>{result.score}</strong>
            </div>
            <p>
              <b>Request ID:</b> {result.request_id}
            </p>
            <p>
              <b>Timestamp:</b> {new Date(result.timestamp).toLocaleString()}
            </p>
            <div className="reasons">
              {result.reason_codes.map((reason) => (
                <span key={reason}>{reason}</span>
              ))}
            </div>
          </section>
        ) : null}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
