import streamlit as st
import pandas as pd

# Pagina instellingen
st.set_page_config(page_title="Personeelsportaal", layout="wide")

# CONFIGURATIE
PASSWORD = "Jtb2016!" 
SHEET_ID = "1f00UVHF6M2-Gp8jvSYlRXDaA7rKPotRcaBwJQGhFrsI"

# Deze URL-structuur werkt feilloos voor publieke Google Sheets
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔒 Inloggen")
        if st.text_input("Wachtwoord", type="password", key="pwd_input") == PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        return False
    return st.session_state["password_correct"]

if check_password():
    st.title("🏢 Personeelsportaal")
    
    @st.cache_data(ttl=60)
    def load_data():
        return pd.read_csv(CSV_URL)

    try:
        df = load_data()
        
        # Tabs aanmaken
        tab1, tab2, tab3 = st.tabs(["Aanwezigheid", "Telefoongids", "Handboek"])

        with tab1:
            st.header("Wie is er vandaag?")
            st.dataframe(df[['Naam', 'Status']], use_container_width=True)

        with tab2:
            st.header("Interne Telefoongids")
            zoekterm = st.text_input("Zoek op naam of functie:")
            
            df_display = df
            if zoekterm:
                df_display = df[df['Naam'].str.contains(zoekterm, case=False, na=False) | 
                                df['Functie'].str.contains(zoekterm, case=False, na=False)]
            
            st.dataframe(df_display[['Naam', 'Functie', 'Telefoon']], use_container_width=True)

        with tab3:
            st.header("Personeelshandboek")
            st.info("Het personeelshandboek volgt binnenkort.")

    except Exception as e:
        st.error("Kon de data niet laden.")
        st.write("Details:", e)
