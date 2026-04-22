"use client";

import { useEffect, useMemo, useState } from "react";
import EventDetails from "@/components/EventDetails";
import EventsTable from "@/components/EventsTable";
import HealthStatus from "@/components/HealthStatus";
import ManualScanPanel from "@/components/ManualScanPanel";
import StatCard from "@/components/StatCard";
import { fetchEvents, fetchHealth, getApiBaseUrl, scanRequest } from "@/lib/api";

function getEventKey(event) {
  return [
    event.timestamp || "",
    event.method || "",
    event.path || "",
    event.query || "",
    event.score ?? "",
    event.threshold ?? "",
  ].join("|");
}

export default function HomePage() {
  const [healthStatus, setHealthStatus] = useState("");
  const [healthLoading, setHealthLoading] = useState(true);
  const [healthError, setHealthError] = useState("");

  const [events, setEvents] = useState([]);
  const [eventsLoading, setEventsLoading] = useState(true);
  const [eventsError, setEventsError] = useState("");
  const [selectedEventKey, setSelectedEventKey] = useState(null);

  useEffect(() => {
    let mounted = true;
    let isFirstLoad = true;

    const loadHealth = async () => {
      try {
        const health = await fetchHealth();
        if (mounted) {
          setHealthStatus(String(health?.status || ""));
          setHealthError("");
        }
      } catch (error) {
        if (mounted) {
          setHealthStatus("");
          setHealthError(error instanceof Error ? error.message : "Health check failed.");
        }
      } finally {
        if (mounted && isFirstLoad) {
          setHealthLoading(false);
          isFirstLoad = false;
        }
      }
    };

    loadHealth();
    const intervalId = setInterval(loadHealth, 10000);

    return () => {
      mounted = false;
      clearInterval(intervalId);
    };
  }, []);

  useEffect(() => {
    let mounted = true;
    let isFirstLoad = true;

    const loadEvents = async () => {
      try {
        const latestEvents = await fetchEvents();
        if (mounted) {
          const normalized = Array.isArray(latestEvents) ? latestEvents : [];
          setEvents(normalized);
          setEventsError("");
        }
      } catch (error) {
        if (mounted) {
          setEventsError(error instanceof Error ? error.message : "Unable to fetch events.");
        }
      } finally {
        if (mounted && isFirstLoad) {
          setEventsLoading(false);
          isFirstLoad = false;
        }
      }
    };

    loadEvents();
    const intervalId = setInterval(loadEvents, 2500);

    return () => {
      mounted = false;
      clearInterval(intervalId);
    };
  }, []);

  useEffect(() => {
    if (events.length === 0) {
      setSelectedEventKey(null);
      return;
    }

    if (!selectedEventKey) {
      setSelectedEventKey(getEventKey(events[0]));
      return;
    }

    const selectedStillExists = events.some((event) => getEventKey(event) === selectedEventKey);
    if (!selectedStillExists) {
      setSelectedEventKey(getEventKey(events[0]));
    }
  }, [events, selectedEventKey]);

  const selectedEvent = useMemo(
    () => events.find((event) => getEventKey(event) === selectedEventKey) || null,
    [events, selectedEventKey]
  );

  const suspiciousCount = useMemo(
    () => events.filter((event) => String(event.verdict || "").toUpperCase() === "SUSPICIOUS").length,
    [events]
  );
  const benignCount = useMemo(
    () => events.filter((event) => String(event.verdict || "").toUpperCase() === "BENIGN").length,
    [events]
  );

  return (
    <main className="page">
      <div className="backdropGlow" />
      <section className="hero">
        <div>
          <p className="eyebrow">Security Monitoring</p>
          <h1>Transformer-based WAF Dashboard</h1>
          <p className="heroSub">
            Frontend dashboard for live request scoring and manual payload testing.
          </p>
          <p className="apiInfo">
            API base URL: <code>{getApiBaseUrl()}</code>
          </p>
        </div>
        <HealthStatus status={healthStatus} loading={healthLoading} error={healthError} />
      </section>

      <section className="statsGrid">
        <StatCard label="Total Displayed Events" value={events.length} />
        <StatCard label="Suspicious Count" value={suspiciousCount} tone="suspicious" />
        <StatCard label="Benign Count" value={benignCount} tone="benign" />
      </section>

      <section className="mainGrid">
        <div className="leftColumn">
          <EventsTable
            events={events}
            selectedKey={selectedEventKey}
            onSelect={setSelectedEventKey}
            loading={eventsLoading}
            error={eventsError}
            getEventKey={getEventKey}
          />
          <EventDetails event={selectedEvent} />
        </div>
        <ManualScanPanel onScan={scanRequest} />
      </section>
    </main>
  );
}
