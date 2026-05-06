import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Hydrotech Gemini AI", page_icon="💎")
st.title("💎 Hydrotech Email Assistant (Gemini)")

# 1. NAČÍTANIE KĽÚČA
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("❌ GEMINI_API_KEY chýba v Secrets!")
    st.stop()

# 2. KONFIGURÁCIA
genai.configure(api_key=api_key)

# 3. DYNAMICKÁ DETEKCIA MODELOV (Tento blok vyrieši váš problém)
@st.cache_resource
def find_working_model():
    try:
        # Získame zoznam všetkých dostupných modelov pre váš kľúč
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_actions]
        # Prioritné poradie modelov
        preferred = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
        for p in preferred:
            if p in models:
                return p
        return models[0] if models else None
    except Exception as e:
        st.error(f"Chyba pri hľadaní modelov: {e}")
        return None

working_model = find_working_model()

if not working_model:
    st.error("❌ Váš API kľúč nevidí žiadne modely. Skontrolujte povolenie 'Generative Language API' v Google Cloud.")
    st.stop()

st.sidebar.success(f"Aktívny model: {working_model}")

# 4. ROZHRANIE
vstup = st.text_area("Zadanie pre email:", height=150)
col1, col2 = st.columns(2)
with col1:
    ton = st.selectbox("Tón:", ["Profesionálny", "Priateľský", "Dôrazný"])
with col2:
    jazyk = st.selectbox("Jazyk:", ["Slovenčina", "Angličtina", "Nemčina"])

if st.button("🚀 Vygenerovať email"):
    if not vstup:
        st.warning("Zadajte text.")
    else:
        try:
            model = genai.GenerativeModel(working_model)
            with st.spinner('Gemini generuje...'):
                res = model.generate_content(f"Si expert v Hydrotech. Napíš {ton} email v jazyku {jazyk}: {vstup}")
            st.success("Hotovo!")
            st.code(res.text)
        except Exception as e:
            st.error(f"Chyba pri generovaní: {e}")
