import streamlit as st
import google.generativeai as genai

# --- KONFIGURÁCIA ---
# Tvoj vložený API kľúč
API_KEY = "AIzaSyCnBWOiDHzd_9qzzCDX8XpA_7I2fl9jSXo"

# Inicializácia Gemini
genai.configure(api_key=API_KEY)

# Nastavenie stránky
st.set_page_config(
    page_title="Hydrotech AI Email Assistant",
    page_icon="✉️",
    layout="centered"
)

# Vlastný CSS štýl pre lepšie zobrazenie
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✉️ AI Email Assistant")
st.info("Tento nástroj automaticky generuje a prekladá biznis emaily pomocou Gemini 1.5 Flash.")

# Výber modelu v bočnom paneli (nepovinné, ale užitočné)
with st.sidebar:
    st.header("Nastavenia AI")
    model_choice = st.selectbox("Vyber si model:", ["gemini-1.5-flash-latest", "gemini-1.5-pro-latest"])
    st.write("---")
    st.caption("Verzia aplikácie: 1.0 (Stable)")

# --- HLAVNÉ ROZHRANIE ---
vstupny_text = st.text_area(
    "Čo má byť v emaile? (napíš fakty, pokojne v bodoch alebo nespisovne):",
    placeholder="Príklad: Píšeme investorovi, že 20kg struvitu zoženieme z liehovaru v Leopoldove...",
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
        "Čeština",
        "Poľština"
    ])

# --- LOGIKA GENEROVANIA ---
if st.button("🚀 Vygenerovať profesionálny email"):
    if not vstupny_text:
        st.warning("Najprv napíš nejaký text alebo body, ktoré chceš do mailu zahrnúť.")
    else:
        try:
            # Výber modelu
            model = genai.GenerativeModel(model_choice)
            
            # Systémové inštrukcie (Prompt)
            prompt = f"""
            Si expert na biznis komunikáciu. Tvojou úlohou je vytvoriť profesionálny email.
            
            Zadanie od používateľa: {vstupny_text}
            Požadovaný tón: {ton}
            Požadovaný jazyk: {jazyk}
            
            Pokyny:
            1. Navrhni výstižný Predmet (Subject) v danom jazyku.
            2. Ak je zadanie v slovenčine a cieľový jazyk je angličtina, urob kvalitný preklad a štylizáciu.
            3. Používaj biznis etiketu (oslovenie, pozdrav).
            4. Ak je tón eskalačný, buď priamy a seriózny, ale nie vulgárny.
            5. Ak sú v texte mená (napr. p. Karas), zakomponuj ich správne.
            """
            
            with st.spinner('AI premýšľa a píše email...'):
                response = model.generate_content(prompt)
                
            st.success("Email bol úspešne vygenerovaný!")
            
            # Zobrazenie výsledku
            st.markdown("### Výsledok:")
            st.code(response.text, language="text")
            
            st.balloons() # Malá animácia pre radosť z úspechu
            
        except Exception as e:
            st.error(f"Vyskytla sa chyba pri komunikácii s AI: {e}")

# Päta stránky
st.markdown("---")
st.caption("© 2026 Hydrotech, a.s. | Powered by Google Gemini")
