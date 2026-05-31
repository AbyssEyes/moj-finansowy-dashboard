import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# 1. KONFIGURACJA STRONY
st.set_page_config(page_title="Pro-Investor Dashboard", layout="wide")

st.title("🏛️ Zaawansowany Dashboard Rynkowy")
st.markdown("Interaktywna analiza największych spółek USA oraz kluczowych funduszy ETF.")

# 2. BAZA AKTYWÓW (Słownik podzielony na kategorie)
AKTYWA = {
    "Indeksy (ETF)": {
        "SPY": "S&P 500 (Rynek USA)",
        "QQQ": "NASDAQ 100 (Technologia)",
        "DIA": "Dow Jones (Przemysł)",
        "IWM": "Russell 2000 (Małe spółki)",
        "EEM": "Emerging Markets (Rynki wschodzące)",
        "VTI": "Total Stock Market (Cały rynek USA)"
    },
    "Giganci Technologiczni": {
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "GOOGL": "Alphabet (Google)",
        "AMZN": "Amazon",
        "NVDA": "NVIDIA",
        "TSLA": "Tesla",
        "META": "Meta (Facebook)"
    },
    "Finanse i Przemysł": {
        "JPM": "JPMorgan Chase",
        "BRK-B": "Berkshire Hathaway",
        "V": "Visa",
        "UNH": "UnitedHealth Group",
        "XOM": "Exxon Mobil"
    },
    "Surowce i Krypto": {
        "GLD": "Złoto (Gold ETF)",
        "SLV": "Srebro (Silver ETF)",
        "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum"
    }
}

# 3. PANEL BOCZNY - FILTRY
st.sidebar.header("🔍 Filtry i Ustawienia")

# Wybór aktywów
wybrane_kategorie = st.sidebar.multiselect("Filtruj kategorie:", list(AKTYWA.keys()), default=["Indeksy (ETF)", "Giganci Technologiczni"])

dostepne_opcje = {}
for kat in wybrane_kategorie:
    dostepne_opcje.update(AKTYWA[kat])

wybrane_nazwy = st.sidebar.multiselect("Wybierz konkretne symbole:", options=list(dostepne_opcje.values()), default=[dostepne_opcje["SPY"], dostepne_opcje["AAPL"]])

# Mapowanie nazw na tickery
wybrane_tickery = [t for t, nazwa in dostepne_opcje.items() if nazwa in wybrane_nazwy]

# Zakres dat
st.sidebar.subheader("Okres analizy")
col_d1, col_d2 = st.sidebar.columns(2)
d_start = col_d1.date_input("Od", datetime.now() - timedelta(days=365))
d_end = col_d2.date_input("Do", datetime.now())

# Interwał i techniczne
interwal = st.sidebar.selectbox("Interwał danych:", ["1d", "1wk", "1mo"], index=0)
st.sidebar.subheader("Analiza techniczna")
pokaz_srednia = st.sidebar.checkbox("Pokaż średnią kroczącą (SMA 50)")

# 4. FUNKCJA POBIERANIA DANYCH (Odporna na błędy Series/DataFrame)
@st.cache_data(ttl=3600)
def pobierz_dane(symbole, start, end, interval):
    if not symbole:
        return pd.DataFrame()
    dane = yf.download(symbole, start=start, end=end, interval=interval)['Close']
    
    # Naprawa dla jednego wyboru (zamiana Series na DataFrame)
    if isinstance(dane, pd.Series):
        dane = dane.to_frame()
        dane.columns = symbole
    return dane

# 5. LOGIKA GŁÓWNA
if wybrane_tickery:
    df = pobierz_dane(wybrane_tickery, d_start, d_end, interwal)
    
    if not df.empty:
        # WSKAŹNIKI KPI
        st.subheader("📌 Podsumowanie okresu")
        cols = st.columns(len(wybrane_tickery))
        for i, t in enumerate(wybrane_tickery):
            c_start = df[t].dropna().iloc[0]
            c_end = df[t].dropna().iloc[-1]
            zmiana = ((c_end - c_start) / c_start) * 100
            cols[i].metric(t, f"{c_end:.2f} $", f"{zmiana:.2f}%")

        st.divider()

        # WYKRESY
        tab1, tab2 = st.tabs(["📈 Notowania", "⚖️ Porównanie Wydajności"])

        with tab1:
            st.write("### Kurs rynkowy")
            fig_price = px.line(df, labels={"value": "Cena (USD)", "Date": "Data"})
            
            if pokaz_srednia and len(wybrane_tickery) == 1:
                sma = df.rolling(window=50).mean()
                fig_price.add_scatter(x=sma.index, y=sma[wybrane_tickery[0]], name="SMA 50", line=dict(dash='dash'))
            elif pokaz_srednia:
                st.warning("Średnia krocząca na wykresie głównym działa najlepiej dla jednego wybranego aktywa.")
                
            st.plotly_chart(fig_price, use_container_width=True)

        with tab2:
            st.write("### Zwrot skumulowany (Start = 100)")
            # Normalizacja danych
            df_norm = (df / df.dropna().iloc[0]) * 100
            fig_norm = px.area(df_norm, labels={"value": "Wzrost %", "Date": "Data"}, facets_col_wrap=2)
            st.plotly_chart(fig_norm, use_container_width=True)

        # SZCZEGÓŁY
        with st.expander("📊 Widok tabelaryczny i statystyki"):
            st.write("Statystyki opisowe:")
            st.dataframe(df.describe(), use_container_width=True)
            st.write("Ostatnie notowania:")
            st.dataframe(df.tail(15), use_container_width=True)
else:
    st.info("Dodaj symbole w panelu bocznym, aby wyświetlić analizę.")

st.caption("Dashboard stworzony przy użyciu Streamlit, yFinance i Plotly. Dane mogą być opóźnione.")
