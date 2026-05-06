import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Hydrotech AI Assistant", page_icon="✉️")
st.title("✉️ Hydrotech Email Assistant")

# Načítanie kľúča
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("❌ API kľúč chýba v Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ROZHRANIE
vstup = st.text_area("Zadanie pre email:", height=150, placeholder="Napr.: Chcem dokumentáciu od investora...")
col1, col2 = st.columns(2)
with col1:
    ton = st.selectbox("Tón:", ["Profesionálny", "Priateľský", "Dôrazný"])
with col2:
    jazyk = st.selectbox("Jazyk:", ["Slovenčina", "Angličtina", "Nemčina"])

if st.button("🚀 Vygenerovať email"):
    if not vstup:
        st.warning("Najprv napíšte zadanie.")
    else:
        # ZOZNAM MODELOV NA TESTOVANIE (riešenie pre 404)
        mozne_modely = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
        uspech = False
        
        for model_name in mozne_modely:
            if uspech: break
            try:
                model = genai.GenerativeModel(model_name)
                with st.spinner(f'Skúšam generovať cez {model_name}...'):
                    res = model.generate_content(f"Si expert v Hydrotech. Napíš {ton} email v jazyku {jazyk}: {vstup}")
                    
                st.success(f"Email vygenerovaný úspešne!")
                st.markdown("### Výsledok:")
                st.code(res.text)
                uspech = True
            except Exception as e:
                # Ak model neexistuje (404), skúsi ďalší v poradí
                if "404" in str(e):
                    continue
                else:
                    st.error(f"Iná chyba: {e}")
                    break
        
        if not uspech:
            st.error("❌ Žiadny z modelov nefunguje. Skúste v Google AI Studio vytvoriť úplne nový API kľúč.")
