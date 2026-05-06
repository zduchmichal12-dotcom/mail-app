import streamlit as st
import google.generativeai as genai

# --- KONFIGURÁCIA ---
# Tvoj vložený API kľúč
API_KEY = "AIzaSyCnBWOiDHzd_9qzzCDX8XpA_7I2fl9jSXo"

# Nastavenie stránky
st.set_page_config(
    page_title="Hydrotech AI Email Assistant",
    page_icon="✉️",
    layout="centered"
)

# Inicializácia Gemini (používame najstabilnejšie nastavenie)
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Chyba pri konfigurácii API: {e}")

# Vlastný CSS štýl
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✉️ AI Email Assistant")
st.info("Nástroj na automatické písanie biznis mailov pre Hydrotech, a.s.")

# --- BOČNÝ PANEL ---
with st.sidebar:
    st.header("Nastavenia")
    # Používame čisté názvy, ktoré neskôr doplníme o prefix models/
    model_choice = st.selectbox("Model:", ["gemini-1.5-flash", "gemini-1.5-pro"])
    st.write("---")
    st.caption("Status: Pripojené")

# --- HLAVNÉ ROZHRANIE ---
vstupny_text = st.text_area(
    "Čo má byť v emaile? (fakty, body, nápady):",
    placeholder="Napríklad: Píšeme investorovi o struvite z Leopoldova, cena je dohodnutá, termín dodania budúci týždeň.",
    height=180
)

col1, col2 = st.columns(2)

with col1:
    ton = st.selectbox("Tón komunikácie:", [
        "Profesionálny a obchodný", 
        "Priateľský a neformálny", 
        "Dôrazný / Eskalačný", 
        "Stručný a technický"
    ])

with col2:
    jazyk = st.selectbox("Cieľový jazyk:", [
        "Angličtina", 
        "Slovenčina", 
        "Nemčina", 
        "Čeština"
    ])

# --- LOGIKA GENEROVANIA ---
if st.button("🚀 Vygenerovať profesionálny email"):
    if not vstupny_text:
        st.warning("Prosím, zadaj nejaké podklady pre email.")
    else:
        try:
            # KLÚČOVÁ OPRAVA: Pridávame prefix 'models/' priamo sem
            # Toto rieši chybu 404 z image_92329c.png
            full_model_name = f"models/{model_choice}"
            model = genai.GenerativeModel(model_name=full_model_name)
            
            prompt = f"""
            Si expert na biznis komunikáciu. Vytvor profesionálny email na základe týchto údajov:
            
            Podklady: {vstupny_text}
            Tón: {ton}
            Jazyk: {jazyk}
            
            Štruktúra:
            1. Predmet (Subject)
            2. Oslovenie
            3. Telo emailu
            4. Profesionálna rozlúčka
            """
            
            with st.spinner('AI pripravuje email...'):
                response = model.generate_content(prompt)
                
            st.success("Hotovo!")
            st.markdown("### Navrhovaný text:")
            st.code(response.text, language="text")
            st.balloons()
            
        except Exception as e:
            # Ak by models/ náhodou zlyhalo, skúsime to bez neho
            st.error(f"Chyba komunikácie: {e}")
            st.info("Tip: Ak chyba pretrváva, skús v bočnom paneli prepnúť model.")

st.markdown("---")
st.caption("© 2026 Hydrotech, a.s. | AI Email Assistant")
