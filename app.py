import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Hydrotech AI (GPT)", page_icon="✉️")
st.title("✉️ Hydrotech Email Assistant (GPT)")

# Načítanie OpenAI kľúča zo Secrets
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("❌ Chýba OPENAI_API_KEY v Secrets!")
    st.stop()

client = OpenAI(api_key=api_key)

vstup = st.text_area("Zadanie pre email:", height=150)
col1, col2 = st.columns(2)
with col1:
    ton = st.selectbox("Tón:", ["Profesionálny", "Priateľský", "Dôrazný"])
with col2:
    # Tu môžeme pridať aj GPT-4o, ak máte zaplatený kredit
    model_gpt = st.selectbox("Model:", ["gpt-4o-mini", "gpt-4o"])

if st.button("🚀 Vygenerovať email"):
    if not vstup:
        st.warning("Zadajte text.")
    else:
        try:
            with st.spinner('ChatGPT rozmýšľa...'):
                response = client.chat.completions.create(
                    model=model_gpt,
                    messages=[
                        {"role": "system", "content": f"Si biznis asistent v Hydrotech. Píš v slovenčine, tón: {ton}."},
                        {"role": "user", "content": vstup}
                    ]
                )
            
            st.success("Hotovo!")
            st.write(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"Chyba: {e}")
