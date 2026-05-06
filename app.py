import streamlit as st
import google.generativeai as genai
import time

# ------------------ STRÁNKA ------------------
st.set_page_config(page_title="Hydrotech AI Assistant", page_icon="✉️")
st.title("✉️ Hydrotech AI Assistant")

# ------------------ API KONFIGURÁCIA ------------------
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API kľúč (GEMINI_API_KEY) sa nenašiel v Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ------------------ SESSION STATE (PAMÄŤ) ------------------
if "last_call_time" not in st.session_state:
    st.session_state.last_call_time = 0
if "cached_prompt" not in st.session_state:
    st.session_state.cached_prompt = None
if "cached_response" not in st.session_state:
    st.session_state.cached_response = None

COOLDOWN_SECONDS = 10  # Čas v sekundách medzi generovaniami

# ------------------ POUŽÍVATEĽSKÉ ROZHRANIE ------------------
vstup = st.text_area("Zadanie pre email:", height=150, 
                     placeholder="Napr.: Chcem požiadať o zaslanie projektovej dokumentácie...")

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

# ------------------ LOGIKA GENEROVANIA ------------------
if st.button("🚀 Vygenerovať email"):

    if not vstup:
        st.warning("Prosím, zadajte text zadania.")
        st.stop()

    now = time.time()

    # VYLADENÝ PROMPT (Inštrukcia pre AI, aby nedávala vysvetlivky)
    prompt = f"""
Si expert v spoločnosti Hydrotech. Napíš {ton} email v jazyku {jazyk} na základe zadania nižšie.

STRIKTNÉ PRAVIDLO: 
Vygeneruj VÝHRADNE čistý text emailu (predmet a telo). 
Nepridávaj žiadne úvody, vysvetlivky, zoznamy s bodmi ani záverečné komentáre. 
Výsledok musí začať predmetom bez podpisu.

Zadanie:
{vstup}
"""

    # 1. KONTROLA CACHE
    if prompt == st.session_state.cached_prompt:
        st.info("♻️ Použitá cache (rovnaké zadanie)")
        st.markdown("### ✉️ Výsledok:")
        st.code(st.session_state.cached_response, language="text")
        st.stop()

    # 2. KONTROLA RATE LIMITU
    elapsed = now - st.session_state.last_call_time
    if elapsed < COOLDOWN_SECONDS:
        st.warning(f"⏳ Počkaj ešte {int(COOLDOWN_SECONDS - elapsed)} sekúnd.")
        st.stop()

    try:
        # Používame model, ktorý máš potvrdený ako funkčný
        model = genai.GenerativeModel("models/gemini-2.5-flash")

        with st.spinner("AI generuje čistý email..."):
            response = model.generate_content(prompt)

        # Uloženie do pamäte
        st.session_state.cached_prompt = prompt
        st.session_state.cached_response = response.text
        st.session_state.last_call_time = now

        st.success("Email úspešne vygenerovaný!")
        st.markdown("### ✉️ Výsledok:")
        st.code(response.text, language="text")

    except Exception as e:
        st.error(f"Vyskytla sa chyba: {e}")

st.divider()
st.caption("© 2026 Hydrotech, a.s. | Model: Gemini 2.5 Flash")
