import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Hydrotech Gemini", page_icon="💎")
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
        # SKÚŠAME POSTUPNE VŠETKY MOŽNÉ NÁZVY (riešenie pre 404)
        uspech = False
        for model_name in ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-pro"]:
            if uspech: break
            try:
                model = genai.GenerativeModel(model_name)
                with st.spinner(f'Skúšam model {model_name}...'):
                    res = model.generate_content(f"Si asistent v Hydrotech. Napíš {ton} email v jazyku {jazyk}: {vstup}")
                st.success(f"Úspech s modelom {model_name}!")
                st.code(res.text)
                uspech = True
            except Exception as e:
                # Ak vráti 404, skúša ďalší model v poradí
                continue
        
        if not uspech:
            st.error("❌ Žiadny z modelov Gemini nereaguje (404).")
            st.info("💡 Odporúčanie: Prepnite aplikáciu na ChatGPT kód, ktorý vám fungoval, pretože Google vo vašom regióne blokuje bezplatné Gemini API.")
