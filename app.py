import streamlit as st
from openai import OpenAI

# Nastavenie stránky
st.set_page_config(page_title="Hydrotech AI Assistant", page_icon="✉️")

# CSS pre krajší vzhľad
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 1.1rem; }
    .stCode { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_config=True)

st.title("✉️ Hydrotech Email Assistant")

# Načítanie OpenAI kľúča (v Secrets musí byť OPENAI_API_KEY)
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("❌ API kľúč nenájdený. Skontroluj 'Settings -> Secrets' v Streamlite.")
    st.stop()

client = OpenAI(api_key=api_key)

# Vstup od používateľa
vstup = st.text_area("Čo má byť obsahom emailu?", height=200, 
                     placeholder="Napr.: Chcem požiadať investora o zaslanie projektovej dokumentácie k čistiarni odpadových vôd, ktorú sľúbil minulý týždeň.")

col1, col2 = st.columns(2)
with col1:
    ton = st.selectbox("Tón komunikácie:", 
                       ["Profesionálny a formálny", "Priateľský", "Dôrazný (Urgentný)", "Stručný / Technický"])
with col2:
    jazyk = st.selectbox("Jazyk emailu:", ["Slovenčina", "Angličtina", "Nemčina"])

if st.button("🚀 Vygenerovať email"):
    if not vstup:
        st.warning("Prosím, zadajte zadanie pre email.")
    else:
        try:
            with st.spinner('ChatGPT pripravuje návrh...'):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Najlepší pomer cena/výkon
                    messages=[
                        {"role": "system", "content": f"Si skúsený biznis asistent v spoločnosti Hydrotech, ktorá sa zaoberá čistením odpadových vôd. Tvojou úlohou je písať jasné, gramaticky správne a profesionálne emaily v jazyku: {jazyk}. Tón emailu musí byť: {ton}."},
                        {"role": "user", "content": f"Napíš email na základe tohto zadania: {vstup}"}
                    ],
                    temperature=0.7 # Kreativita vs. presnosť
                )
            
            email_text = response.choices[0].message.content
            
            st.success("Email bol úspešne vygenerovaný!")
            st.markdown("---")
            st.subheader("Návrh emailu:")
            st.write(email_text)
            
            # Tlačidlo na skopírovanie (zobrazí kódový blok)
            st.info("Nižšie môžete text pohodlne skopírovať:")
            st.code(email_text, language="text")
            
        except Exception as e:
            if "insufficient_quota" in str(e):
                st.error("❌ Chyba: Nemáte dobitý kredit na OpenAI!")
                st.info("Prejdite do 'Settings -> Billing' na platform.openai.com a pridajte aspoň 5$.")
            else:
                st.error(f"Vyskytla sa neočakávaná chyba: {e}")

st.divider()
st.caption("© 2026 Hydrotech, a.s. | Powered by OpenAI GPT-4o-mini")
