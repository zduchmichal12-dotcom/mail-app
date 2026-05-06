import streamlit as st
import google.generativeai as genai
import time

# ------------------ STRÁNKA ------------------
st.set_page_config(page_title="Hydrotech AI Assistant", page_icon="✉️")
st.title("✉️ Hydrotech AI Assistant")

# ------------------ API ------------------
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API kľúč sa nenašiel v Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ------------------ SESSION STATE ------------------
st.session_state.setdefault("last_call_time", 0)
st.session_state.setdefault("cached_prompt", None)
st.session_state.setdefault("cached_response", None)

COOLDOWN_SECONDS = 20

# ------------------ UI ------------------
vstup = st.text_area("Zadanie pre email:", height=150)

col1, col2 = st.columns(2)

with col1:
    ton = st.selectbox(
        "Tón komunikácie:",
        ["Profesionálny", "Priateľský", "Dôrazný / Eskalačný", "Stručný"]
    )

with col2:
    jazyk = st.selectbox(
        "Jazyk:",
        ["Slovenčina", "Angličtina", "Nemčina"]
    )

# ------------------ GENEROVANIE ------------------
if st.button("🚀 Vygenerovať email"):

    if not vstup:
        st.warning("Zadaj text.")
        st.stop()

    now = time.time()

    prompt = f"""
Napíš {ton} email v jazyku {jazyk}.

Zadanie:
{vstup}
"""

    # ------------------ CACHE (ZÁCHRANA API) ------------------
    if prompt == st.session_state.cached_prompt:
        st.info("♻️ Použitá cache (bez API volania)")
        st.markdown("### ✉️ Výsledok:")
        st.code(st.session_state.cached_response)
        st.stop()

    # ------------------ RATE LIMIT ------------------
    if now - st.session_state.last_call_time < COOLDOWN_SECONDS:
        st.warning("⏳ Počkaj pár sekúnd pred ďalším generovaním.")
        st.stop()

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        with st.spinner("Generujem email..."):
            response = model.generate_content(prompt)

        # uloženie cache
        st.session_state.cached_prompt = prompt
        st.session_state.cached_response = response.text
        st.session_state.last_call_time = now

        st.success("Hotovo!")
        st.markdown("### ✉️ Výsledok:")
        st.code(response.text)

    except Exception as e:
        if "429" in str(e):
            st.error("⏳ API limit (počkaj chvíľu).")
        else:
            st.error(f"Chyba: {e}")
