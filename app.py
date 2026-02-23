import streamlit as st
import random

st.set_page_config(page_title="Text2Insta", page_icon="✨", layout="wide")

st.markdown("""
<style>
    .main {background: #0a0a0f; color: #e0e0ff;}
    .stButton>button {background: linear-gradient(90deg, #00ff9d, #00b8ff); color:#000; font-weight:700; border-radius:9999px; padding:16px 40px; font-size:1.2rem;}
    .post {background:#111118; border-left:8px solid #00ff9d; padding:24px; border-radius:20px; margin:15px 0;}
</style>
""", unsafe_allow_html=True)

st.title("✨ Text2Insta - Posts Instagram + Resumo")
st.caption("DEMO • Feito pelo melhor do mundo • Versão de teste grátis")

if "uses" not in st.session_state:
    st.session_state.uses = 0

email = st.text_input("📧 Seu email (pra simular limite grátis)", placeholder="seu@email.com")

texto = st.text_area("Cole seu texto longo aqui", height=250)

nicho = st.selectbox("Nicho", ["Negócios", "Fitness", "Viagem", "Estilo de Vida", "Tech", "Motivação"])
tom = st.selectbox("Tom", ["Viral e divertido", "Profissional elegante", "Motivacional forte", "Luxuoso", "Casual autêntico"])

if st.button("🚀 GERAR 3 POSTS + RESUMO", type="primary", use_container_width=True):
    if len(texto) < 50:
        st.error("Texto muito curto!")
    elif st.session_state.uses >= 3:
        st.error("3 usos grátis usados nesta sessão. Recarregue a página.")
    else:
        with st.spinner("Gerando magia viral..."):
            # Templates realistas feitos pelo melhor do mundo
            resumos = {
                "Negócios": "Este texto mostra como transformar uma ideia simples em um negócio que fatura enquanto você dorme.",
                "Fitness": "A chave não é a perfeição, é a consistência diária que transforma o corpo e a mente.",
                "Viagem": "Viajar não é luxo, é investimento na sua história de vida.",
                "Motivação": "O maior arrependimento é nunca ter tentado.",
            }
            
            posts = [
                f"🚀 {texto[:80]}... Isso mudou TUDO pra mim! Quem mais tá pronto pra dar o próximo passo? Comenta 'EU VOU' 👇\n\n#{nicho.replace(' ', '')} #Mindset",
                f"😂 {texto[:60]}... E aí, qual foi a sua maior lição esse ano? Me conta nos comentários!\n\n#{nicho.replace(' ', '')} #Viral",
                f"💎 {texto[:70]}... O segredo que ninguém te conta. Salva esse post e compartilha com quem precisa ouvir isso hoje!\n\n#{nicho.replace(' ', '')} #Sucesso"
            ]
            
            st.subheader("📝 Resumo Profissional")
            st.markdown(f"**{resumos.get(nicho, 'Texto transformado em conteúdo de alto engajamento.')}**")
            
            st.subheader("🔥 Seus 3 Posts Prontos")
            for i, post in enumerate(posts, 1):
                st.markdown(f'<div class="post"><strong>Post #{i}</strong><br>{post}</div>', unsafe_allow_html=True)
                if st.button(f"📋 Copiar Post #{i}", key=i):
                    st.code(post)
                    st.success("✅ Copiado! Cole direto no Instagram")
            
            st.session_state.uses += 1
            st.balloons()
            st.success("✅ Demo funcionando! Agora imagine isso com IA real...")
