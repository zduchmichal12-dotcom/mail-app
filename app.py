import streamlit as st
import google.generativeai as genai

# --- KONFIGURÁCIA CEZ SECRETS ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Nastavte GEMINI_API_KEY v Secrets!")
    st.stop()

st.set_page_config(page_title="Hydrotech AI", page_icon="✉️")
st.title("✉️ Hydrotech Email Assistant")

# --- DYNAMICKÉ ZÍSKANIE MODELU (Riešenie pre 404) ---
@st.cache_resource
def get_available_model():
    try:
        # Získame zoznam všetkých modelov, ktoré podporujú generovanie obsahu
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_actions]
        # Vyberieme ten, ktorý vyzerá ako flash (rýchly), inak prvý v poradí
        flash_models = [m for m in models if 'flash' in m]
        return flash_models[0] if flash_models else models[0]
    except:
        return "models/gemini-1.5-flash" # Posledná záchrana

working_model_name = get_available_model()

# --- ROZHRANIE ---
vstupny_text = st.text_area("Čo má byť v emaile?", height=150)

col1, col2 = st.columns(2)
with col1:
    ton = st.selectbox("Tón:", ["Profesionálny", "Priateľský", "Eskalačný", "Technický"])
with col2:
    jazyk = st.selectbox("Jazyk:", ["Slovenčina", "Angličtina", "Nemčina"])

if st.button("🚀 Vygenerovať email"):
    if not vstupny_text:
        st.warning("Zadajte text.")
    else:
        try:
            # Použijeme model, ktorý sme našli ako funkčný
            model = genai.GenerativeModel(working_model_name)
            
            prompt = f"Si biznis asistent v Hydrotech. Napíš {ton} email v jazyku {jazyk}: {vstupny_text}"
            
            with st.spinner(f'AI pracuje (model: {working_model_name})...'):
                response = model.generate_content(prompt)
                
            st.success("Email vygenerovaný!")
            st.code(response.text, language="text")
            
        except Exception as e:
            st.error(f"Chyba: {e}")
            st.info("Skúste v AI Studio vytvoriť úplne nový API kľúč.")

st.caption(f"Aktuálne pripojený model: {working_model_name}")
