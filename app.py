import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ---- SETUP ----
st.set_page_config(
    page_title="Retail AI Analytics",
    page_icon="🛍️",
    layout="wide"
)

# Initialize Groq client securely
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Database connection
engine = create_engine('sqlite:///C:/Users/Sam/Desktop/retail-ai-project/retail.db')

# ---- AI AGENT FUNCTION ----
def ask_data(question):
    # Step 1: AI converts question to SQL
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""You are a SQL expert working with a retail orders database.
            
Table name: orders
Columns: order_id, order_date, ship_mode, segment, country, city, 
         state, postal_code, region, category, sub_category,
         cost_price, list_price, quantity, discount_percent,
         order_month, order_year, order_quarter,
         discount, sale_price, profit, revenue, profit_margin

Convert this question to a valid SQLite query:
Question: {question}

Return ONLY the SQL query, nothing else. No explanation, no markdown."""
        }],
        max_tokens=500
    )

    sql = response.choices[0].message.content.strip()
    # Remove markdown code blocks if AI adds them
    sql = sql.replace("```sql", "").replace("```", "").strip()

    # Step 2: Run SQL against database
    try:
        results = pd.read_sql(sql, engine)

        # Step 3: AI explains results in plain English
        explanation = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""Question: {question}
SQL Results: {results.to_string()}
Explain the answer in 2-3 clear sentences for a business user."""
            }],
            max_tokens=300
        )

        return sql, results, explanation.choices[0].message.content

    except Exception as e:
        return sql, None, f"Error running query: {str(e)}"


# ---- LOAD DATA ----
df = pd.read_sql('SELECT * FROM orders', engine)

# ---- HEADER ----
st.title("🛍️ Retail AI Analytics Platform")
st.markdown("*Powered by AI — Ask questions about your retail data in plain English*")
st.divider()

# ---- KPI METRICS ----
st.subheader("📊 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
with col2:
    st.metric("Total Profit", f"${df['profit'].sum():,.0f}")
with col3:
    st.metric("Total Orders", f"{len(df):,}")
with col4:
    st.metric("Avg Profit Margin", f"{df['profit_margin'].mean():.1f}%")

st.divider()

# ---- CHARTS ROW 1 ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Revenue by Month")
    monthly = df.groupby('order_month')['revenue'].sum().reset_index()
    monthly = monthly.sort_values('order_month')
    st.line_chart(monthly.set_index('order_month'))

with col2:
    st.subheader("🏆 Revenue by Category")
    category = df.groupby('category')['revenue'].sum().reset_index()
    category = category.sort_values('revenue', ascending=False)
    st.bar_chart(category.set_index('category'))

# ---- CHARTS ROW 2 ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 Revenue by Region")
    region = df.groupby('region')['revenue'].sum().reset_index()
    region = region.sort_values('revenue', ascending=False)
    st.bar_chart(region.set_index('region'))

with col2:
    st.subheader("👥 Profit by Segment")
    segment = df.groupby('segment')['profit'].sum().reset_index()
    segment = segment.sort_values('profit', ascending=False)
    st.bar_chart(segment.set_index('segment'))

st.divider()

# ---- CHARTS ROW 3 ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Top 10 Sub-Categories by Revenue")
    subcat = df.groupby('sub_category')['revenue'].sum().reset_index()
    subcat = subcat.sort_values('revenue', ascending=False).head(10)
    st.bar_chart(subcat.set_index('sub_category'))

with col2:
    st.subheader("🚚 Orders by Ship Mode")
    shipmode = df.groupby('ship_mode')['order_id'].count().reset_index()
    shipmode.columns = ['ship_mode', 'order_count']
    st.bar_chart(shipmode.set_index('ship_mode'))

st.divider()

# ---- AI AGENT ----
st.subheader("🤖 Ask AI About Your Data")
st.markdown("Type any business question below and AI will write the SQL, run it, and explain the answer.")

question = st.text_input(
    "Your question:",
    placeholder="e.g. What are the top 5 products by profit?"
)

if st.button("Ask AI ✨", type="primary"):
    if question:
        with st.spinner("AI is thinking..."):
            sql, results, answer = ask_data(question)

        st.success("✅ Answer Ready!")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🤖 AI Answer:**")
            st.info(answer)
        with col2:
            st.markdown("**📝 SQL Generated:**")
            st.code(sql, language="sql")

        if results is not None and not results.empty:
            st.markdown("**📊 Data:**")
            st.dataframe(results, use_container_width=True)
    else:
        st.warning("Please type a question first!")

st.divider()
st.caption("Built with Python • SQLite • Groq AI • Streamlit | Sanyukta Singh")