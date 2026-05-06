import streamlit as st
import google.generativeai as genai

# --- KONFIGURÁCIA ---
API_KEY = "AIzaSyCnBWOiDHzd_9qzzCDX8XpA_7I2fl9jSXo"

st.set_page_config(page_title="Hydrotech AI Email Assistant", page_icon="✉️")

# Inicializácia API
genai.configure(api_key=API_KEY)

# --- FUNKCIA NA ZÍSKANIE MODELU ---
def get_safe_model(model_name):
    # Skúsime model s prefixom models/ (nový štandard)
    return genai.GenerativeModel(model_name=f"models/{model_name}")

st.title("✉️ AI Email Assistant")

# --- VÝBER MODELU (AKTUALIZOVANÉ NA ROK 2026) ---
with st.sidebar:
    st.header("Nastavenia")
    # Zmenili sme názvy na aktuálne dostupné modely
    model_choice = st.selectbox("Model:", [
        "gemini-2.0-flash", 
        "gemini-1.5-pro",
        "gemini-1.5-flash"
    ])
    st.caption("Poznámka: Ak verzia 2.0 nefunguje, prepnite na 1.5.")

# --- ROZHRANIE ---
vstupny_text = st.text_area("Čo má byť v emaile?", height=150)
col1, col2 = st.columns(2)
with col1:
    ton = st.selectbox("Tón:", ["Profesionálny", "Priateľský", "Eskalačný"])
with col2:
    jazyk = st.selectbox("Jazyk:", ["Angličtina", "Slovenčina", "Nemčina"])

if st.button("🚀 Vygenerovať email"):
    if not vstupny_text:
        st.warning("Zadajte text.")
    else:
        try:
            # Voláme model pomocou našej bezpečnej funkcie
            model = get_safe_model(model_choice)
            
            prompt = f"Vytvor {ton} email v jazyku {jazyk} na tému: {vstupny_text}"
            
            with st.spinner('AI pracuje...'):
                response = model.generate_content(prompt)
                
            st.success("Email vygenerovaný!")
            st.code(response.text, language="text")
            
        except Exception as e:
            # Ak model neexistuje, vypíšeme zoznam dostupných modelov pre ladenie
            st.error(f"Chyba: {e}")
            st.info("Pokúšam sa zistiť dostupné modely pre váš kľúč...")
            try:
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_actions]
                st.write("Dostupné modely na vašom účte:", available_models)
            except:
                st.write("Nepodarilo sa načítať zoznam modelov. Skontrolujte API kľúč.")
