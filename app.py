import streamlit as st
import google.generativeai as genai

# 1. Načítanie kľúča (image_91af7e.png)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Chyba: API kľúč nie je v Secrets správne uložený.")
    st.stop()

st.set_page_config(page_title="Hydrotech AI Assistant", page_icon="✉️")
st.title("✉️ Hydrotech Email Assistant")

# 2. Rozhranie (vrátený tón a jazyk)
vstup = st.text_area("Čo má byť v emaile?", height=150)

col1, col2 = st.columns(2)
with col1:
    ton = st.selectbox("Tón komunikácie:", ["Profesionálny", "Priateľský", "Eskalačný", "Stručný"])
with col2:
    jazyk = st.selectbox("Jazyk:", ["Slovenčina", "Angličtina", "Nemčina"])

if st.button("🚀 Vygenerovať email"):
    if not vstup:
        st.warning("Najprv napíšte zadanie.")
    else:
        # Skúsime tri najbežnejšie názvy modelu za sebou, kým jeden neprejde
        uspech = False
        for model_name in ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-pro"]:
            if uspech: break
            try:
                model = genai.GenerativeModel(model_name)
                prompt = f"Si asistent v Hydrotech. Napíš {ton} email v jazyku {jazyk}: {vstup}"
                
                with st.spinner(f'Skúšam model {model_name}...'):
                    res = model.generate_content(prompt)
                    st.success(f"Email vygenerovaný (cez {model_name})")
                    st.code(res.text)
                    st.balloons()
                    uspech = True
            except Exception as e:
                # Ak tento model hodí 404, ideme na ďalší v zozname
                continue
        
        if not uspech:
            st.error("Žiadny z dostupných modelov nefunguje. Skontrolujte, či váš API kľúč nie je zablokovaný v Google AI Studio.")

st.divider()
st.caption("© 2026 Hydrotech, a.s.")
