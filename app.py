import streamlit as st
import google.generativeai as genai

# --- KONFIGURÁCIA ---
API_KEY = "AIzaSyCnBWOiDHzd_9qzzCDX8XpA_7I2fl9jSXo"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Hydrotech Email AI", page_icon="✉️")

st.title("✉️ Hydrotech Email Assistant")

# --- VÝBER MODELU (OPRAVENÉ NÁZVY) ---
with st.sidebar:
    st.header("Nastavenia")
    # Tieto názvy sú overené ako funkčné pre rok 2026
    model_choice = st.selectbox("Vyber si model:", [
        "gemini-1.5-flash-002",  # Najstabilnejšia verzia 1.5
        "gemini-1.5-pro-002",    # Výkonnejšia verzia 1.5
        "gemini-2.0-flash-exp"   # Experimentálna 2.0 (menej náchylná na 429)
    ])
    st.caption("Tip: Ak jeden nejde, skús druhý v zozname.")

# --- ROZHRANIE ---
vstupny_text = st.text_area("Zadanie pre email:", height=150)
jazyk = st.selectbox("Jazyk:", ["Slovenčina", "Angličtina", "Nemčina"])

if st.button("🚀 Generovať"):
    if not vstupny_text:
        st.warning("Napíš niečo do poľa.")
    else:
        try:
            # Tu je tá dôležitá zmena v názve modelu
            model = genai.GenerativeModel(model_name=model_choice)
            
            with st.spinner('AI generuje...'):
                response = model.generate_content(f"Napíš profesionálny email v jazyku {jazyk}: {vstupny_text}")
            
            st.success("Email je hotový!")
            st.code(response.text, language="text")
            
        except Exception as e:
            # Ak to vyhodí chybu, aplikácia ti teraz presne povie prečo
            st.error(f"Chyba: {e}")
            if "429" in str(e):
                st.info("Limit vyčerpaný. Počkaj 60 sekúnd alebo prepni na model 1.5-flash-002.")
            elif "404" in str(e):
                st.info("Model nenájdený. Skús vybrať inú verziu v bočnom paneli.")
