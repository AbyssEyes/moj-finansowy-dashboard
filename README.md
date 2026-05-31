# 🏛️ Globalny Dashboard Inwestycyjny - Projekt Akademicki

## 📝 Opis Projektu
Projekt został przygotowany jako narzędzie do interaktywnej analizy danych giełdowych w czasie rzeczywistym. Aplikacja pozwala na monitorowanie kluczowych indeksów (ETF), największych spółek amerykańskich (Big Tech) oraz kryptowalut. 

Głównym celem projektu było wykorzystanie bibliotek analizy danych w języku Python do stworzenia w pełni reaktywnego dashboardu analitycznego, który wspomaga podejmowanie decyzji inwestycyjnych poprzez wizualizację trendów i wydajności relatywnej aktywów.

## 🚀 Funkcje Aplikacji
- **Dane Real-Time**: Integracja z API Yahoo Finance (`yfinance`) zapewnia zawsze aktualne notowania.
- **Zaawansowane Filtrowanie Czasowe**: Predefiniowane zakresy (1T, 1M, YTD, 1R, 5L) oraz własny kalendarz.
- **Analiza Porównawcza (Normalizacja)**: Funkcja sprowadzania cen różnych aktywów do wspólnej bazy (Start = 100), co pozwala na obiektywne porównanie stóp zwrotu.
- **Analiza Techniczna**: Możliwość nałożenia średniej kroczącej (SMA 50) w celu identyfikacji trendów średnioterminowych.
- **Wizualizacja "Small Multiples"**: Rozbicie wykresów wydajności na osobne panele (faceting) dla zwiększenia czytelności przy wielu aktywach.
- **Responsywny Interfejs**: Dynamiczne wskaźniki KPI (metryki wzrostu) dopasowujące się do wybranych danych.

## 🛠️ Stack Technologiczny
- **Język**: Python 3.x
- **Framework UI**: [Streamlit](https://streamlit.io/)
- **Wizualizacja**: [Plotly Express](https://plotly.com/python/)
- **Przetwarzanie danych**: Pandas, NumPy
- **Źródło danych**: yFinance API

## 📦 Instalacja i Uruchomienie Lokalne

1. Sklonuj repozytorium:
   ```bash
   git clone [https://github.com/TWOJA-NAZWA-UZYTKOWNIKA/moj-finansowy-dashboard.git](https://github.com/TWOJA-NAZWA-UZYTKOWNIKA/moj-finansowy-dashboard.git)
