import streamlit as st
import google.generativeai as genai
import time

# ------------------ STRÁNKA ------------------
st.set_page_config(page_title="Hydrotech AI Assistant", page_icon="✉️")
st.title("✉️ Hydrotech Email Assistant")

# ------------------ API KĽÚČ ------------------
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API kľúč sa nenašiel v nastaveniach (Secrets).")
    st.stop()

genai.configure(api_key=api_key)

# ------------------ SESSION STATE SAFE INIT ------------------
st.session_state.setdefault("last_call_time", 0)

# ------------------ UI ------------------
vstup = st.text_area(
    "Zadanie pre email:",
    height=150,
    placeholder="Napr.: Potrebujem súrne dokumentáciu od investora..."
)

col1, col2 = st.columns(2)

with col1:
    ton = st.selectbox(
        "Tón komunikácie:",
        ["Profesionálny", "Priateľský", "Dôrazný / Eskalačný", "Stručný"]
    )

with col2:
    jazyk = st.selectbox(
        "Cieľový jazyk:",
        ["Slovenčina", "Angličtina", "Nemčina"]
    )

# ------------------ RATE LIMIT ------------------
COOLDOWN_SECONDS = 15

# ------------------ GENEROVANIE ------------------
if st.button("🚀 Vygenerovať email"):

    now = time.time()

    # ochrana proti 429
    if now - st.session_state.last_call_time < COOLDOWN_SECONDS:
        st.warning("⏳ Počkajte pár sekúnd pred ďalším generovaním (API limit ochrana).")
        st.stop()

    if not vstup:
        st.warning("Najprv napíšte zadanie pre email.")
        st.stop()

    try:
        # ------------------ MODEL ------------------
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
Si expert na biznis komunikáciu v spoločnosti Hydrotech.
Napíš {ton} email v jazyku {jazyk} na základe tohto zadania:

{vstup}
"""

        with st.spinner("AI pripravuje váš email..."):
            response = model.generate_content(prompt)

        # uloženie času volania
        st.session_state.last_call_time = now

        st.success("Hotovo! Email bol úspešne vygenerovaný.")
        st.markdown("### ✉️ Výsledok:")
        st.code(response.text, language="text")

    except Exception as e:
        if "429" in str(e):
            st.error("⏳ Preťaženie API (limit). Skús o chvíľu znova.")
        else:
            st.error(f"Vyskytla sa chyba: {e}")
