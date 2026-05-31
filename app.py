import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# 1. KONFIGURACJA STRONY
st.set_page_config(page_title="InwestorVision - Dashboard", layout="wide")

st.title("📈 Dashboard Analizy Rynkowej")
st.markdown("Dane pobierane na żywo z **Yahoo Finance**.")

# 2. PANEL BOCZNY
st.sidebar.header("⚙️ Ustawienia")
popularne = ["AAPL", "MSFT", "TSLA", "NVDA", "SPY", "QQQ", "BTC-USD"]
wybrane = st.sidebar.multiselect("Wybierz symbole:", popularne, default=["AAPL", "SPY"])

data_start = st.sidebar.date_input("Data początkowa", datetime.now() - timedelta(days=365))

# 3. FUNKCJA POBIERANIA DANYCH
@st.cache_data(ttl=3600)
def pobierz_dane(symbole, start):
    if not symbole:
        return pd.DataFrame()
    dane = yf.download(symbole, start=start)['Close']
    if len(symbole) == 1:
        dane = dane.to_frame()
        dane.columns = symbole
    return dane

# 4. LOGIKA GŁÓWNA
if wybrane:
    df = pobierz_dane(wybrane, data_start)
    
    if not df.empty:
        # WSKAŹNIKI KPI
        st.subheader("🚀 Aktualne ceny")
        kolumny = st.columns(len(wybrane))
        
        for i, ticker in enumerate(wybrane):
            cena_akt = df[ticker].iloc[-1]
            cena_poprz = df[ticker].iloc[0]
            zmiana = ((cena_akt - cena_poprz) / cena_poprz) * 100
            # Poprawiona linia - wszystko w jednym wywołaniu:
            kolumny[i].metric(label=ticker, value=f"${cena_akt:.2f}", delta=f"{zmiana:.2f}%")

        st.divider()

        # WYKRESY
        c1, c2 = st.columns(2)
        with c1:
            st.write("### Cena w USD")
            st.plotly_chart(px.line(df), use_container_width=True)
        with c2:
            st.write("### Wydajność (Start = 100)")
            df_norm = (df / df.iloc[0]) * 100
            st.plotly_chart(px.line(df_norm), use_container_width=True)

        with st.expander("🔍 Dane tabelaryczne"):
            st.dataframe(df.tail(10), use_container_width=True)
else:
    st.info("👈 Wybierz symbole na pasku bocznym.")
