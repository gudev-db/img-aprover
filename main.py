import streamlit as st
from pptx import Presentation
import io
import pdfplumber
import google.generativeai as genai
import os
from PIL import Image
import requests




# Configuração inicial
st.set_page_config(
    layout="wide",
    page_title="Macfor AutoDoc",
    page_icon="assets/page-icon.png"
)
st.image('assets/macLogo.png', width=300)

st.header('Agente Holambra')
st.header(' ')




gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)
modelo_vision = genai.GenerativeModel("gemini-2.0-flash", generation_config={"temperature": 0.1})
modelo_texto = genai.GenerativeModel("gemini-1.5-flash")




# Carrega diretrizes
with open('data.txt', 'r') as file:
    conteudo = file.read()

tab_chatbot, tab_aprovacao, tab_geracao, tab_briefing = st.tabs([
    "💬 Chatbot Holambra", 
    "✅ Aprovação de Conteúdo", 
    "✨ Geração de Conteúdo",
    "📋 Geração de Briefing Holambra"
])


with tab_chatbot:  
    st.header("Assistente Virtual Holambra")
    st.caption("Pergunte qualquer coisa sobre as diretrizes e informações da Holambra")
    
    # Inicializa o histórico de chat na session_state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Exibe o histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Como posso ajudar?"):
        # Adiciona a mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Prepara o contexto com as diretrizes
        contexto = f"""
        Você é um assistente virtual especializado na Holambra Cooperativa Agroindustrial.
        Baseie todas as suas respostas nestas diretrizes oficiais:
        {conteudo}
        
        Regras importantes:
        - Seja preciso e técnico
        - Mantenha o tom profissional mas amigável
        - Se a pergunta for irrelevante, oriente educadamente
        - Forneça exemplos quando útil
        """
        
        # Gera a resposta do modelo
        with st.chat_message("assistant"):
            with st.spinner('Pensando...'):
                try:
                    # Usa o histórico completo para contexto
                    historico_formatado = "\n".join(
                        [f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages]
                    )
                    
                    resposta = modelo_texto.generate_content(
                        f"{contexto}\n\nHistórico da conversa:\n{historico_formatado}\n\nResposta:"
                    )
                    
                    # Exibe a resposta
                    st.markdown(resposta.text)
                    
                    # Adiciona ao histórico
                    st.session_state.messages.append({"role": "assistant", "content": resposta.text})
                    
                except Exception as e:
                    st.error(f"Erro ao gerar resposta: {str(e)}")

# --- Estilização Adicional ---
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    [data-testid="stChatMessageContent"] {
        font-size: 1rem;
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        padding: 0.5rem 1rem;
    }
    .stChatInput {
        bottom: 20px;
        position: fixed;
        width: calc(100% - 5rem);
    }
