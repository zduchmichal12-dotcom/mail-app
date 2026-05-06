import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Hydrotech AI Assistant", page_icon="✉️")
st.title("✉️ Hydrotech Email Assistant")

# --- NAČÍTANIE KĽÚČA ---
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API kľúč sa nenašiel v nastaveniach (Secrets).")
    st.stop()

# Konfigurácia pripojenia
genai.configure(api_key=api_key)

# --- DEBUG: ZOZNAM MODELOV ---
with st.expander("📋 Dostupné Gemini modely (debug)", expanded=False):
    try:
        models = genai.list_models()
        for m in models:
            st.write(m.name)
    except Exception as e:
        st.error(f"❌ Nepodarilo sa načítať modely: {e}")

# --- ROZHRANIE APLIKÁCIE ---
vstup = st.text_area(
    "Zadanie pre email:",
    height=150,
    placeholder="Napr.: Potrebujem súrne dokumentáciu od investora..."
)

col1, col2 = st.columns(2)
with col1:
    ton = st.selectbox(
        "Tón komunikácie:",
        ["Profesionálny", "Priateľský", "Dôrazný / Eskalačný", "Stručný"]
    )
with col2:
    jazyk = st.selectbox(
        "Cieľový jazyk:",
        ["Slovenčina", "Angličtina", "Nemčina"]
    )

if st.button("🚀 Vygenerovať email"):
    if not vstup:
        st.warning("Najprv napíšte zadanie pre email.")
    else:
        try:
            # ⚠️ sem potom dáme správny model podľa výpisu
            model = genai.GenerativeModel("gemini-1.5-pro")

            prompt = f"Si expert na biznis komunikáciu v spoločnosti Hydrotech. Napíš {ton} email v jazyku {jazyk} na základe tohto zadania: {vstup}"

            with st.spinner('AI pripravuje váš email...'):
                response = model.generate_content(prompt)

            st.success("Hotovo! Email bol úspešne vygenerovaný.")
            st.markdown("### Výsledok:")
            st.code(response.text, language="text")

        except Exception as e:
            st.error(f"Vyskytla sa chyba: {e}")
