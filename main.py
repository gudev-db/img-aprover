import streamlit as st
from pptx import Presentation
import io
import pdfplumber
import google.generativeai as genai
import os
from PIL import Image

# Configuração inicial
st.set_page_config(
    layout="wide",
    page_title="Macfor AutoDoc",
    page_icon="assets/page-icon.png"
)
st.image('assets/macLogo.png', width=300)

st.header('Agente Holambra')

gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)
modelo_vision = genai.GenerativeModel("gemini-2.0-flash", generation_config={"temperature": 0.1})
modelo_texto = genai.GenerativeModel("gemini-1.5-flash")

# Carrega diretrizes
with open('data.txt', 'r') as file:
    conteudo = file.read()

# --- Abas Principais ---
tab_aprovacao, tab_geracao = st.tabs(["✅ Aprovação de Conteúdo", "✨ Geração de Conteúdo"])

with tab_aprovacao:
    st.header("Validação de Materiais")
    subtab1, subtab2 = st.tabs(["🖼️ Análise de Imagens", "✍️ Revisão de Textos"])
    
    with subtab1:
        uploaded_image = st.file_uploader("Carregue imagem para análise (.jpg, .png)", type=["jpg", "jpeg", "png"], key="img_uploader")
        if uploaded_image:
            st.image(uploaded_image, use_column_width=True, caption="Pré-visualização")
            if st.button("Validar Imagem", key="analyze_img"):
                with st.spinner('Comparando com diretrizes da marca...'):
                    try:
                        image = Image.open(uploaded_image)
                        img_bytes = io.BytesIO()
                        image.save(img_bytes, format=image.format)
                        
                        resposta = modelo_vision.generate_content([
                            f"""Analise esta imagem considerando:
                            {conteudo}
                            Forneça um parecer técnico detalhado com:
                            - ✅ Acertos
                            - ❌ Desvios das diretrizes
                            - 🛠 Recomendações precisas""",
                            {"mime_type": "image/jpeg", "data": img_bytes.getvalue()}
                        ])
                        st.subheader("Resultado da Análise")
                        st.markdown(resposta.text)
                    except Exception as e:
                        st.error(f"Falha na análise: {str(e)}")

    with subtab2:
        texto_input = st.text_area("Insira o texto para validação:", height=200, key="text_input")
        if st.button("Validar Texto", key="validate_text"):
            with st.spinner('Verificando conformidade...'):
                resposta = modelo_texto.generate_content(
                    f"""Revise este texto conforme:
                    Diretrizes: {conteudo}
                    Texto: {texto_input}
                    
                    Formato requerido:
                    ### Texto Ajustado
                    [versão reformulada]
                    
                    ### Alterações Realizadas
                    - [lista itemizada de modificações]
                    ### Justificativas
                    [explicação técnica das mudanças]"""
                )
                st.subheader("Versão Validada")
                st.markdown(resposta.text)

with tab_geracao:
    st.header("Criação de Conteúdo")
    campanha_brief = st.text_area("Briefing criativo:", help="Descreva objetivos, tom de voz e especificações", height=150)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Diretrizes Visuais")
        if st.button("Gerar Especificações", key="gen_visual"):
            with st.spinner('Criando guia de estilo...'):
                prompt = f"""
                Crie um manual técnico para designers baseado em:
                Brief: {campanha_brief}
                Diretrizes: {conteudo}
                
                Inclua:
                1. 🎨 Paleta de cores (códigos HEX/RGB)
                2. 🖼️ Diretrizes de fotografia
                3. ✏️ Tipografia hierárquica
                4. 📐 Grid e proporções
                5. ⚠️ Restrições de uso
                """
                resposta = modelo_texto.generate_content(prompt)
                st.markdown(resposta.text)

    with col2:
        st.subheader("Copywriting")
        if st.button("Gerar Textos", key="gen_copy"):
            with st.spinner('Desenvolvendo conteúdo textual...'):
                prompt = f"""
                Crie textos para campanha considerando:
                Brief: {campanha_brief}
                Diretrizes: {conteudo}
                
                Entregar:
                - 🎯 3 opções de headline
                - 📝 Corpo de texto (200 caracteres)
                - 📢 2 variações de CTA
                - 🔍 Meta description (SEO)
                """
                resposta = modelo_texto.generate_content(prompt)
                st.markdown(resposta.text)

# --- Estilização ---
st.markdown("""
<style>
    div[data-testid="stTabs"] {
        margin-top: -30px;
    }
    div[data-testid="stVerticalBlock"] > div:has(>.stTextArea) {
        border-left: 3px solid #4CAF50;
        padding-left: 1rem;
    }
    button[kind="secondary"] {
        background: #f0f2f6 !important;
    }
</style>
""", unsafe_allow_html=True)