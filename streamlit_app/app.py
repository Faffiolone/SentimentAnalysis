import streamlit as st
import requests
import pandas as pd
import time

# Configurazione Pagina
st.set_page_config(page_title="Reputation Monitor", page_icon="📊", layout="wide")

st.title("📊 AI Reputation Monitor")
st.markdown("Monitor brand reputation using **Google News** and **RoBERTa AI**.")

# URL dell'API (Se siamo in Docker usa localhost, altrimenti l'URL dello Space)
# In Codespaces locale usa questo:
API_URL = "http://localhost:8000" 

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    target_company = st.text_input("Company/Brand to monitor:", value="Ferrari")
    num_news = st.slider("Number of news to analyze:", 1, 20, 5)
    analyze_btn = st.button("🚀 Analyze Reputation")
    st.divider()
    st.info("System Status: Online 🟢")

# --- MAIN LOGIC ---
if analyze_btn:
    if target_company:
        with st.spinner(f"🔍 Searching news for '{target_company}' and analyzing sentiment..."):
            try:
                # Chiamata all'API
                payload = {"query": target_company, "limit": num_news}
                response = requests.post(f"{API_URL}/analyze", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data['results']
                    summary = data['summary']
                    
                    # 1. METRICHE (KPI)
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Positive News", summary.get('positive', 0), delta_color="normal")
                    col2.metric("Negative News", summary.get('negative', 0), delta_color="inverse")
                    col3.metric("Neutral News", summary.get('neutral', 0), delta_color="off")
                    
                    # 2. GRAFICI
                    st.subheader("Sentiment Distribution")
                    chart_data = pd.DataFrame({
                        "Sentiment": list(summary.keys()),
                        "Count": list(summary.values())
                    })
                    st.bar_chart(chart_data, x="Sentiment", y="Count", color="Sentiment")

                    # 3. DETTAGLI (Tabella)
                    st.subheader("Latest News Analyzed")
                    for item in results:
                        color = "green" if item['sentiment'] == "positive" else "red" if item['sentiment'] == "negative" else "gray"
                        with st.expander(f":{color}[{item['sentiment'].upper()}] - {item['text'][:80]}..."):
                            st.write(f"**Full Text:** {item['text']}")
                            st.write(f"**Confidence:** {item['confidence']:.2%}")
                            
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}. Is the API running?")
    else:
        st.warning("Please enter a company name.")

# --- MONITORING TAB (Punto 2 dell'esercizio) ---
st.divider()
st.header("📈 Continuous Monitoring Logs")
if st.button("Refresh Logs"):
    try:
        # Leggiamo il CSV generato dall'API
        # Nota: Funziona perché in Codespaces condividiamo il file system. 
        # In produzione servirebbe un endpoint API dedicato /get_logs
        if requests.get(f"{API_URL}/health").status_code == 200:
             # Trucco: leggiamo il file locale (se siamo in locale)
             try:
                 df_logs = pd.read_csv("reputation_logs.csv")
                 st.dataframe(df_logs.sort_values(by="timestamp", ascending=False).head(50))
             except:
                 st.warning("Logs not accessible directly (Are you in Docker?)")
    except:
        st.warning("API not reachable")