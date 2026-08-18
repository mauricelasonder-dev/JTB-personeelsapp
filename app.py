import streamlit as st
import pandas as pd

# Pagina instellingen
st.set_page_config(page_title="Personeelsportaal", layout="wide")

# WACHTWOORD CONFIGURATIE
PASSWORD = "Jtb2016!" # Verander dit naar je eigen wachtwoord

# GOOGLE SHEET CONFIGURATIE
SHEET_ID = "1f00UVHF6M2-Gp8jvSYlRXDaA7rKPotRcaBwJQGhFrsI" 

@st.cache_data(ttl=600)
def load_sheet(gid_nummer):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid_nummer}"
    return pd.read_csv(url)

def check_password():
    def password_entered():
        if st.session_state["password"] == PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔒 Inloggen Personeelsportaal")
        st.text_input("Voer het wachtwoord in om door te gaan:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.title("🔒 Inloggen Personeelsportaal")
        st.text_input("Voer het wachtwoord in om door te gaan:", type="password", on_change=password_entered, key="password")
        st.error("Wachtwoord onjuist. Probeer het opnieuw.")
        return False
    else:
        return True

# --- HOOFDPROGRAMMA ---
if check_password():
    st.title("🏢 Personeelsportaal")
    tab1, tab2, tab3 = st.tabs(["Aanwezigheid", "Telefoongids", "Handboek"])

    with tab1:
        st.header("Wie is er vandaag?")
        df = load_sheet("0")
        st.dataframe(df[['Naam', 'Status']], use_container_width=True)

    with tab2:
        st.header("Interne Telefoongids")
        df_tel = load_sheet("0")
        zoekterm = st.text_input("Zoek op naam of functie:")
        if zoekterm:
            df_tel = df_tel[df_tel['Naam'].str.contains(zoekterm, case=False, na=False) | 
                            df_tel['Functie'].str.contains(zoekterm, case=False, na=False)]
        st.dataframe(df_tel[['Naam', 'Functie', 'Telefoon']], use_container_width=True)

    with tab3:
        st.header("Personeelshandboek")
        st.write("Klik hieronder voor het personeelshandboek.")
        st.link_button("Open Handboek", "VOEG_HIER_JE_DRIVE_LINK_IN")
