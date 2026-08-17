import streamlit as st
import pandas as pd

# Pagina instellingen
st.set_page_config(page_title="Personeelsportaal", layout="wide")

# VUL HIER JOUW SHEET ID IN
SHEET_ID = "JOUW_SHEET_ID" 

# Functie om data op te halen via de CSV-export link van Google Sheets
@st.cache_data(ttl=600)
def load_sheet(tabblad):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={tabblad}"
    return pd.read_csv(url)

st.title("🏢 Personeelsportaal")
tab1, tab2, tab3 = st.tabs(["Aanwezigheid", "Telefoongids", "Handboek"])

# --- TAB 1: AANWEZIGHEID ---
with tab1:
    st.header("Wie is er vandaag?")
    df = load_sheet("Medewerkers")
    st.dataframe(df[['Naam', 'Status']], use_container_width=True)

# --- TAB 2: TELEFOONGIDS ---
with tab2:
    st.header("Interne Telefoongids")
    df_tel = load_sheet("Medewerkers")
    zoekterm = st.text_input("Zoek op naam of functie:")
    if zoekterm:
        df_tel = df_tel[df_tel['Naam'].str.contains(zoekterm, case=False, na=False) | 
                        df_tel['Functie'].str.contains(zoekterm, case=False, na=False)]
    st.dataframe(df_tel[['Naam', 'Functie', 'Telefoon']], use_container_width=True)

# --- TAB 3: HANDBOEK ---
with tab3:
    st.header("Personeelshandboek")
    st.write("Klik hieronder voor het personeelshandboek.")
    st.link_button("Open Handboek", "VOEG_HIER_JE_DRIVE_LINK_IN")