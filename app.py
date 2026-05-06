import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

st.set_page_config(page_title="Hydrotech Fix", page_icon="✉️")
st.title("✉️ Hydrotech Email Assistant")

# Načítanie kľúča
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Chýba kľúč v Secrets!")
    st.stop()

genai.configure(api_key=api_key)

vstup = st.text_area("Zadanie:")

if st.button("🚀 Generovať"):
    # Skúsime tieto 3 konkrétne cesty, ktoré fungujú v EÚ
    test_models = ["gemini-1.5-flash", "gemini-1.5-pro", "models/gemini-1.0-pro"]
    
    found_success = False
    
    for m_name in test_models:
        try:
            model = genai.GenerativeModel(model_name=m_name)
            # Skúšobný krátky prompt
            response = model.generate_content(f"Napiš krátky profesionálny email: {vstup}")
            
            st.success(f"✅ ÚSPECH! Model '{m_name}' funguje.")
            st.code(response.text)
            found_success = True
            break # Ak jeden funguje, končíme
            
        except exceptions.NotFound:
            st.warning(f"❌ Model '{m_name}' nebol nájdený (404).")
        except exceptions.PermissionDenied:
            st.error(f"🚫 Model '{m_name}': Prístup zamietnutý (403). Váš kľúč nemá povolenie.")
        except exceptions.ResourceExhausted:
            st.error(f"⏳ Model '{m_name}': Prekročený limit (429). Počkajte minútu.")
        except Exception as e:
            st.error(f"⚠️ Model '{m_name}' zlyhal: {str(e)}")

    if not found_success:
        st.error("Žiadny model neuspel. Pravdepodobne máte v Google AI Studio nastavený kľúč v projekte, ktorý nemá povolené Generative AI API.")
        st.info("TIP: Skúste v Google AI Studio vytvoriť kľúč cez 'Create API key in NEW project' pod súkromným @gmail.com účtom.")
