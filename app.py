import streamlit as st
import google.generativeai as genai

# --- BEZPEČNÁ KONFIGURÁCIA ---
try:
    # Streamlit si vytiahne kľúč z okna, ktoré ste videli na image_91bb79.png
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Chýba API kľúč v Secrets! Nastavte ho podľa image_91bb79.png.")
    st.stop()

# Nastavenie vzhľadu stránky
st.set_page_config(page_title="Hydrotech AI Assistant", page_icon="✉️")

st.title("✉️ Hydrotech Email Assistant")
st.markdown("---")

# --- HLAVNÉ ROZHRANIE ---
vstupny_text = st.text_area(
    "Čo má byť v emaile? (zadajte fakty alebo body):",
    placeholder="Napr.: Píšeme investorovi, že dokument o struvite nemáme, ale preverujeme liehovar v Leopoldove...",
    height=150
)

# Výber tónu a jazyka vedľa seba
col1, col2 = st.columns(2)

with col1:
    ton = st.selectbox("Tón komunikácie:", [
        "Profesionálny a obchodný", 
        "Priateľský a neformálny", 
        "Dôrazný / Eskalačný", 
        "Stručný a technický"
    ])

with col2:
    jazyk = st.selectbox("Cieľový jazyk:", [
        "Slovenčina",
        "Angličtina", 
        "Nemčina", 
        "Poľština"
    ])

# --- LOGIKA GENEROVANIA ---
if st.button("🚀 Vygenerovať email"):
    if not vstupny_text:
        st.warning("Najprv napíšte zadanie pre email.")
    else:
        try:
            # Používame stabilný model gemini-1.5-flash
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Detailný pokyn pre AI (Prompt)
            prompt = f"""
            Si expert na biznis komunikáciu v spoločnosti Hydrotech. 
            Tvojou úlohou je napísať email na základe týchto podkladov: {vstupny_text}
            Požadovaný tón: {ton}
            Cieľový jazyk: {jazyk}
            
            Email musí obsahovať Predmet (Subject), profesionálne oslovenie a štruktúrované telo.
            """
            
            with st.spinner('AI pripravuje váš email...'):
                response = model.generate_content(prompt)
                
            st.success("Email bol úspešne vytvorený!")
            st.markdown("### Výsledok:")
            st.code(response.text, language="text")
            st.balloons()
            
        except Exception as e:
            # Ak by Google opäť hlásil chybu 429 (limit), vypíšeme to zrozumiteľne
            if "429" in str(e):
                st.error("Prekročený limit bezplatnej verzie. Počkajte prosím 60 sekúnd.")
            else:
                st.error(f"Vyskytla sa chyba: {e}")

st.markdown("---")
st.caption("© 2026 Hydrotech, a.s. | Powered by Google Gemini 1.5")
