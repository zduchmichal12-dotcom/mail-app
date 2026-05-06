import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Hydrotech Diagnostika")

# Načítanie kľúča zo Secrets (image_91af7e.png)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Kľúč sa nenašiel v Secrets: {e}")
    st.stop()

st.title("🔍 Diagnostika spojenia")

# TEST 1: Zoznam modelov
st.subheader("1. Test prístupu k modelom")
try:
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_actions]
    if models:
        st.success(f"Váš kľúč vidí tieto modely: {models}")
        selected_model = models[0]
    else:
        st.error("Váš kľúč vidí 0 modelov. Problém je v Google účte alebo regióne.")
        st.stop()
except Exception as e:
    st.error(f"Nepodarilo sa pripojiť k API: {e}")
    st.stop()

# TEST 2: Skúšobné generovanie
st.subheader("2. Test generovania")
vstup = st.text_input("Napíšte sem 'Ahoj':")

if st.button("🚀 Spustiť test"):
    try:
        model = genai.GenerativeModel(selected_model)
        # Pridáme nastavenie bezpečnosti, ktoré je v EÚ občas povinné
        res = model.generate_content("Napiš krátky pozdrav.")
        st.write("Odpoveď od AI:")
        st.info(res.text)
    except Exception as e:
        st.error(f"Generovanie zlyhalo: {e}")
