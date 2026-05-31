import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# 1. KONFIGURACJA STRONY
st.set_page_config(page_title="InwestorVision - Analiza ETF", layout="wide")

st.title("📈 Globalny Dashboard Finansowy")
st.markdown("Analiza najpopularniejszych **Indeksów (ETF)** oraz **Akcji** w czasie rzeczywistym.")

# 2. PANEL BOCZNY - Rozbudowana lista
st.sidebar.header("⚙️ Konfiguracja")

# Słownik z opisami dla profesjonalnego wyglądu
opisy_tickerow = {
    "SPY": "S&P 500 (USA - 500 firm)",
    "QQQ": "NASDAQ 100 (Technologia)",
    "DIA": "Dow Jones (Przemysł)",
    "IWM": "Russell 2000 (Małe firmy)",
    "EEM": "Emerging Markets (Rynki wschodzące)",
    "GLD": "Złoto (Gold)",
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "TSLA": "Tesla",
    "NVDA": "NVIDIA",
    "BTC-USD": "Bitcoin"
}

# Wybór symboli
wybrane_opisy = st.sidebar.multiselect(
    "Wybierz aktywa do analizy:",
    options=list(opisy_tickerow.values()),
    default=["S&P 500 (USA - 500 firm)", "NASDAQ 100 (Technologia)"]
)

# Mapowanie opisów z powrotem na tickery dla Yahoo Finance
wybrane_tickery = [t for t, opis in opisy_tickerow.items() if opis in wybrane_opisy]

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
if wybrane_tickery:
    df = pobierz_dane(wybrane_tickery, data_start)
    
    if not df.empty:
        # WSKAŹNIKI KPI
        st.subheader("🚀 Podsumowanie rynkowe")
        kolumny = st.columns(len(wybrane_tickery))
        
        for i, ticker in enumerate(wybrane_tickery):
            cena_akt = df[ticker].iloc[-1]
            cena_poprz = df[ticker].iloc[0]
            zmiana = ((cena_akt - cena_poprz) / cena_poprz) * 100
            kolumny[i].metric(label=ticker, value=f"${cena_akt:.2f}", delta=f"{zmiana:.2f}%")

        st.divider()

        # WYKRESY
        c1, c2 = st.columns(2)
        with c1:
            st.write("### Notowania historyczne (Cena USD)")
            st.plotly_chart(px.line(df, labels={"value": "Cena", "Date": "Data"}), use_container_width=True)
        with c2:
            st.write("### Porównanie siły (Skumulowany zwrot - Start = 100)")
            # To jest kluczowe dla prezentacji - normalizacja danych
            df_norm = (df / df.iloc[0]) * 100
            st.plotly_chart(px.line(df_norm, labels={"value": "Wzrost %", "Date": "Data"}), use_container_width=True)

        with st.expander("🔍 Szczegóły danych (Ostatnie 10 dni)"):
            st.dataframe(df.tail(10), use_container_width=True)
else:
    st.info("👈 Wybierz indeksy lub akcje z panelu bocznego.")
