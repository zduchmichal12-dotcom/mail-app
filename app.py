import streamlit as st
import google.generativeai as genai

# --- KONFIGURÁCIA ---
API_KEY = "AIzaSyCnBWOiDHzd_9qzzCDX8XpA_7I2fl9jSXo"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Hydrotech AI", page_icon="✉️")
st.title("✉️ Hydrotech Email Assistant")

# ROZHRANIE
vstup = st.text_area("Zadanie pre email:")

if st.button("🚀 Generovať email"):
    if not vstup:
        st.error("Napíš zadanie.")
    else:
        try:
            # Skúsime absolútne najzákladnejší názov bez prefixov
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('Generujem...'):
                res = model.generate_content(f"Napíš profesionálny email: {vstup}")
            
            st.success("Hotovo!")
            st.code(res.text)
            
        except Exception as e:
            st.error(f"Chyba: {e}")
            
            # TENTO BLOK NÁM POVIE PRAVDU, AK TO ZLYHÁ:
            st.write("Hľadám modely, ktoré váš kľúč skutočne vidí...")
            try:
                m_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_actions]
                st.info(f"Skúste do kódu namiesto 'gemini-1.5-flash' napísať jeden z týchto: {m_list}")
            except:
                st.warning("Nepodarilo sa načítať ani zoznam modelov. Skontrolujte, či je API kľúč aktívny.")
