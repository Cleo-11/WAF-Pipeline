export default function StatCard({ label, value, tone = "neutral" }) {
  return (
    <article className={`statCard statCard${tone[0].toUpperCase()}${tone.slice(1)}`}>
      <p className="statLabel">{label}</p>
      <p className="statValue">{value}</p>
    </article>
  );
}
