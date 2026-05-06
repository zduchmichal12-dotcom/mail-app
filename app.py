import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Hydrotech AI Final", page_icon="✉️")
st.title("✉️ Hydrotech Email Assistant")

# --- KONTROLA SYSTÉMU ---
st.sidebar.info(f"Verzia knižnice: {genai.__version__}")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Nastavte GEMINI_API_KEY v Secrets!")
    st.stop()

# --- DIAGNOSTIKA ---
@st.cache_resource
def get_working_model():
    try:
        # Tento príkaz zistí, čo váš kľúč skutočne dokáže
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_actions]
        if available:
            # Skúsime nájsť 1.5 flash, ak nie, vezmeme čokoľvek prvé
            for name in ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]:
                if name in available: return name
            return available[0]
        return None
    except:
        return None

working_model = get_working_model()

if not working_model:
    st.error("❌ Váš kľúč nevidí ŽIADNE modely.")
    st.warning("Choďte do [Google Cloud Console](https://console.cloud.google.com/), vyberte váš projekt a v 'APIs & Services' povoľte 'Generative Language API'.")
    st.stop()

# --- ROZHRANIE ---
st.success(f"✅ Pripojené k modelu: {working_model}")

vstup = st.text_area("Zadanie pre email:", height=150)
col1, col2 = st.columns(2)
with col1:
    ton = st.selectbox("Tón:", ["Profesionálny", "Priateľský", "Eskalačný", "Stručný"])
with col2:
    jazyk = st.selectbox("Jazyk:", ["Slovenčina", "Angličtina", "Nemčina"])

if st.button("🚀 Vygenerovať email"):
    if not vstup:
        st.warning("Napíšte zadanie.")
    else:
        try:
            model = genai.GenerativeModel(working_model)
            res = model.generate_content(f"Si biznis expert v Hydrotech. Napíš {ton} email v jazyku {jazyk}: {vstup}")
            st.markdown("### Výsledok:")
            st.code(res.text)
        except Exception as e:
            st.error(f"Chyba: {e}")
