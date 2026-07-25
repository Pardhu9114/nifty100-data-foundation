DROP TABLE IF EXISTS peer_percentiles;

CREATE TABLE peer_percentiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT NOT NULL,
    peer_group_name TEXT NOT NULL,
    metric TEXT NOT NULL,
    value REAL,
    percentile_rank REAL,
    year TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(id)
);

CREATE INDEX idx_peer_percentiles_company
ON peer_percentiles(company_id);

CREATE INDEX idx_peer_percentiles_group
ON peer_percentiles(peer_group_name);

CREATE INDEX idx_peer_percentiles_metric
ON peer_percentiles(metric);