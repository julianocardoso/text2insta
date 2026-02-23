import streamlit as st
import json
from openai import OpenAI

st.set_page_config(page_title="Text2Insta", page_icon="✨", layout="wide")

st.title("✨ Text2Insta - Posts Instagram + Resumo")
st.caption("Feito pelo melhor do mundo • Grok-4 • 100% funcionando")

if "uses" not in st.session_state:
    st.session_state.uses = 0

email = st.text_input("📧 Seu email", placeholder="seu@email.com")

if email:
    if st.session_state.uses >= 3 and not st.session_state.get("is_pro", False):
        st.error("3 usos grátis usados nesta sessão. Volte amanhã ou faça Pro.")
        st.stop()

texto = st.text_area("Cole seu texto longo aqui", height=250)

nicho = st.selectbox("Nicho", ["Negócios", "Fitness", "Viagem", "Estilo de Vida", "Tech", "Motivação"])
tom = st.selectbox("Tom", ["Viral e divertido", "Profissional elegante", "Motivacional forte", "Luxuoso", "Casual autêntico"])

if st.button("🚀 GERAR 3 POSTS + RESUMO", type="primary", use_container_width=True):
    if len(texto) < 100:
        st.error("Texto muito curto!")
    else:
        with st.spinner("Grok-4 criando magia viral..."):
            try:
                client = OpenAI(
                    api_key=st.secrets["xai"]["key"],
                    base_url="https://api.x.ai/v1"
                )
                
                response = client.chat.completions.create(
                    model="grok-4",
                    messages=[{
                        "role": "user",
                        "content": f"""Crie exatamente 3 posts Instagram virais + 1 resumo profissional a partir deste texto:
Texto: {texto}
Nicho: {nicho}
Tom: {tom}

Responda APENAS com JSON válido:
{{"resumo": "...", "posts": [{{"caption": "..."}}, ...]}}"""
                    }],
                    temperature=0.85,
                    max_tokens=1200,
                    response_format={"type": "json_object"}
                )
                
                resultado = json.loads(response.choices[0].message.content)
                
                st.subheader("📝 Resumo Profissional")
                st.markdown(f"**{resultado['resumo']}**")
                
                st.subheader("🔥 Seus 3 Posts Prontos")
                for i, post in enumerate(resultado["posts"], 1):
                    st.markdown(f'<div style="background:#111; padding:20px; border-radius:15px; border-left:5px solid #00ff9d;">{post["caption"]}</div>', unsafe_allow_html=True)
                    if st.button(f"📋 Copiar Post #{i}", key=f"copy{i}"):
                        st.code(post["caption"])
                        st.success("Copiado!")
                
                st.session_state.uses += 1
                st.balloons()
                
            except Exception as e:
                st.error(f"Erro: {str(e)}")
                st.info("Verifique se a chave está correta no Secrets ou se tem créditos no console.x.ai")
