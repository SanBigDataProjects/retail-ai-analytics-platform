# 🛍️ Retail AI Analytics Platform

An end-to-end AI-powered data analytics platform that ingests, 
transforms, and analyzes retail sales data — with a natural 
language AI agent that answers business questions instantly.

## 🏗️ Architecture
```
CSV Data → ETL Pipeline (Python/Pandas) → SQLite Database
                                               ↓
                                      Groq AI Agent (LLaMA 3.3)
                                               ↓
                                    Natural Language → SQL → Answer
                                               ↓
                                    Streamlit Dashboard
```

## ✨ Features

- **ETL Pipeline** — Extracts, cleans, transforms 9,993 retail 
  records including revenue, profit, and margin calculations
- **AI Agent** — Ask any business question in plain English, 
  AI writes the SQL and explains the results
- **Live Dashboard** — KPI metrics, revenue trends, category 
  and regional performance charts
- **Data Quality** — Automated null handling, column 
  standardization, and validation

## 📊 Dashboard Preview

- Total Revenue: $11,079,176
- Total Orders: 9,993
- Avg Profit Margin: 5.3%
- Revenue by Month, Category, Region, Segment

## 🤖 AI Agent Examples

Ask it anything:
- *"What are the top 5 products by profit?"*
- *"Which region had the highest revenue?"*
- *"What was the best month for sales?"*
- *"Show average profit margin by segment"*

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Data Processing | Python, Pandas |
| Database | SQLite |
| AI Agent | Groq API, LLaMA 3.3 70B |
| Dashboard | Streamlit |
| ETL Notebook | Jupyter |

## 🚀 How to Run

1. Clone the repo
2. Install dependencies:
```bash
   pip install pandas sqlalchemy streamlit groq plotly python-dotenv
```
3. Create `.env` file:
```
   GROQ_API_KEY=your_groq_api_key_here
```
4. Run ETL pipeline — open `Etl.ipynb` and run all cells
5. Launch dashboard:
```bash
   streamlit run app.py
```

## 📁 Project Structure
```
retail-ai-analytics-platform/
│
├── app.py              # Streamlit dashboard + AI agent
├── Etl.ipynb           # ETL pipeline notebook
├── orders.csv          # Raw retail dataset (9,994 rows)
├── .gitignore          # Excludes database and env files
└── README.md           # Project documentation
```

## 👩‍💻 Author

**Sanyukta Singh**  
Data Engineer | Azure • Databricks • Python • SQL  
📍 Plymouth, Minnesota  
🔗 [LinkedIn](https://linkedin.com/in/sanyukta-singh-38742a223)
