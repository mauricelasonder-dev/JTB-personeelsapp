import streamlit as st
import pandas as pd
import datetime

# Pagina instellingen
st.set_page_config(page_title="Personeelsportaal", layout="wide")

# CONFIGURATIE
PASSWORD = "Jtb2016!" 
SHEET_ID = "1f00UVHf6M2-Gp8jvSYlRxDAa7rKPotRcaBwJQGHfRsI"
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
    # Zet hier je logo neer (zorg dat logo.png in dezelfde map staat)
    try:
        st.image("logo.png", width=300)
    except Exception:
        pass # Gaat geruisloos verder als het logo (nog) ontbreekt
        
    st.title("🏢 Personeelsportaal")
    
    @st.cache_data(ttl=60)
    def load_data():
        df_temp = pd.read_csv(CSV_URL)
        df_temp.columns = df_temp.columns.str.strip()
        return df_temp

    try:
        df = load_data()
        
        # Initialiseer tijdelijke statussen in session_state
        if "custom_statuses" not in st.session_state:
            st.session_state["custom_statuses"] = {}

        # Bepaal de dag van vandaag (0 = Maandag, 4 = Vrijdag)
        dagen_map = {0: "Ma", 1: "Di", 2: "Wo", 3: "Do", 4: "Vr", 5: "Za", 6: "Zo"}
        vandaag_code = dagen_map.get(datetime.datetime.today().weekday())

        # Functie om de actuele status te bepalen
        def bereken_status(row):
            naam = row['Naam']
            if naam in st.session_state["custom_statuses"]:
                return st.session_state["custom_statuses"][naam]
            
            if vandaag_code and vandaag_code in df.columns:
                werkdag_waarde = row[vandaag_code]
                if pd.notna(werkdag_waarde):
                    val_str = str(werkdag_waarde).strip().lower()
                    if val_str in ["1", "1.0", "waar", "true"]:
                        return "Aanwezig (Rooster)"
                    elif val_str in ["0.5", "0,5", "ochtend", "0.5 ochtend"]:
                        return "Aanwezig (Ochtend)"
                    elif val_str in ["middag", "0.5 middag"]:
                        return "Aanwezig (Middag)"
            
            return "Vrij (Rooster)"

        df['Actuele_Status'] = df.apply(bereken_status, axis=1)

        # Hoofdtabs van de app
        tab1, tab2, tab3 = st.tabs(["Aanwezigheid", "Telefoongids", "Personeelsgids"])

        with tab1:
            st.header("Wie is er vandaag?")
            
            # Direct op het beginscherm het inklapmenu
            with st.expander("🛠️ Zelf ziek, vrij of halve dag melden voor vandaag"):
                col_m, col_s, col_btn = st.columns([2, 2, 1])
                with col_m:
                    gekozen_naam = st.selectbox("Selecteer je naam:", df['Naam'].unique(), key="select_naam_1")
                with col_s:
                    nieuwe_status = st.selectbox(
                        "Status voor vandaag:", 
                        ["Aanwezig (Rooster)", "Aanwezig (Ochtend)", "Aanwezig (Middag)", "Ziek", "Vrij / Verlof"], 
                        key="select_status_1"
                    )
                with col_btn:
                    st.write("") 
                    st.write("")
                    if st.button("Opslaan"):
                        st.session_state["custom_statuses"][gekozen_naam] = nieuwe_status
                        st.success("Aangepast!")
                        st.rerun()

            st.markdown("---")

            # Afdelingen weergave op het beginscherm
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
            
            # Optionele zoekbalk bovenin voor als je direct iemand zoekt
            zoekterm = st.text_input("Zoek op naam of functie:", key="zoek_telefoon")
            
            if zoekterm and 'Naam' in df.columns and 'Functie' in df.columns:
                df_display = df[df['Naam'].str.contains(zoekterm, case=False, na=False) | 
                                df['Functie'].str.contains(zoekterm, case=False, na=False)]
                st.dataframe(df_display[['Naam', 'Afdeling', 'Functie', 'Telefoon']], use_container_width=True)
            else:
                # Als er niet gezocht wordt, tonen we de tab-structuur (Net zoals bij aanwezigheid)
                if 'Afdeling' in df.columns:
                    afdelingen_lijst = sorted(df['Afdeling'].dropna().unique().tolist())
                    telefoon_tabs = ["Totaaloverzicht"] + afdelingen_lijst
                    subtabs_tel = st.tabs(telefoon_tabs)
                    
                    # Totaaloverzicht telefoongids als EERSTE tabblad
                    with subtabs_tel[0]:
                        st.subheader("Totaaloverzicht Telefoongids")
                        st.dataframe(df[['Naam', 'Afdeling', 'Functie', 'Telefoon']], use_container_width=True)
                    
                    # Per afdeling telefoongids
                    for i, afdeling in enumerate(afdelingen_lijst):
                        with subtabs_tel[i + 1]:
                            st.subheader(f"Afdeling: {afdeling}")
                            df_afdeling = df[df['Afdeling'] == afdeling]
                            st.dataframe(df_afdeling[['Naam', 'Functie', 'Telefoon']], use_container_width=True)
                else:
                    st.dataframe(df[['Naam', 'Functie', 'Telefoon']], use_container_width=True)

        with tab3:
            st.header("Personeelsgids")
            st.write("Hier vind je het officiële personeelshandboek.")
            
            drive_link = "https://drive.google.com/file/d/1mfZn5Mm5355WGYYnqD8G3VUYvZXv7Oe9/preview"
            
            st.markdown(
                f'<a href="{drive_link}" target="_blank"><button style="background-color: #ff4b4b; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">📄 Open het Personeelshandboek</button></a>',
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error("Kon de data niet laden vanuit Google Sheets.")
        st.write("Details:", e)
        st.error("Kon de data niet laden vanuit Google Sheets.")
        st.write("Details:", e)
