import streamlit as st
import google.generativeai as genai

# Bezpečné načítanie kľúča zo Streamlit Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Chýba API kľúč v nastaveniach (Secrets).")
    st.stop()

st.set_page_config(page_title="Hydrotech AI Assistant", page_icon="✉️")
st.title("✉️ Hydrotech Email Assistant")

vstup = st.text_area("Zadanie pre email:", placeholder="Píšeme investorovi o dokumente...")

if st.button("🚀 Generovať email"):
    if not vstup:
        st.warning("Zadaj podklady.")
    else:
        try:
            # Použijeme najstabilnejší model pre rok 2026
            model = genai.GenerativeModel('gemini-1.5-flash')
            with st.spinner('AI pracuje...'):
                res = model.generate_content(f"Napíš profesionálny biznis email: {vstup}")
            st.success("Hotovo!")
            st.code(res.text)
        except Exception as e:
            st.error(f"Chyba: {e}")