</style>
""", unsafe_allow_html=True)


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
                Você é um designer que trabalha para a Macfor Marketing digital e você deve gerar conteúdo criativo para o cliente Holambra Cooperativa Agroindustrial.

                Crie um manual técnico para designers baseado em:
                Brief: {campanha_brief}
                Diretrizes: {conteudo}
                
                Inclua:
                1. 🎨 Paleta de cores (códigos HEX/RGB)
                2. 🖼️ Diretrizes de fotografia
                3. ✏️ Tipografia hierárquica
                4. 📐 Grid e proporções
                5. ⚠️ Restrições de uso
                6. Descrição exata e palpável da imagem a ser utilizada no criativo que atenda a todas as guias acima
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




with tab_briefing:
    st.header("Gerador de Briefing Holambra")
    st.caption("Crie briefings completos para diferentes áreas de atuação da Holambra")
    
    # Setores específicos para Holambra
    setores_holambra = [
        "Marketing Digital", 
        "Redes Sociais", 
        "Campanhas Agrícolas", 
        "Comunicação Institucional",
        "Eventos e Feiras",
        "Produtos Agrícolas",
        "Relacionamento com Cooperados",
        "Sustentabilidade"
    ]
    
    # Layout em colunas
    col1, col2 = st.columns([1, 2])
    
    with col1:
        setor_selecionado = st.selectbox("Área de Atuação:", setores_holambra)
        nome_projeto = st.text_input("Nome do Projeto:")
        responsavel = st.text_input("Responsável pelo Briefing:")
        data_entrega = st.date_input("Data de Entrega Prevista:")
        
        # Campos comuns a todos os setores
        st.subheader("Informações Básicas")
        contexto = st.text_area("Contexto/Justificativa:", help="Por que este projeto está sendo realizado?")
        objetivos = st.text_area("Objetivos Principais:", help="O que se pretende alcançar com este projeto?")
        publico_alvo = st.text_area("Público-Alvo:", help="Quem será impactado por este projeto?")
        
        # Campos específicos por setor
        st.subheader("Informações Específicas")
        if setor_selecionado == "Marketing Digital":
            canais = st.multiselect("Canais Digitais:", ["Site", "Redes Sociais", "E-mail Marketing", "SEO", "ADS"])
            metricas = st.text_input("Métricas de Sucesso:")
        elif setor_selecionado == "Redes Sociais":
            plataformas = st.multiselect("Plataformas:", ["Facebook", "Instagram", "LinkedIn", "YouTube", "Twitter"])
            frequencia = st.selectbox("Frequência de Postagem:", ["Diária", "3x semana", "Semanal"])
        elif setor_selecionado == "Campanhas Agrícolas":
            cultura = st.text_input("Cultura Agrícola:")
            periodo_safra = st.text_input("Período da Safra:")
        elif setor_selecionado == "Comunicação Institucional":
            tom_voz = st.selectbox("Tom de Voz:", ["Institucional", "Técnico", "Inspiracional", "Educativo"])
        elif setor_selecionado == "Eventos e Feiras":
            tipo_evento = st.selectbox("Tipo de Evento:", ["Feira Agrícola", "Dia de Campo", "Palestra Técnica", "Workshop"])
            local = st.text_input("Local do Evento:")
        elif setor_selecionado == "Produtos Agrícolas":
            produto = st.text_input("Produto Foco:")
            diferencial = st.text_area("Diferenciais Competitivos:")
        elif setor_selecionado == "Relacionamento com Cooperados":
            quantidade_cooperados = st.number_input("Número de Cooperados Impactados:", min_value=1)
            canal_comunicacao = st.selectbox("Canal de Comunicação:", ["App", "Newsletter", "Reuniões", "WhatsApp"])
        elif setor_selecionado == "Sustentabilidade":
            iniciativa = st.selectbox("Tipo de Iniciativa:", ["Ambiental", "Social", "Econômica"])
            certificacoes = st.text_input("Certificações Relacionadas:")
    
    with col2:
        st.subheader("Preview do Briefing")
        
        if st.button("Gerar Briefing Completo", key="gen_briefing"):
            with st.spinner('Construindo briefing personalizado...'):
                try:
                    # Template de briefing com placeholders
                    prompt = f"""
                    Crie um briefing profissional para a Holambra Cooperativa Agroindustrial seguindo rigorosamente este padrão:

                    # BRIEFING {setor_selecionado.upper()} - HOLAMBRA
                    **Projeto:** {nome_projeto}
                    **Responsável:** {responsavel}
                    **Data de Entrega:** {data_entrega}

                    ## 1. CONTEXTO
                    {contexto}

                    ## 2. OBJETIVOS
                    {objetivos}

                    ## 3. PÚBLICO-ALVO
                    {publico_alvo}

                    ## 4. DIRETRIZES DA MARCA (Extraídas do data.txt)
                    {conteudo}

                    ## 5. INFORMAÇÕES ESPECÍFICAS
                    {f"Canais: {', '.join(canais)} | Métricas: {metricas}" if setor_selecionado == "Marketing Digital" else ""}
                    {f"Plataformas: {', '.join(plataformas)} | Frequência: {frequencia}" if setor_selecionado == "Redes Sociais" else ""}
                    {f"Cultura: {cultura} | Safra: {periodo_safra}" if setor_selecionado == "Campanhas Agrícolas" else ""}
                    {f"Tom de Voz: {tom_voz}" if setor_selecionado == "Comunicação Institucional" else ""}
                    {f"Evento: {tipo_evento} | Local: {local}" if setor_selecionado == "Eventos e Feiras" else ""}
                    {f"Produto: {produto} | Diferenciais: {diferencial}" if setor_selecionado == "Produtos Agrícolas" else ""}
                    {f"Cooperados: {quantidade_cooperados} | Canal: {canal_comunicacao}" if setor_selecionado == "Relacionamento com Cooperados" else ""}
                    {f"Iniciativa: {iniciativa} | Certificações: {certificacoes}" if setor_selecionado == "Sustentabilidade" else ""}

                    ## 6. CRONOGRAMA PRELIMINAR
                    - [ ] Definição de estratégia
                    - [ ] Desenvolvimento de materiais
                    - [ ] Aprovações
                    - [ ] Implementação
                    - [ ] Monitoramento

                    ## 7. ORÇAMENTO
                    A ser definido conforme escopo aprovado.

                    

                    IMPORTANTE:
                    - Mantenha o formato profissional
                    - Use linguagem clara e objetiva
                    - Destaque os pontos críticos
                    - Inclua todas as informações fornecidas
                    - Considere as diretrizes da Holambra em todas as seções
                    """

                    resposta = modelo_texto.generate_content(prompt)
                    
                    st.subheader(f"Briefing {setor_selecionado} - {nome_projeto}")
                    st.markdown(resposta.text)
                    
                    # Botão para download
                    briefing_txt = resposta.text
                    st.download_button(
                        label="Download do Briefing",
                        data=briefing_txt,
                        file_name=f"briefing_holambra_{nome_projeto.lower().replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"Erro ao gerar briefing: {str(e)}")

# Estilização adicional
st.markdown("""
<style>
    div[data-testid="stTabs"] {
        margin-top: -30px;
    }
    div[data-testid="stVerticalBlock"] > div:has(>.stTextArea) {
        border-left: 3px solid #4CAF50;
        padding-left: 1rem;
    }
    .stDownloadButton button {
        background-color: #2e7d32 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

