# Smart-City-Management-Platform
A living digital twin of your city, combining real-time sensors, AI prediction, citizen engagement, and gorgeous dashboards. It doesn’t just show data, it tells a story: “This is what’s happening, what’s about to happen, and how to fix it.”

# 🌆 Smart City Management Platform (MVP)

**A digital twin of the city** — real-time sensors, citizen reporting, AI predictions, and equity dashboards.  
Built with **FastAPI + Jinja2 + Leaflet**. No external API keys needed.

---

## ✨ Features
- 📡 **Live Sensor Stream (SSE):** Simulated traffic, AQI, waste, noise sensors.
- 📝 **Citizen Incident Reporting:** Submit potholes, leaks, garbage with SLA timers.
- 🔮 **Prediction Stubs:** Forecast next-30m traffic & waste bin overflow.
- ⚖️ **Equity Metrics:** Ward-level SLA resolution stats.
- 🗺️ **Beautiful Map UI:** Leaflet-based dashboard with colored live markers.
- 🔧 **Admin Tools:** View equity & run prediction demos.

---

## 🛠️ Tech Stack
- **Backend:** FastAPI, Pydantic, Uvicorn
- **Frontend:** Jinja2 templates, Leaflet.js, Vanilla JS
- **Data Store:** JSON file (MVP mode)
- **Languages:** Python 3.10+

---

## 🚀 Quickstart

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/smart-city-mvp.git
cd smart-city-mvp

# Setup venv
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
source .venv/bin/activate

# Install deps
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --port 8000
