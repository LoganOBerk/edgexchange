"use client";

import { createContext, useContext, useState, useEffect } from "react";
import { useSession } from "@/context/SessionContext";
import { subscribePortfolios } from "@/lib/api";

const CACHE_KEY = "edgexchange_live_data_v2";

const fmt = (n) => Number(n).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });

const readCache = () => {
    try { return JSON.parse(localStorage.getItem(CACHE_KEY)) ?? {}; }
    catch { return {}; }
};

const writeCache = (data) => {
    try { localStorage.setItem(CACHE_KEY, JSON.stringify(data)); }
    catch { }
};

const PortfolioContext = createContext(null);

export const usePortfolio = () => {
    const ctx = useContext(PortfolioContext);
    if (!ctx) throw new Error("usePortfolio must be used within PortfolioProvider");
    return ctx;
};

export const PortfolioProvider = ({ children }) => {
    const { sessionId, user, logout } = useSession();
    const [liveData, setLiveData] = useState({});

    useEffect(() => {
        setLiveData(readCache());
    }, []);

    useEffect(() => {
        const portfolioNames = Object.keys(user?.portfolios ?? {});
        if (!sessionId || !portfolioNames.length) return;

        const unsubscribe = subscribePortfolios(
            sessionId,
            (parsed) => {
                for (const entry of parsed.portfolios ?? []) {
                    if (!entry.portfolio) continue;
                    setLiveData((prev) => {
                        const next = {
                            ...prev,
                            [entry.portfolio]: {
                                total: `$${fmt(entry.total)}`,
                                holdings: entry.stocks,
                            },
                        };
                        writeCache(next);
                        return next;
                    });
                }
            },
            (err) => {
                // An expired/invalid session is expected once the backend
                // restarts or the session times out - treat it as a normal
                // "please log in again" state, not a console error.
                if (err === "Invalid session") {
                    logout();
                    return;
                }
                console.error("Portfolio stream error", err);
            }
        );

        return unsubscribe;
    }, [sessionId, Object.keys(user?.portfolios ?? {}).join(",")]);

    return (
        <PortfolioContext.Provider value={{ liveData }}>
            {children}
        </PortfolioContext.Provider>
    );
};