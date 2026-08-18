import streamlit as st
import pandas as pd

# Pagina instellingen
st.set_page_config(page_title="Personeelsportaal", layout="wide")

# CONFIGURATIE
PASSWORD = "Jtb2016!" 
SHEET_ID = "1f00UVHF6M2-Gp8jvSYlRXDaA7rKPotRcaBwJQGhFrsI"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔒 Inloggen")
        if st.text_input("Wachtwoord", type="password") == PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        return False
    return st.session_state["password_correct"]

if check_password():
    st.title("🏢 Personeelsportaal")
    
    @st.cache_data(ttl=60)
    def load_data():
        # We proberen de data in te laden
        return pd.read_csv(CSV_URL)

    try:
        df = load_data()
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["Aanwezigheid", "Telefoongids", "Handboek"])

        with tab1:
            st.dataframe(df[['Naam', 'Status']], use_container_width=True)

        with tab2:
            st.dataframe(df[['Naam', 'Functie', 'Telefoon']], use_container_width=True)
            
        with tab3:
            st.write("Handboek volgt.")

    except Exception as e:
        st.error("Kon de data niet laden.")
        st.write("Details:", e)
