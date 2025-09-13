# 🏙️ Smart City Management Platform — Architecture

This document explains the high-level design of the **Smart City MVP**.

---

## 🔄 System Overview
The platform consists of:

1. **Sensor Simulation Service**
   - Generates synthetic real-time data (traffic, AQI, waste, noise).
   - Exposed via **Server-Sent Events (SSE)** at `/api/stream`.

2. **Citizen Incident Module**
   - Citizens submit issues (pothole, garbage, leaks, streetlights).
   - Auto-classifier assigns type.
   - SLA timer & assignment support.
   - Data stored in `app/data/incidents.json`.

3. **Prediction Engine (Stub)**
   - `/api/predict?type=traffic` → returns forecasted congestion hotspots.
   - `/api/predict?type=waste` → predicts bin overflow hours.
   - ML-ready stubs for future deep learning models.

4. **Admin Dashboard**
   - Ward-wise equity metrics (total vs resolved).
   - Transparency & fairness indicators.
   - Prediction tools.

5. **Frontend UI**
   - **Dashboard:** Live map (Leaflet.js) with colored markers.
   - **Incidents:** Reporting form + incident table.
   - **Admin:** Equity metrics & predictions.

---

## 🗂️ Architecture Diagram

```mermaid
flowchart TD
    subgraph Frontend [🌐 Frontend]
        A1[Dashboard (Leaflet Map)]
        A2[Incident Form + Table]
        A3[Admin Dashboard]
    end

    subgraph API [⚡ FastAPI Backend]
        B1[/api/stream (SSE)/]
        B2[/api/incidents/]
        B3[/api/predict/]
    end

    subgraph Services [🛠️ Services]
        C1[Sensor Simulator]
        C2[Incident Classifier]
        C3[Prediction Stubs]
        C4[File Store (JSON)]
    end

    subgraph Data [📂 Data Layer]
        D1[incidents.json]
    end

    A1 --> B1
    A2 --> B2
    A3 --> B2
    A3 --> B3

    B1 --> C1
    B2 --> C2
    B2 --> C4
    B3 --> C3
    C4 --> D1
