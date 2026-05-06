import streamlit as st
import google.generativeai as genai

# --- BEZPEČNÉ NAČÍTANIE ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Chyba: Kľúč v Secrets nie je správne nastavený.")
    st.stop()

st.set_page_config(page_title="Hydrotech AI", page_icon="✉️")
st.title("✉️ Hydrotech Email Assistant")

# --- DYNAMICKÉ ZÍSKANIE MODELU (Riešenie pre 404) ---
@st.cache_resource
def find_working_model():
    try:
        # Získame zoznam všetkých modelov dostupných pre váš kľúč
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_actions]
        # Uprednostníme verziu flash, ak existuje, inak vezmeme prvý v zozname
        flash_variants = [m for m in available_models if "flash" in m]
        return flash_variants[0] if flash_variants else available_models[0]
    except Exception as e:
        # Ak by zlyhal aj zoznam, skúsime túto verziu (najbežnejšia pre 2026)
        return "models/gemini-1.5-flash-001"

selected_model = find_working_model()

# --- ROZHRANIE ---
vstup = st.text_area("Čo má byť v emaile?", height=150)
col1, col2 = st.columns(2)
with col1:
    ton = st.selectbox("Tón:", ["Profesionálny", "Priateľský", "Eskalačný", "Technický"])
with col2:
    jazyk = st.selectbox("Jazyk:", ["Slovenčina", "Angličtina", "Nemčina"])

if st.button("🚀 Vygenerovať email"):
    if not vstup:
        st.warning("Zadajte text.")
    else:
        try:
            model = genai.GenerativeModel(selected_model)
            prompt = f"Si expert v Hydrotech. Napíš {ton} email v jazyku {jazyk}: {vstup}"
            
            with st.spinner(f'AI pracuje (používam: {selected_model})...'):
                response = model.generate_content(prompt)
                
            st.success("Hotovo!")
            st.code(response.text)
        except Exception as e:
            st.error(f"Chyba: {e}")
            st.info("Ak vidíte chybu 403 alebo 429, počkajte minútu alebo skúste nový API kľúč.")

st.divider()
st.caption(f"Aktuálne pripojený model: {selected_model}")
