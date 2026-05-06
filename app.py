import time

# --- RATE LIMIT OCHRANA ---
if "last_call_time" not in st.session_state:
    st.session_state.last_call_time = 0

COOLDOWN_SECONDS = 15  # ochrana proti 429

if st.button("🚀 Vygenerovať email"):

    # kontrola limitu kliknutí
    now = time.time()
    if now - st.session_state.last_call_time < COOLDOWN_SECONDS:
        st.warning("⏳ Prosím počkaj pár sekúnd pred ďalším generovaním (API limit ochrana).")
        st.stop()

    if not vstup:
        st.warning("Najprv napíšte zadanie pre email.")
        st.stop()

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"Si expert na biznis komunikáciu v spoločnosti Hydrotech. Napíš {ton} email v jazyku {jazyk} na základe tohto zadania: {vstup}"

        with st.spinner('AI pripravuje váš email...'):
            response = model.generate_content(prompt)

        # uložiť čas posledného volania
        st.session_state.last_call_time = now

        st.success("Hotovo! Email bol úspešne vygenerovaný.")
        st.markdown("### Výsledok:")
        st.code(response.text, language="text")

    except Exception as e:
        if "429" in str(e):
            st.error("⏳ Preťaženie API (limit). Skús o pár sekúnd znova.")
        else:
            st.error(f"Vyskytla sa chyba: {e}")
