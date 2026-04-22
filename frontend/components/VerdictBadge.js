export default function VerdictBadge({ verdict }) {
  const value = String(verdict || "UNKNOWN").toUpperCase();
  const className =
    value === "SUSPICIOUS" ? "verdictBadge verdictSuspicious" : value === "BENIGN" ? "verdictBadge verdictBenign" : "verdictBadge verdictUnknown";

  return <span className={className}>{value}</span>;
}
