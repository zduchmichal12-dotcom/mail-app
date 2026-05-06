import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Hydrotech Email", page_icon="💎")
st.title("💎 Hydrotech Email Assistant")

# Načítanie kľúča
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Chýba GEMINI_API_KEY v Secrets!")
    st.stop()

genai.configure(api_key=api_key)

# ROZHRANIE
vstup = st.text_area("Čo potrebujete napísať?", height=150)
col1, col2 = st.columns(2)
with col1:
    ton = st.selectbox("Tón:", ["Profesionálny", "Priateľský", "Dôrazný"])
with col2:
    jazyk = st.selectbox("Jazyk:", ["Slovenčina", "Angličtina", "Nemčina"])

if st.button("🚀 Vygenerovať"):
    if not vstup:
        st.warning("Zadajte text.")
    else:
        try:
            # Tu nepoužívame list_models ani supported_actions, len priame volanie
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            with st.spinner('Generujem...'):
                res = model.generate_content(f"Si asistent v Hydrotech. Napíš {ton} email v jazyku {jazyk}: {vstup}")
            
            st.success("Hotovo!")
            st.code(res.text)
        except Exception as e:
            st.error(f"Chyba: {e}")
            st.info("Ak vidíte chybu 404, váš projekt 'mail-assist' v Google Cloud stále nemá plne aktívne API, alebo kľúč nepatrí k tomu projektu.")
