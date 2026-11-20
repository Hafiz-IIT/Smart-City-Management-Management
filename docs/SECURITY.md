# Security and operational boundaries

- Incident creation and listing are public demo endpoints. Incident status and assignment changes require an Authorization Bearer token matching ADMIN_API_TOKEN.
- Set ADMIN_API_TOKEN to a long random secret (at least 32 characters). If it is absent, administrative updates fail closed.
- The file-backed store uses an in-process lock and atomic file replacement. This protects against partial writes and same-process request races; it is not a multi-worker or multi-host database. Use a transactional database before scaling out.
- Ward mapping is a toy coordinate partition, not an authoritative municipal boundary dataset.
- Sensor feeds and prediction endpoints are stochastic demonstrations, not calibrated forecasts or real sensor observations.
