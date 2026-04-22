import VerdictBadge from "@/components/VerdictBadge";

function formatScore(value) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) {
    return "-";
  }
  return numeric.toFixed(4);
}

function DetailRow({ label, value }) {
  return (
    <div className="detailRow">
      <dt>{label}</dt>
      <dd>{value || "-"}</dd>
    </div>
  );
}

export default function EventDetails({ event }) {
  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>Event Details</h2>
          <p>Click a row in the events table to inspect full payload data.</p>
        </div>
      </div>

      {!event ? <p className="emptyStateBlock">Select an event to view details.</p> : null}

      {event ? (
        <dl className="detailList">
          <DetailRow label="Query" value={event.query} />
          <DetailRow label="Serialized Request" value={event.serialized} />
          <DetailRow label="Route" value={event.route} />
          <DetailRow label="Mode" value={event.mode} />
          <DetailRow label="Score" value={formatScore(event.score)} />
          <DetailRow label="Threshold" value={formatScore(event.threshold)} />
          <div className="detailRow">
            <dt>Verdict</dt>
            <dd>
              <VerdictBadge verdict={event.verdict} />
            </dd>
          </div>
        </dl>
      ) : null}
    </section>
  );
}
