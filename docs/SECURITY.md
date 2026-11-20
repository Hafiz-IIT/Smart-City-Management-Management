# Security and operational boundaries

- Incident status and assignment changes require the X-Admin-Key header matching ADMIN_API_KEY. If the key is absent or too short, the endpoint fails closed.
- Incident creation and listing remain public demonstration endpoints; add abuse controls before production use.
- The file-backed incident store uses an in-process lock and atomic replacement. It is not safe for multiple worker processes or multiple hosts; migrate to a transactional database before scaling.
- Incident status changes follow a finite transition graph. Resolved and expired are terminal.
- Unknown incident descriptions are not silently classified as garbage; the caller must select a category.
- Ward mapping is a toy coordinate partition, not an authoritative municipal boundary dataset.
- Sensor feeds and prediction endpoints are stochastic demonstrations, not calibrated forecasts or real sensor observations.
