const DEFAULT_API_BASE_URL = "http://192.168.1.6:5000";

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_BASE_URL || DEFAULT_API_BASE_URL).replace(
  /\/+$/,
  ""
);
console.log("API_BASE_URL =", API_BASE_URL);

async function buildErrorMessage(response) {
  const fallback = `Request failed with status ${response.status}`;
  try {
    const contentType = response.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      const data = await response.json();
      if (data && typeof data === "object" && data.error) {
        return String(data.error);
      }
      return fallback;
    }
    const text = await response.text();
    return text || fallback;
  } catch {
    return fallback;
  }
}

async function request(path, { method = "GET", body, signal } = {}) {
  const headers = {};
  if (body !== undefined) {
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
    signal,
  });

  if (!response.ok) {
    throw new Error(await buildErrorMessage(response));
  }

  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return response.json();
  }

  return null;
}

export function getApiBaseUrl() {
  return API_BASE_URL;
}

export function fetchHealth(signal) {
  return request("/health", { signal });
}

export function fetchEvents(signal) {
  return request("/events", { signal });
}

export function scanRequest(payload, signal) {
  return request("/scan", {
    method: "POST",
    body: {
      method: payload.method || "GET",
      path: payload.path || "/",
      query: payload.query || "",
      body: payload.body || "",
      headers: {},
    },
    signal,
  });
}
