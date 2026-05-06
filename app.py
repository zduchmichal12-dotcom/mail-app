import streamlit as st
import google.generativeai as genai

# Nastavenie vzhľadu stránky
st.set_page_config(page_title="AI Email Assistant", page_icon="✉️")
st.title("✉️ Gemini Email Assistant")
st.markdown("Nástroj na automatické písanie a preklad mailov.")

# Bočný panel pre nastavenia
with st.sidebar:
    st.header("Nastavenia")
    api_key = st.text_input("Vlož Gemini API Key:", type="password")
    model_choice = st.selectbox("Model:", ["gemini-1.5-flash", "gemini-1.5-pro"])
    st.info("Flash je rýchlejší, Pro je inteligentnejší.")

# Hlavné rozhranie
vstupny_text = st.text_area("Vlož zadanie pre mail (napr. fakty v slovenčine):", height=150)

col1, col2 = st.columns(2)
with col1:
    ton = st.selectbox("Tón komunikácie:", 
                       ["Priateľský a neformálny", 
                        "Profesionálny a obchodný", 
                        "Dôrazný / Eskalačný", 
                        "Stručný a jasný"])
with col2:
    jazyk = st.selectbox("Cieľový jazyk:", ["Angličtina", "Nemčina", "Slovenčina", "Čeština"])

if st.button("🚀 Vygenerovať email"):
    if not api_key:
        st.error("Prosím, zadaj API kľúč v bočnom paneli.")
    elif not vstupny_text:
        st.warning("Napíš aspoň pár slov o tom, čo má v maily byť.")
    else:
        try:
            # Konfigurácia Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_choice)
            
            # Definícia promptu
            prompt = f"""
            Si profesionálny asistent pre biznis komunikáciu. 
            Tvojou úlohou je napísať email na základe týchto údajov:
            
            Obsah: {vstupny_text}
            Tón: {ton}
            Jazyk: {jazyk}
            
            Pravidlá:
            1. Ak je jazyk Angličtina, použi prirodzené biznis frázy.
            2. Ak je tón eskalačný, buď priamy ale zachovaj dekórum.
            3. Výstup musí obsahovať Predmet (Subject) a samotné telo mailu.
            """
            
            with st.spinner('Generujem...'):
                response = model.generate_content(prompt)
                
            st.success("Hotovo!")
            st.markdown("---")
            st.subheader("Navrhovaný email:")
            st.write(response.text)
            
            # Tlačidlo na skopírovanie (Streamlit to má v st.code automaticky)
            st.code(response.text, language="text")
            
        except Exception as e:
            st.error(f"Vyskytla sa chyba: {e}")