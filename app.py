import streamlit as st
import json
import requests

st.set_page_config(page_title="Text2Insta", page_icon="✨", layout="wide")

st.markdown("""
<style>
    .main {background: #0a0a0f; color: #e0e0ff;}
    .stButton>button {background: linear-gradient(90deg, #00ff9d, #00b8ff); color:#000; font-weight:700; border-radius:9999px; padding:16px 40px; font-size:1.2rem;}
    .post {background:#111118; border-left:8px solid #00ff9d; padding:24px; border-radius:20px; margin:15px 0;}
</style>
""", unsafe_allow_html=True)

st.title("✨ Text2Insta - Posts Instagram + Resumo")
st.caption("Feito pelo melhor do mundo • Agora com Hugging Face grátis e supremo")

# === LIMITE GRÁTIS POR SESSÃO ===
if "uses" not in st.session_state:
    st.session_state.uses = 0

email = st.text_input("📧 Seu email (pra controlar os 3 usos grátis)", placeholder="seu@email.com")

if email:
    if st.session_state.uses >= 3:
        st.error("Seus 3 usos grátis acabaram nesta sessão. Recarregue ou volte amanhã!")
        st.stop()
    else:
        st.success(f"✅ Você tem **{3 - st.session_state.uses} usos grátis** restantes")

texto = st.text_area("Cole seu texto longo aqui (blog, ideia, roteiro...)", height=300)

nicho = st.selectbox("Nicho", ["Negócios", "Fitness", "Viagem", "Estilo de Vida", "Tech", "Motivação"])
tom = st.selectbox("Tom do post", ["Viral e divertido", "Profissional elegante", "Motivacional forte", "Luxuoso", "Casual autêntico"])

if st.button("🚀 GERAR 3 POSTS + RESUMO", type="primary", use_container_width=True):
    if len(texto) < 100:
        st.error("Texto muito curto!")
    else:
        with st.spinner("Hugging Face criando magia viral... (5-10 segundos)"):
            api_key = st.secrets["huggingface"]["key"]
            headers = {"Authorization": f"Bearer {api_key}"}
            API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
            payload = {
                "inputs": f"""Você é o melhor copywriter de Instagram do mundo. Responda APENAS com JSON válido:
{{
  "resumo": "Resumo profissional em 2-3 frases",
  "posts": [
    {{"caption": "Caption completa com emojis, CTA forte e hashtags virais"}},
    {{"caption": "..."}},
    {{"caption": "..."}}
  ]
}}
Exatamente 3 posts. Estilo autêntico, otimizado para engajamento máximo.

Texto original: {texto}
Nicho: {nicho}
Tom: {tom}
Gere 3 posts + 1 resumo.""",
                "parameters": {"temperature": 0.85, "max_new_tokens": 1200}
            }
            response = requests.post(API_URL, headers=headers, json=payload)
            result = response.json()
            resultado = json.loads(result[0]["generated_text"].split("Responda APENAS com JSON válido:")[1].strip())
        
        st.subheader("📝 Resumo Profissional")
        st.markdown(f"**{resultado['resumo']}**")
        
        st.subheader("🔥 Seus 3 Posts Prontos")
        for i, post in enumerate(resultado["posts"], 1):
            st.markdown(f'<div class="post"><strong>Post #{i}</strong><br>{post["caption"]}</div>', unsafe_allow_html=True)
            if st.button(f"📋 Copiar Post #{i}", key=f"copy{i}"):
                st.code(post["caption"], language=None)
                st.success("Copiado! Cole direto no Instagram")
        
        st.session_state.uses += 1
        st.balloons()
