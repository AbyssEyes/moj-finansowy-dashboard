import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# 1. KONFIGURACJA STRONY
st.set_page_config(page_title="Pro-Investor Dashboard", layout="wide")

st.title("🏛️ Globalny Dashboard Inwestycyjny")
st.markdown("Analiza trendów rynkowych w oparciu o dane czasu rzeczywistego.")

# 2. DEFINICJA AKTYWÓW I MAPOWANIE NAZW
# Klucz to Ticker (używany przez API), Wartość to Pełna Nazwa (dla użytkownika)
AKTYWA = {
    "Indeksy (ETF)": {
        "SPY": "S&P 500 (USA)",
        "QQQ": "NASDAQ 100 (Technologia)",
        "DIA": "Dow Jones (Przemysł)",
        "IWM": "Russell 2000 (Małe spółki)",
        "EEM": "Emerging Markets (Rynki wschodzące)",
        "VTI": "Total Market (USA)"
    },
    "Giganci Technologiczni": {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft",
        "GOOGL": "Alphabet (Google)",
        "AMZN": "Amazon",
        "NVDA": "NVIDIA",
        "TSLA": "Tesla",
        "META": "Meta Platforms"
    },
    "Surowce i Krypto": {
        "GLD": "Złoto (Gold)",
        "SLV": "Srebro (Silver)",
        "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum"
    }
}

# Tworzymy słownik pomocniczy do szybkiego wyszukiwania: Ticker -> "Ticker - Nazwa"
TICKER_TO_FULL = {}
for kat in AKTYWA.values():
    for t, nazwa in kat.items():
        TICKER_TO_FULL[t] = f"{t} - {nazwa}"

# 3. PANEL BOCZNY - FILTRY
st.sidebar.header("🔍 Ustawienia")

wybrane_kategorie = st.sidebar.multiselect("Kategorie:", list(AKTYWA.keys()), default=["Indeksy (ETF)"])

# Budujemy listę dostępnych opcji wyświetlanych jako "Ticker - Nazwa"
opcje_wyswietlane = []
for kat in wybrane_kategorie:
    for t, nazwa in AKTYWA[kat].items():
        opcje_wyswietlane.append(f"{t} - {nazwa}")

wybrane_pelne_nazwy = st.sidebar.multiselect(
    "Wybierz aktywa:", 
    options=opcje_wyswietlane, 
    default=[opcje_wyswietlane[0]] if opcje_wyswietlane else []
)

# Wyciągamy same tickery do zapytania API
wybrane_tickery = [n.split(" - ")[0] for n in wybrane_pelne_nazwy]

st.sidebar.subheader("Okres i technika")
d_start = st.sidebar.date_input("Data od", datetime.now() - timedelta(days=365))
pokaz_srednia = st.sidebar.checkbox("Pokaż SMA 50 (tylko dla 1 aktywa)")

# 4. FUNKCJA POBIERANIA DANYCH
@st.cache_data(ttl=3600)
def pobierz_dane(symbole, start):
    if not symbole: return pd.DataFrame()
    dane = yf.download(symbole, start=start)['Close']
    if isinstance(dane, pd.Series):
        dane = dane.to_frame()
        dane.columns = symbole
    return dane

# 5. LOGIKA GŁÓWNA
if wybrane_tickery:
    df = pobierz_dane(wybrane_tickery, d_start)
    
    if not df.empty:
        # Zmiana nazw kolumn w DataFrame na "Ticker - Pełna Nazwa"
        # Dzięki temu Plotly automatycznie użyje tych nazw w legendach i na wykresach
        df_display = df.rename(columns=TICKER_TO_FULL)
        wybrane_kolumny_full = [TICKER_TO_FULL[t] for t in wybrane_tickery]

        # WSKAŹNIKI KPI
        st.subheader("📌 Podsumowanie rynkowe")
        cols = st.columns(len(wybrane_kolumny_full))
        for i, col_name in enumerate(wybrane_kolumny_full):
            seria = df_display[col_name].dropna()
            c_start, c_end = seria.iloc[0], seria.iloc[-1]
            zmiana = ((c_end - c_start) / c_start) * 100
            cols[i].metric(label=col_name, value=f"{c_end:.2f} $", delta=f"{zmiana:.2f}%")

        st.divider()

        tab1, tab2 = st.tabs(["📈 Kursy Walutowe", "⚖️ Analiza Porównawcza"])

        with tab1:
            fig_price = px.line(df_display, labels={"value": "Cena (USD)", "Date": "Data"})
            if pokaz_srednia and len(wybrane_tickery) == 1:
                sma = df_display.rolling(window=50).mean()
                fig_price.add_scatter(x=sma.index, y=sma[wybrane_kolumny_full[0]], name="SMA 50 (Trend)")
            st.plotly_chart(fig_price, use_container_width=True)

        with tab2:
            st.write("### Wydajność skumulowana (Small Multiples)")
            df_norm = (df_display / df_display.iloc[0]) * 100
            df_long = df_norm.reset_index().melt(id_vars='Date', var_name='Aktywo', value_name='Wzrost')
            
            fig_norm = px.area(
                df_long, x='Date', y='Wzrost', color='Aktywo',
                facet_col='Aktywo', facet_col_wrap=2,
                labels={"Wzrost": "Wzrost %"},
                height=400 * ((len(wybrane_tickery) + 1) // 2)
            )
            fig_norm.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
            st.plotly_chart(fig_norm, use_container_width=True)
else:
    st.info("👈 Wybierz aktywa z panelu bocznego.")
