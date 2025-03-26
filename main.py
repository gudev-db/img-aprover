import streamlit as st
from pptx import Presentation
import io
import pdfplumber
import google.generativeai as genai
import os
from PIL import Image
from google.generativeai.types import Tool, GenerateContentConfig, GoogleSearch

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
    campanha_brief = st.text_area("Briefing criativo:", help="Descreva objetivos, tom de voz e especificações", height=150)
    
    # Seção de pesquisa de tendências
    st.subheader("🔍 Pesquisa de Tendências")
    with st.expander("Adicionar temas de pesquisa"):
        tema1 = st.text_input("Tema de pesquisa 1", placeholder="Ex.: Tendências em embalagens sustentáveis")
        tema2 = st.text_input("Tema de pesquisa 2", placeholder="Ex.: Inovações no agronegócio 2024")
        tema3 = st.text_input("Tema de pesquisa 3", placeholder="Ex.: Novas tecnologias para cooperativas")
    
    temas_pesquisa = [t for t in [tema1, tema2, tema3] if t]  # Filtra temas não preenchidos
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Diretrizes Visuais")
        if st.button("Gerar Especificações", key="gen_visual"):
            with st.spinner('Criando guia de estilo com base nas tendências...'):
                # Incorpora os temas de pesquisa no prompt
                prompt_tendencias = ""
                if temas_pesquisa:
                    prompt_tendencias = f"""
                    ### Tendências de Mercado:
                    {', '.join(temas_pesquisa)}
                    """
                
                prompt = f"""
                Crie um manual técnico para designers baseado em:
                Brief: {campanha_brief}
                Diretrizes: {conteudo}
                {prompt_tendencias}
                
                Inclua:
                1. 🎨 Paleta de cores (códigos HEX/RGB) que reflitam essas tendências
                2. 🖼️ Diretrizes de fotografia atualizadas
                3. ✏️ Tipografia hierárquica moderna
                4. 📐 Grid e proporções contemporâneas
                5. ⚠️ Restrições de uso
                
                Destaque como as tendências foram incorporadas ao design.
                """
                resposta = modelo_texto.generate_content(prompt)
                st.subheader("Diretrizes Visuais com Tendências")
                st.markdown(resposta.text)

    with col2:
        st.subheader("Copywriting")
        if st.button("Gerar Textos", key="gen_copy"):
            with st.spinner('Desenvolvendo conteúdo alinhado às tendências...'):
                # Incorpora os temas de pesquisa no prompt
                prompt_tendencias = ""
                if temas_pesquisa:
                    prompt_tendencias = f"""
                    ### Contexto de Tendências:
                    Considere estas tendências no desenvolvimento dos textos:
                    {chr(10).join(f'- {t}' for t in temas_pesquisa)}
                    """
                
                prompt = f"""
                Crie textos para campanha considerando:
                Brief: {campanha_brief}
                Diretrizes: {conteudo}
                {prompt_tendencias}
                
                Entregar:
                - 🎯 3 opções de headline que incorporem as tendências
                - 📝 Corpo de texto (200 caracteres) com linguagem atual
                - 📢 2 variações de CTA modernas
                - 🔍 Meta description (SEO) com palavras-chave relevantes
                
                Destaque como o texto reflete as tendências atuais do mercado.
                """
                resposta = modelo_texto.generate_content(prompt)
                st.subheader("Textos com Tendências Incorporadas")
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
    .st-expander {
        background: #f9f9f9;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)