import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# 1. KONFIGURACJA STRONY
st.set_page_config(
    page_title="InwestorVision - Dashboard ETF & Akcji",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stylizacja nagłówka
st.title("📈 Dashboard Analizy Rynkowej")
st.markdown("""
Ta aplikacja monitoruje dane giełdowe w czasie rzeczywistym. 
Wykorzystuje **yfinance** do pobierania danych, **Plotly** do wizualizacji i **Streamlit** jako interfejs.
""")

# 2. PANEL BOCZNY (SIDEBAR)
st.sidebar.header("⚙️ Ustawienia Analizy")

# Wybór aktywów
popularne_tickery = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "SPY", "QQQ", "VTI", "BTC-USD"]
wybrane_aktywa = st.sidebar.multiselect(
    "Wybierz symbole do porównania:",
    popularne_tickery,
    default=["AAPL", "SPY"]
)

# Wybór zakresu dat
st.sidebar.subheader("Zakres czasu")
data_start = st.sidebar.date_input("Data początkowa", datetime.now() - timedelta(days=365))
data_koniec = st.sidebar.date_input("Data końcowa", datetime.now())

# 3. FUNKCJA POBIERANIA DANYCH (Z CACHEM)
@st.cache_data(ttl=3600) # Dane cache'owane przez godzinę
def pobierz_notowania(symbole, start, end):
    if not symbole:
        return pd.DataFrame()
    # Pobieramy ceny zamknięcia
    dane = yf.download(symbole, start=start, end=end)['Close']
    
    # Jeśli wybrano tylko jeden ticker, yfinance zwraca Series, konwertujemy na DF
    if len(symbole) == 1:
        dane = dane.to_frame()
        dane.columns = symbole
    return dane

# 4. LOGIKA GŁÓWNA
if wybrane_aktywa:
    df = pobierz_notowania(wybrane_aktywa, data_start, data_koniec)
    
    if not df.empty:
        # WSKAŹNIKI KPI (Kluczowe wyniki na górze)
        st.subheader("🚀 Aktualne ceny i zmiana")
        kolumny_kpi = st.columns(len(wybrane_aktywa))
        
        for i, ticker in enumerate(wybrane_aktywa):
            cena_akt = df[ticker].iloc[-1]
            cena_poprzednia = df[ticker].iloc[0]
            zmiana_proc = ((cena_akt - cena_poprzednia) / cena_poprzednia) * 100
            
            kolumny_kpi[i].metric(
                label=ticker,