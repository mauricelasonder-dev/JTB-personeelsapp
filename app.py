import streamlit as st
import pandas as pd

# Pagina instellingen
st.set_page_config(page_title="Personeelsportaal", layout="wide")

# Jouw unieke Sheet ID
SHEET_ID = "1f00UVHF6M2-Gp8jvSYlRXDaA7rKPotRcaBwJQGhFrsI"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

@st.cache_data(ttl=60)
def get_data():
    return pd.read_csv(CSV_URL)

st.title("🏢 Personeelsportaal")

try:
    df = get_data()
    
    # Tabs aanmaken voor de hoofdsecties
    tab1, tab2, tab3 = st.tabs(["Aanwezigheid per afdeling", "Telefoongids", "Handboek"])

    with tab1:
        st.header("Wie is er vandaag per afdeling?")
        
        # Zorg dat de kolomnaam 'Afdeling' bestaat
        if 'Afdeling' in df.columns:
            # Haal unieke afdelingen op en sorteer ze
            afdelingen_lijst = sorted(df['Afdeling'].dropna().unique().tolist())
            
            # Maak dynamisch sub-tabs aan voor elke afdeling
            subtabs = st.tabs(afdelingen_lijst)
            
            for i, afdeling in enumerate(afdelingen_lijst):
                with subtabs[i]:
                    # Filter de data voor de huidige afdeling
                    df_afdeling = df[df['Afdeling'] == afdeling]
                    # Toon de tabel
                    st.dataframe(df_afdeling[['Naam', 'Status']], use_container_width=True)
        else:
            st.warning("Kolom 'Afdeling' niet gevonden in de Google Sheet. Voeg deze kolom toe.")

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
    st.error("Er ging iets mis bij het ophalen van de data.")
    st.write("Foutmelding:", e)
