# Wealth AI Dashboard

A lightweight, professional portfolio analytics dashboard designed for a private banking context.  
It combines synthetic wealth management data, multilingual UI, dynamic filtering, and interactive charts.

The goal of this project is to demonstrate practical skills aligned with real Wealth Management analytics roles:
- Data generation & transformation (Python, pandas)
- KPI and business reporting (Streamlit)
- Client segmentation & allocation analysis
- Localization (EN, DE, FR, IT, ES)
- Scalable architecture prepared for future AI-based insights

---

##  Features

### ✔ Synthetic Portfolio Dataset  
Generated programmatically using controlled financial distributions:
- AUM (CHF)
- YTD return, volatility, Sharpe ratio  
- Asset allocation (Equity, Bonds, FX, Alternatives)
- Segment (HNW, UHNW, Affluent)
- Advisor ID, country, region

---

###  Interactive Filtering  
Located in the sidebar:
- Client segment  
- Country  
- Language selector (EN, DE, FR, IT, ES)

All charts and KPIs update dynamically based on the selected filters.

---

###  KPI Overview  
- **Total AUM (CHF)**
- **Average YTD return**
- **Average Sharpe ratio**
- **Number of clients (post-filter)**

---

###  Visual Analytics  
- **Client distribution** by segment  
- **Average asset allocation**  
- **Risk / return scatter plot**  
- **Raw data explorer**

---

##  Project Structure

wealth-ai-dashboard/
│
├── app.py   # Streamlit frontend
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│ ├── generate_data.py # Synthetic dataset 
│ ├── viz.py # (future visuals)
│ ├── ai_insights.py # (future AI insights)
│ └── init.py
│
└── data/
└── (empty - generated on the fly)
