import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Hydrotech AI", page_icon="✉️")
st.title("✉️ Hydrotech Email Assistant")

# BEZPEČNÉ NAČÍTANIE (Aplikácia nespadne)
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API kľúč sa nenašiel v nastaveniach (Secrets).")
    st.info("Choďte do 'Settings' -> 'Secrets' a pridajte: GEMINI_API_KEY = 'váš_kľúč'")
    st.stop()

# Konfigurácia API
genai.configure(api_key=api_key)

# ROZHRANIE
vstup = st.text_area("Zadanie pre email:", height=150)
col1, col2 = st.columns(2)
with col1:
    ton = st.selectbox("Tón:", ["Profesionálny", "Priateľský", "Eskalačný"])
with col2:
    jazyk = st.selectbox("Jazyk:", ["Slovenčina", "Angličtina", "Nemčina"])

if st.button("🚀 Vygenerovať email"):
    if not vstup:
        st.warning("Napíšte zadanie.")
    else:
        try:
            # Skúšame najuniverzálnejšiu cestu k modelu
            model = genai.GenerativeModel('gemini-1.5-flash')
            with st.spinner('AI pracuje...'):
                res = model.generate_content(f"Ako expert v Hydrotech napíš {ton} email v jazyku {jazyk}: {vstup}")
            st.success("Hotovo!")
            st.code(res.text)
        except Exception as e:
            st.error(f"Chyba pri generovaní: {e}")
