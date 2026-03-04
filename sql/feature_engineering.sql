-- Customer-level features for ML
DROP VIEW IF EXISTS customer_features;

CREATE VIEW customer_features AS
WITH transaction_stats AS (
    SELECT
        customer_id,
        COUNT(*) AS transaction_count,
        AVG(amount) AS avg_transaction_amount,
        SUM(amount) AS total_spend
    FROM transactions
    GROUP BY customer_id
),
session_stats AS (
    SELECT
        customer_id,
        AVG(duration) AS avg_session_duration,
        AVG(pages_viewed) AS avg_pages_viewed
    FROM sessions
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.age,
    c.gender,
    c.location,
    t.transaction_count,
    t.avg_transaction_amount,
    t.total_spend,
    s.avg_session_duration,
    s.avg_pages_viewed
FROM customers c
LEFT JOIN transaction_stats t ON c.customer_id = t.customer_id
LEFT JOIN session_stats s ON c.customer_id = s.customer_id;

-- Add churn label 
-- DROP VIEW IF EXISTS customer_features_labeled;

-- CREATE VIEW customer_features_labeled AS
-- SELECT
--     *,
--     CASE
--         WHEN transaction_count < 4 THEN 1
--         ELSE 0
--     END AS churn_label
-- FROM customer_features;

-- Recreate labeled feature view 
-- DROP VIEW IF EXISTS customer_features_labeled;

-- CREATE VIEW customer_features_labeled AS
-- SELECT
--     *,
--     CASE
--         WHEN total_spend < 300
--              AND avg_session_duration < 5
--         THEN 1
--         ELSE 0
--     END AS churn_label
-- FROM customer_features;


-- Leakage-free, data-driven churn label
DROP VIEW IF EXISTS customer_features_labeled;

CREATE VIEW customer_features_labeled AS
WITH ranked AS (
    SELECT
        *,
        NTILE(4) OVER (ORDER BY total_spend) AS spend_quartile,
        NTILE(4) OVER (ORDER BY avg_session_duration) AS session_quartile
    FROM customer_features
)
SELECT
    *,
    CASE
        WHEN spend_quartile = 1
         AND session_quartile = 1
        THEN 1
        ELSE 0
    END AS churn_label
FROM ranked;