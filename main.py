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
st.header(' ')

# Configuração da API Gemini
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
    
    # Subtabs para geração de conteúdo
    subtab_ger1, subtab_ger2 = st.tabs(["📝 Gerar Texto", "🎨 Gerar Imagem"])
    
    with subtab_ger1:
        st.subheader("Criação de Textos")
        campanha_brief = st.text_area("Briefing criativo:", help="Descreva objetivos, tom de voz e especificações", height=150, key="text_brief")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Gerar Copywriting", key="gen_copy"):
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
                    st.subheader("Textos Gerados")
                    st.markdown(resposta.text)
        
        with col2:
            if st.button("Gerar Diretrizes de Estilo", key="gen_style"):
                with st.spinner('Criando guia de estilo textual...'):
                    prompt = f"""
                    Crie diretrizes de estilo de escrita baseado em:
                    Brief: {campanha_brief}
                    Diretrizes: {conteudo}
                    
                    Inclua:
                    - 🎭 Tom de voz recomendado
                    - 📝 Estrutura de parágrafos
                    - 🔤 Uso de vocabulário
                    - ❌ Palavras e frases a evitar
                    """
                    resposta = modelo_texto.generate_content(prompt)
                    st.subheader("Diretrizes de Estilo")
                    st.markdown(resposta.text)
    
    with subtab_ger2:
        st.subheader("Criação de Imagens")
        descricao_imagem = st.text_area("Descreva a imagem desejada:", help="Inclua elementos, estilo, cores e composição", height=150, key="img_desc")
        
        if st.button("Gerar Diretrizes Visuais", key="gen_visual"):
            with st.spinner('Criando especificações visuais...'):
                prompt = f"""
                Crie um manual técnico para designers baseado em:
                Descrição: {descricao_imagem}
                Diretrizes: {conteudo}
                
                Inclua:
                1. 🎨 Paleta de cores (códigos HEX/RGB)
                2. 🖼️ Estilo de composição
                3. ✏️ Tipografia recomendada
                4. 📐 Proporções e layout
                5. ⚠️ Restrições de uso
                """
                resposta = modelo_texto.generate_content(prompt)
                st.subheader("Diretrizes Visuais")
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
    /* Remove o efeito de hover dos botões */
    button[kind="secondary"] {
        background: #f0f2f6 !important;
        transition: none !important;
    }
    button[kind="secondary"]:hover {
        background: #f0f2f6 !important;
        border-color: #f0f2f6 !important;
    }
    /* Estilo para as subtabs */
    [data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }
</style>
""", unsafe_allow_html=True)