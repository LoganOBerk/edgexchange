const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function req(endpoint, options = {}) {
    const res = await fetch(`${BASE}${endpoint}`, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });
    if (!res.ok) {
        const text = await res.text();
        let detail; try { detail = JSON.parse(text)?.detail; } catch { }
        const err = new Error(detail || `Server error (${res.status})`);
        err.status = res.status;
        throw err;
    }
    return res.json();
}

const post = (url, body) => req(url, { method: "POST", body: JSON.stringify(body) });

export const registerUser = (username, password) => post("/register", { username, password });
export const loginUser = (username, password) => post("/login", { username, password });
export const logoutUser = (session_id) => post("/logout", { session_id });
export const getUser = (session_id) => req(`/user?session_id=${session_id}`);
export const fundAccount = (session_id, funds_requested) => post("/fund", { session_id, funds_requested });
export const createPortfolio = (session_id, name) => post("/portfolio/create", { session_id, name });
export const removePortfolio = (session_id, name) => post("/portfolio/remove", { session_id, name });
export const executeBuy = (session_id, portfolio_name, ticker, quantity) => post("/buy", { session_id, portfolio_name, ticker, quantity });
export const executeSell = (session_id, portfolio_name, ticker, quantity) => post("/sell", { session_id, portfolio_name, ticker, quantity });

// Shared ndjson stream reader. Resolves each parsed line to onData, or
// reports failure (either a non-2xx before the stream opens, or a
// mid-stream fetch failure) to onError. Returns an unsubscribe function.
function streamNdjson(url, onData, onError) {
    const controller = new AbortController();
    fetch(url, { signal: controller.signal }).then(async (res) => {
        if (!res.ok) {
            const text = await res.text();
            let detail; try { detail = JSON.parse(text)?.detail; } catch { }
            onError?.(detail || `Server error (${res.status})`);
            return;
        }
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            for (const line of decoder.decode(value).trim().split("\n"))
                if (line) try { onData(JSON.parse(line)); } catch { }
        }
    }).catch((err) => { if (err.name !== "AbortError") onError?.(err.message || String(err)); });
    return () => controller.abort();
}

// Streams all of the session's portfolios; backend sends every portfolio
// on this connection, there is no per-portfolio filtering.
export function subscribePortfolios(session_id, onData, onError) {
    return streamNdjson(`${BASE}/portfolios?session_id=${session_id}`, onData, onError);
}

// Streams live quote updates for a single ticker.
export function subscribeQuote(ticker, onData, onError) {
    return streamNdjson(`${BASE}/quote?ticker=${ticker}`, onData, onError);
}