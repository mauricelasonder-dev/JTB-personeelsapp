import streamlit as st
import pandas as pd
import datetime

# Pagina instellingen
st.set_page_config(page_title="Personeelsportaal", layout="wide")

# CONFIGURATIE
PASSWORD = "Jtb2016!" 
SHEET_ID = "1f00UVHF6M2-Gp8jvSYlRXDaA7rKPotRcaBwJQGhFrsI"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# Wachtwoord controle
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
    
    @st.cache_data(ttl=60)
    def load_data():
        return pd.read_csv(CSV_URL)

    try:
        df = load_data()
        
        # Initialiseer tijdelijke statussen in session_state als dat er nog niet is
        if "custom_statuses" not in st.session_state:
            st.session_state["custom_statuses"] = {}

        # Bepaal de dag van vandaag (0 = Maandag, 4 = Vrijdag)
        dagen_map = {0: "Ma", 1: "Di", 2: "Wo", 3: "Do", 4: "Vr", 5: "Za", 6: "Zo"}
        vandaag_code = dagen_map.get(datetime.datetime.today().weekday())

        # Functie om de actuele status te bepalen op basis van rooster + handmatige override
        def bereken_status(row):
            naam = row['Naam']
            # Als iemand handmatig iets heeft ingesteld voor vandaag, gebruik dat
            if naam in st.session_state["custom_statuses"]:
                return st.session_state["custom_statuses"][naam]
            
            # Anders kijken naar het rooster voor vandaag
            if vandaag_code and vandaag_code in df.columns:
                werkdag_waarde = row[vandaag_code]
                if pd.notna(werkdag_waarde) and str(werkdag_waarde).strip() in ["1", "1.0", "waar", "True"]:
                    return "Aanwezig (Rooster)"
            
            return "Vrij (Rooster)"

        df['Actuele_Status'] = df.apply(bereken_status, axis=1)

        # Hoofdtabs van de app
        tab1, tab2, tab3, tab4 = st.tabs(["Aanwezigheid", "Telefoongids", "Zelf Ziek/Vrij melden", "Handboek"])

        with tab1:
            st.header("Wie is er vandaag?")
            
            if 'Afdeling' in df.columns:
                afdelingen_lijst = sorted(df['Afdeling'].dropna().unique().tolist())
                alle_tabs = ["Totaaloverzicht"] + afdelingen_lijst
                subtabs = st.tabs(alle_tabs)
                
                # Totaaloverzicht
                with subtabs[0]:
                    st.subheader("Totaaloverzicht alle medewerkers")
                    st.dataframe(df[['Naam', 'Afdeling', 'Actuele_Status']], use_container_width=True)
                
                # Per afdeling
                for i, afdeling in enumerate(afdelingen_lijst):
                    with subtabs[i + 1]:
                        st.subheader(f"Afdeling: {afdeling}")
                        df_afdeling = df[df['Afdeling'] == afdeling]
                        st.dataframe(df_afdeling[['Naam', 'Actuele_Status']], use_container_width=True)
            else:
                st.dataframe(df[['Naam', 'Actuele_Status']], use_container_width=True)

        with tab2:
            st.header("Interne Telefoongids")
            zoekterm = st.text_input("Zoek op naam of functie:")
            
            df_display = df
            if zoekterm and 'Naam' in df.columns and 'Functie' in df.columns:
                df_display = df[df['Naam'].str.contains(zoekterm, case=False, na=False) | 
                                df['Functie'].str.contains(zoekterm, case=False, na=False)]
            
            st.dataframe(df_display[['Naam', 'Functie', 'Telefoon']], use_container_width=True)

        with tab3:
            st.header("Status wijzigen (Ziek / Vrij)")
            st.write("Geef hieronder aan als je vandaag afwijkt van je rooster (bijv. ziek of extra vrij).")
            
            col_m, col_s = st.columns(2)
            with col_m:
                gekozen_naam = st.selectbox("Selecteer je naam:", df['Naam'].unique())
            with col_s:
                nieuwe_status = st.selectbox("Status voor vandaag:", ["Aanwezig", "Ziek", "Vrij / Verlof"])
            
            if st.button("Status Opslaan"):
                st.session_state["custom_statuses"][gekozen_naam] = nieuwe_status
                st.success(𒄑 f"De status voor {gekozen_naam} is succesvol aangepast naar '{nieuwe_status}' voor vandaag!")
                st.rerun()

        with tab4:
            st.header("Personeelshandboek")
            st.info("Het personeelshandboek volgt binnenkort.")

    except Exception as e:
        st.error("Kon de data niet laden vanuit Google Sheets.")
        st.write("Details:", e)
