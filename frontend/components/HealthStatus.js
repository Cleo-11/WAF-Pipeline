export default function HealthStatus({ status, loading, error }) {
  const isHealthy = !loading && !error && status === "ok";
  const text = loading ? "Checking backend..." : error ? `Health check failed: ${error}` : `Backend status: ${status || "unknown"}`;

  return (
    <div className="healthWrap" role="status" aria-live="polite">
      <span className={`healthDot ${isHealthy ? "healthUp" : "healthDown"}`} />
      <span className="healthText">{text}</span>
    </div>
  );
}
