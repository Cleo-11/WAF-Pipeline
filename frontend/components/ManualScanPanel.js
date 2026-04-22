"use client";

import { useState } from "react";
import VerdictBadge from "@/components/VerdictBadge";

function formatScore(value) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) {
    return "-";
  }
  return numeric.toFixed(4);
}

function ResultRow({ label, value }) {
  return (
    <div className="resultRow">
      <dt>{label}</dt>
      <dd>{value || "-"}</dd>
    </div>
  );
}

export default function ManualScanPanel({ onScan }) {
  const [form, setForm] = useState({
    method: "GET",
    path: "/rest/products/search",
    query: "",
    body: "",
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const updateField = (name, value) => {
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await onScan(form);
      setResult(response);
    } catch (scanError) {
      setResult(null);
      setError(scanError instanceof Error ? scanError.message : "Scan failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="panel scanPanel">
      <div className="panelHeader">
        <div>
          <h2>Manual Scan Panel</h2>
          <p>Submit request payloads to the backend model and inspect the response.</p>
        </div>
      </div>

      <form className="scanForm" onSubmit={handleSubmit}>
        <label>
          Method
          <select value={form.method} onChange={(event) => updateField("method", event.target.value)}>
            <option value="GET">GET</option>
            <option value="POST">POST</option>
            <option value="PUT">PUT</option>
            <option value="PATCH">PATCH</option>
            <option value="DELETE">DELETE</option>
          </select>
        </label>

        <label>
          Path
          <input
            type="text"
            value={form.path}
            onChange={(event) => updateField("path", event.target.value)}
            placeholder="/rest/products/search"
            required
          />
        </label>

        <label>
          Query
          <input
            type="text"
            value={form.query}
            onChange={(event) => updateField("query", event.target.value)}
            placeholder="q=<script>alert(1)</script>"
          />
        </label>

        <label>
          Body
          <textarea
            value={form.body}
            onChange={(event) => updateField("body", event.target.value)}
            placeholder="Optional request body"
            rows={5}
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? "Scanning..." : "Run Scan"}
        </button>
      </form>

      {error ? <p className="panelError">{error}</p> : null}

      {result ? (
        <div className="scanResult">
          <div className="scanResultVerdict">
            <span>Verdict</span>
            <VerdictBadge verdict={result.verdict} />
          </div>
          <dl>
            <ResultRow label="Serialized Request" value={result.serialized} />
            <ResultRow label="Route" value={result.route} />
            <ResultRow label="Mode" value={result.mode} />
            <ResultRow label="Score" value={formatScore(result.score)} />
            <ResultRow label="Threshold" value={formatScore(result.threshold)} />
          </dl>
        </div>
      ) : null}
    </section>
  );
}
