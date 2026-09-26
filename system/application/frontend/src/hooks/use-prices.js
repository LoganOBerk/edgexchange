import { useState, useEffect } from "react";
import { subscribeQuote } from "@/lib/api";

export function usePrices(tickers) {
    const [prices, setPrices] = useState({});
    const [errors, setErrors] = useState({});

    useEffect(() => {
        const unique = [...new Set(tickers)];
        if (!unique.length) return;

        const unsubscribers = unique.map((t) =>
            subscribeQuote(
                t,
                (data) => {
                    // Backend may send the quote fields directly, or wrapped
                    // as { quote: {...} }; handle either until confirmed.
                    const quote = data?.quote ?? data;
                    setPrices((prev) => ({ ...prev, [t]: quote }));
                    setErrors((prev) => {
                        if (!(t in prev)) return prev;
                        const next = { ...prev };
                        delete next[t];
                        return next;
                    });
                },
                (message) => {
                    setErrors((prev) => ({ ...prev, [t]: message }));
                }
            )
        );

        return () => unsubscribers.forEach((unsub) => unsub());
    }, [tickers.join(",")]);

    const loading = tickers.some((t) => !prices[t] && !errors[t]);

    return { prices, errors, loading };
}