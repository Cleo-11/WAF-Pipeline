import VerdictBadge from "@/components/VerdictBadge";

function formatScore(value) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) {
    return "-";
  }
  return numeric.toFixed(4);
}

export default function EventsTable({ events, selectedKey, onSelect, loading, error, getEventKey }) {
  return (
    <section className="panel">
      <div className="panelHeader">
        <div>
          <h2>Live Events Dashboard</h2>
          <p>Auto-refresh every 2.5 seconds</p>
        </div>
      </div>

      {error ? <p className="panelError">{error}</p> : null}

      <div className="tableWrap">
        <table className="eventsTable">
          <thead>
            <tr>
              <th>timestamp</th>
              <th>method</th>
              <th>path</th>
              <th>mode</th>
              <th>score</th>
              <th>threshold</th>
              <th>verdict</th>
            </tr>
          </thead>
          <tbody>
            {loading && events.length === 0 ? (
              <tr>
                <td colSpan={7} className="emptyState">
                  Loading events...
                </td>
              </tr>
            ) : null}

            {!loading && events.length === 0 ? (
              <tr>
                <td colSpan={7} className="emptyState">
                  No events available.
                </td>
              </tr>
            ) : null}

            {events.map((event, index) => {
              const key = getEventKey(event, index);
              const isSelected = key === selectedKey;
              return (
                <tr key={key} className={isSelected ? "selectedRow" : ""} onClick={() => onSelect(key)}>
                  <td>{event.timestamp || "-"}</td>
                  <td>{event.method || "-"}</td>
                  <td className="pathCell">{event.path || "-"}</td>
                  <td>{event.mode || "-"}</td>
                  <td>{formatScore(event.score)}</td>
                  <td>{formatScore(event.threshold)}</td>
                  <td>
                    <VerdictBadge verdict={event.verdict} />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}
