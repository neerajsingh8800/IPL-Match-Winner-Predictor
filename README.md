# 🏏 IPL Match Winner-Predictor
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://ipl-match-winner-predictor-g76nuf3epp3j6gjqqvwxbh.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![ML](https://img.shields.io/badge/Model-XGBoost-green.svg)](https://xgboost.readthedocs.io/)

An end-to-end Machine Learning solution that predicts the win probability of the chasing team in an IPL match. This project transitions from raw data processing to a production-ready web application.

## 🚀 Live Demo
**[Click here to view the Live Web App](https://ipl-match-winner-predictor-g76nuf3epp3j6gjqqvwxbh.streamlit.app/)**

<img width="1919" height="905" alt="Screenshot 2026-04-14 103031" src="https://github.com/user-attachments/assets/6bd47f3c-75c2-4348-a1ec-6f57e338b9d9" />

## 🧠 Technical Overview
This project leverages an **XGBoost Classifier** to handle the high-dimensional and non-linear complexities of T20 cricket. Key features include:
* **Dynamic Feature Engineering:** Calculates real-time metrics such as "Required Run Rate," "Wickets Remaining," and "Target Pressure."
* **Contextual Intelligence:** Incorporates **Head-to-Head (H2H)** historical dominance and **Venue-specific** scoring trends.
* **Data Standardization:** Handles franchise name changes (e.g., Delhi Daredevils → Delhi Capitals) across 15+ years of historical data.

## 📁 Repository Structure
```bash
├── models/             # Serialized XGBoost model, Scaler, and Feature Columns
├── IPL_Model.ipynb     # Full Pipeline: Data Cleaning, EDA, & Model Training
├── IPL_Prediction.py   # Streamlit Production Script
└── requirements.txt    # Deployment Dependencies
