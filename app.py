import streamlit as st
import pandas as pd

# Pagina instellingen
st.set_page_config(page_title="Personeelsportaal", layout="wide")

# CONFIGURATIE
PASSWORD = "Jtb2016!" 
SHEET_ID = "1f00UVHF6M2-Gp8jvSYlRXDaA7rKPotRcaBwJQGhFrsI"

# Wachtwoord controle functie
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔒 Inloggen Personeelsportaal")
        pwd = st.text_input("Voer het wachtwoord in:", type="password", key="pwd_input")
        if pwd == PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        elif pwd:
            st.error("Verkeerd wachtwoord.")
        return False
    return st.session_state["password_correct"]

if check_password():
    st.title("🏢 Personeelsportaal")
    
    # We gebruiken een alternatieve, stabiele methode om de data op te halen
    @st.cache_data(ttl=60)
    def load_data():
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Medewerkers"
        return pd.read_csv(url)

    try:
        df = load_data()
        
        # Tabs aanmaken
        tab1, tab2, tab3 = st.tabs(["Aanwezigheid", "Telefoongids", "Handboek"])

        with tab1:
            st.header("Wie is er vandaag?")
            if 'Naam' in df.columns and 'Status' in df.columns:
                st.dataframe(df[['Naam', 'Status']], use_container_width=True)
            else:
                st.warning("De kolommen 'Naam' of 'Status' konden niet gevonden worden in de Google Sheet.")

        with tab2:
            st.header("Interne Telefoongids")
            zoekterm = st.text_input("Zoek op naam of functie:")
            
            df_display = df
            if zoekterm and 'Naam' in df.columns and 'Functie' in df.columns:
                df_display = df[df['Naam'].str.contains(zoekterm, case=False, na=False) | 
                                df['Functie'].str.contains(zoekterm, case=False, na=False)]
            
            if 'Naam' in df.columns and 'Functie' in df.columns and 'Telefoon' in df.columns:
                st.dataframe(df_display[['Naam', 'Functie', 'Telefoon']], use_container_width=True)
            else:
                st.dataframe(df_display, use_container_width=True)

        with tab3:
            st.header("Personeelshandboek")
            st.info("Het personeelshandboek volgt binnenkort.")

    except Exception as e:
        st.error("Kon de data niet laden vanuit Google Sheets.")
        st.write("Controleer of de Google Sheet gedeeld is met 'Iedereen met de link' (Lezer). Technische details:", e)
