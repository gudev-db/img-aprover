import streamlit as st
from pptx import Presentation
import io
import pdfplumber
import google.generativeai as genai
import os
from PIL import Image

# Configuração inicial
st.set_page_config(layout="wide")
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)
modelo_vision = genai.GenerativeModel("gemini-2.0-flash", generation_config={"temperature": 0.1})
modelo_texto = genai.GenerativeModel("gemini-1.5-flash")

# Carrega diretrizes
with open('data.txt', 'r') as file:
    conteudo = file.read()

# --- Seção 1: Aprovação de Conteúdo ---
st.header("📋 Aprovação de Conteúdo")
tab1, tab2 = st.tabs(["🖼️ Imagens", "✍️ Textos"])

with tab1:
    uploaded_image = st.file_uploader("Envie a imagem para análise (.jpg, .png)", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        st.image(uploaded_image, use_column_width=True)
        if st.button("Analisar Imagem", key="analyze_img"):
            with st.spinner('Validando contra as diretrizes da Holambra...'):
                try:
                    image = Image.open(uploaded_image)
                    img_bytes = io.BytesIO()
                    image.save(img_bytes, format=image.format)
                    
                    resposta = modelo_vision.generate_content([
                        f"""Analise esta imagem considerando rigorosamente:
                        {conteudo}
                        Forneça um parecer técnico com:
                        - ✅ Pontos de conformidade
                        - ❌ Não-conformidades críticas
                        - 🛠 Sugestões de ajustes específicos
                        """,
                        {"mime_type": "image/jpeg", "data": img_bytes.getvalue()}
                    ])
                    st.subheader("Laudo Técnico")
                    st.markdown(resposta.text)
                except Exception as e:
                    st.error(f"Erro na análise: {str(e)}")

with tab2:
    texto_input = st.text_area("Cole o texto para validação:", height=200)
    if st.button("Validar Texto", key="validate_text"):
        with st.spinner('Cross-check com guias da marca...'):
            resposta = modelo_texto.generate_content(
                f"""Revise este texto conforme as diretrizes da Holambra:
                Diretrizes: {conteudo}
                Texto a revisar: {texto_input}
                
                Formato de resposta:
                ### Versão Ajustada
                [texto reformulado]
                
                ### Alterações Realizadas
                - [lista de mudanças com justificativas]
                """
            )
            st.subheader("Texto Otimizado")
            st.markdown(resposta.text)

# --- Seção 2: Geração de Conteúdo ---
st.header("✨ Geração de Conteúdo")
campanha_brief = st.text_area("Briefing da Campanha:", help="Descreva objetivos, público-alvo e tom desejado")
col1, col2 = st.columns(2)

with col1:
    if st.button("Gerar Conceito Visual", key="gen_visual"):
        with st.spinner('Criando diretrizes visuais...'):
            prompt = f"""
            Crie especificações técnicas para designers baseadas em:
            Brief: {campanha_brief}
            Diretrizes: {conteudo}
            
            Inclua:
            1. 🎨 Paleta de cores exata (códigos HEX)
            2. 📐 Layout recomendado 
            3. 🖼️ Estilo fotográfico 
            4. ✨ Elementos gráficos obrigatórios
            5. ⚠️ Restrições criativas
            """
            resposta = modelo_texto.generate_content(prompt)
            st.subheader("Blueprint Visual")
            st.markdown(resposta.text)

with col2:
    if st.button("Gerar Copywriting", key="gen_copy"):
        with st.spinner('Desenvolvendo textos...'):
            prompt = f"""
            Crie textos para campanha alinhados a:
            Brief: {campanha_brief}
            Diretrizes: {conteudo}
            
            Entregue:
            - 🎯 Headline principal (3 opções)
            - 📝 Corpo de texto (tom {campanha_brief.split()[-1] if campanha_brief else 'inspiracional'})
            - 📢 Call-to-action (2 variações)
            """
            resposta = modelo_texto.generate_content(prompt)
            st.subheader("Textos Prontos")
            st.markdown(resposta.text)

# --- Estilização ---
st.markdown("""
<style>
    [data-testid="stHeader"] {background-color: #f5f5f5;}
    .st-bb {background-color: #f0f2f6;}
    .st-at {background-color: #4CAF50;}
    .st-ae {border-color: #4CAF50;}
</style>
""", unsafe_allow_html=True)