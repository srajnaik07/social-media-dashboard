# PulseMetrics | Social Media Analytics & Intelligence Engine

A full-stack exploratory data analysis (EDA) application built with **Streamlit** and **Plotly**. Designed for real-time social performance attribution, cross-channel engagement tracking, and integrated conversational data queries.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pulsemetrics-social-media-analyser.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red.svg)
![Visualization](https://img.shields.io/badge/Visualization-Plotly-black.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Live Deployment:** [pulsemetrics-social-media-analyser.streamlit.app](https://pulsemetrics-social-media-analyser.streamlit.app/)

---

## Executive Overview

PulseMetrics transforms raw social media telemetry and engagement records into actionable business intelligence. The platform combines interactive exploratory data analysis, dynamic multi-parameter filtering, and a deterministic Natural Language Query (NLQ) engine that performs direct computational queries across active dataset slices without third-party API dependencies.

---

## Core Capabilities

- **Executive KPI Monitoring:** Computational tracking of aggregate impressions, engagement coefficients, interaction totals, and channel-level benchmarks.
- **Dynamic Plotly Visualizations:**
  - **Performance Trajectory:** Time-series impression tracking across major social platforms.
  - **Format Attribution:** Quantitative assessment of engagement across media formats (Reels, Carousels, Static Images, Stories).
  - **Volume vs. Engagement Correlation:** Scatter mapping to isolate outlier assets and campaign reach.
- **Integrated AI Analytics Assistant:**
  - Contextual querying engine evaluated directly against live DataFrame subsets.
  - Handles natural language queries regarding top-performing content, platform efficiency benchmarks, and distribution strategy.
- **Data Pipeline & Export:**
  - Native loading of repository datasets (`social_media_usage.csv`).
  - Live CSV upload engine allowing custom enterprise data ingestion.
  - Granular multi-parameter filtering and instant CSV export.
- **Design System:** Custom obsidian dark theme with crimson accents, structured typography, and Font Awesome vector icons.

---

## Technical Architecture

- **Application Logic:** Python 3.9+
- **Frontend Framework:** Streamlit
- **Data Engineering:** Pandas, NumPy
- **Visual Analytics:** Plotly Express, Plotly Graph Objects
- **Styling & Assets:** Custom CSS, Font Awesome 6 CDN, Streamlit Configuration Engine (`config.toml`)
- **Hosting & CI/CD:** Streamlit Community Cloud (connected via GitHub Continuous Deployment)

---

## Project Structure

```text
social-media-dashboard/
│
├── assets/
│   ├── 01_usage_distribution.png
│   ├── 02_app_popularity.png
│   ├── 03_avg_minutes_per_app.png
│   ├── 04_correlation_heatmap.png
│   ├── 05_boxplot_per_app.png
│   ├── 06_usage_category_pie.png
│   └── 07_engagement_per_app.png
│
├── .streamlit/
│   └── config.toml
│
├── app.py
├── requirements.txt
├── social_media_usage.csv
└── README.md

```
## Author

**Spurthi Raj**
- GitHub: [@srajnaik07](https://github.com/srajnaik07)
- LinkedIn: [Spurthi Raj](https://www.linkedin.com/in/s-rajnaik07)
