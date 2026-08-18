import streamlit as st
import pandas as pd
import datetime

# Pagina instellingen
st.set_page_config(page_title="Personeelsportaal", layout="wide")

SHEET_ID = "1f00UVHf6M2-Gp8jvSYlRxDAa7rKPotRcaBwJQGHfRsI"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

@st.cache_data(ttl=60)
def get_data():
    return pd.read_csv(CSV_URL)

st.title("🏢 Personeelsportaal")

# 1. Bepaal de dag van vandaag
dagen = ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"]
vandaag_index = datetime.datetime.today().weekday() # 0=Ma, 4=Vr
dag_naam = dagen[vandaag_index] if vandaag_index < 5 else None

try:
    df = get_data()

    # 2. Status berekenen
    # Als de status kolom leeg is, kijk naar het rooster
    def bepaal_status(row):
        if pd.notna(row['Status']) and row['Status'] != "Aanwezig":
            return row['Status'] # Gebruiker heeft handmatig iets anders ingevuld
        if dag_naam and row.get(dag_naam) == 1:
            return "Aanwezig"
        return "Vrij (Rooster)"

    df['Actuele_Status'] = df.apply(bepaal_status, axis=1)

    tab1, tab2, tab3 = st.tabs(["Aanwezigheid", "Telefoongids", "Zelf Status Wijzigen"])

    with tab1:
        # Hier komt je bestaande afdelingen/totaaloverzicht logica
        # Gebruik df['Actuele_Status'] in plaats van df['Status']
        st.dataframe(df[['Naam', 'Afdeling', 'Actuele_Status']], use_container_width=True)

    with tab3:
        st.header("Geef je status door")
        naam = st.selectbox("Selecteer je naam:", df['Naam'].unique())
        nieuwe_status = st.selectbox("Nieuwe status:", ["Aanwezig", "Ziek", "Vrij"])
        if st.button("Opslaan"):
            st.warning("Let op: Omdat we met een CSV-link werken, is dit een visuele wijziging. Voor echte opslag in Google Sheets is een Google-API koppeling (Gspread) nodig.")
            st.write(f"Status voor {naam} gewijzigd naar {nieuwe_status}")

except Exception as e:
    st.error(f"Fout bij laden: {e}")
