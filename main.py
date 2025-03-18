
import streamlit as st
from pptx import Presentation
import io
import pdfplumber
import google.generativeai as genai
import os
from PIL import Image

# Guias do cliente
guias = """

Comment: Usaria ícone ao lado das culturas para chamar atenção
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T19:25:15.769Z
----
Comment: achei que ficou com muita informação
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T19:24:09.943Z
----
Comment: Sugiro deixar a fonte mais de rodapé e trabalhar mais o título para chamar mais atenção
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T19:23:30.036Z
----
Comment: Esse cenário ainda continua com a virada do ano? Vale revisar/atualizar?
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T18:57:47.386Z
----
Comment: Será que vale falar para contarem com a Holambra na venda de sementes, tratamento e monitoramento?
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T18:51:31.840Z
----
Comment: o sol ficou muito estourado, né?
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T18:50:12.319Z
----
Comment: Como é sinal de atenção, colocaria um ícone para ilustrar
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T18:49:06.850Z
----
Comment: Verificar se o vermelho está correto. Na minha tela pareceu rosa. Além disso, confirmar se é  essa foto que é antiga (sem as atualizações do parque industrial)
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T18:47:17.778Z
----
Comment: @snjezana.abreu@holambra.com.br, validar com o Pitt. Pelo o que ouvi, ainda não é superior, mas até 400 mil. Talvez: armazenagem de até 400 mil toneladas
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-02-06T18:46:51.473Z
----
Comment: As # precisam ter caixa alta e baixa? É melhor para identificação?

EmCampo, DaSoja...
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-01-30T12:15:12.324Z
----
Comment: não gostei do gerúndio, talvez tirar?

... dessa jornada com soluções cada vez mais eficientes e sustentáveis
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-01-30T12:13:36.641Z
----
Comment: No primeiro evento do ano, realizado em Itaberá-SP, reunimos cooperados, produtores...
Created by: Holambra Cooperativa Agroindustrial
Created at: 2025-01-30T12:08:52.726Z
----
Comment: Sugestão: 

🌱Holambra em Campo 2025: conectando tecnologia e inovação na cultura da soja!

 
No primeiro evento do ano, reunimos cooperados, produtores, especialistas e empresas parceiras para compartilhar conhecimento, apresentar tendências e debater as inovações que estão transformando o campo.

Agradecemos a todos que participaram e às empresas que fazem parte dessa jornada, fortalecendo com soluções cada vez mais eficientes e sustentáveis.

🎥 Confira no vídeo os melhores momentos do Holambra em Campo e veja como, juntos, estamos cultivando o futuro da produção agrícola!
Created by: Snjezana Simunovic
Created at: 2025-01-28T16:45:37.150Z
----
Comment: cooperados, produtores, especialistas e empresas parceiras
Created by: Snjezana Simunovic
Created at: 2025-01-28T16:39:27.662Z
----
Comment: Algo mais nese sentido:

Demos início à programação de eventos de 2025 com o primeiro Holambra em Campo do ano, conectando tecnologia e inovação à cultura da soja!
Created by: Snjezana Simunovic
Created at: 2025-01-28T16:38:12.104Z
----
Comment: retirar
Created by: Snjezana Simunovic
Created at: 2025-01-28T16:32:55.861Z
----
Comment: Sugestão:

Parabéns, Santa Cruz do Rio Pardo! 

São 155 anos de história, crescimento e desenvolvimento! Desde julho de 2024, temos a honra de fazer parte com nossa loja, contribuindo para o progresso dos produtores locais e fortalecendo o agronegócio da região.

Queremos seguir ao lado dos nossos clientes santa-cruzenses, apoiando cada nova conquista! 

#HolambraCooperativa #Cooperativa #SantaCruzdoRioPardo
Created by: Snjezana Simunovic
Created at: 2025-01-20T17:50:04.526Z
----
Comment: Gosto mais dessa opção, mas não vejo qual a relevância dessa infermoção para o nosso negócio, não temos produtores de arroz.

Conforme combinado, nos aniversários das cidades, utilizaremos uma foto da cidade junto com a da loja ou unidade correspondente.
Created by: Snjezana Simunovic
Created at: 2025-01-20T14:34:08.755Z
----
comments_2025-02-27T11:12:29.725Z.txt
Displaying comments_2025-02-27T11:12:29.725Z.txt.
"""

# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

# Inicializa os modelos do Gemini
modelo_vision = genai.GenerativeModel("gemini-2.0-flash", generation_config={"temperature": 0.1})
modelo_texto = genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_pptx(file):
    prs = Presentation(file)
    slides_text = []
    for slide in prs.slides:
        slide_text = ""
        for shape in slide.shapes:
            if hasattr(shape, "text"):  # Verifica se o shape tem texto
                slide_text += shape.text + "\n"
        slides_text.append(slide_text.strip())
    return slides_text

def extract_text_from_pdf(file):
    pages_text = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or "(Página sem texto extraível)"
            pages_text.append(text)
    return pages_text

st.set_page_config(layout="wide")
st.title("Upload e Extração de Texto de PPTX e PDF")

# Campo de upload para múltiplos arquivos de diretrizes (PPTX ou PDF)
uploaded_guideline_files = st.file_uploader("Envie arquivos de diretrizes (.pptx, .pdf)", type=["pptx", "pdf"], accept_multiple_files=True)

# Campo de upload para a imagem
uploaded_image_file = st.file_uploader("Envie uma imagem para aprovação (.jpg, .jpeg, .png)", type=["jpg", "jpeg", "png"])

branding_material = ""
if uploaded_guideline_files:
    all_texts = []
    
    # Processa cada arquivo carregado
    for uploaded_guideline_file in uploaded_guideline_files:
        file_type = uploaded_guideline_file.name.split(".")[-1]
        
        if file_type == "pptx":
            texts = extract_text_from_pptx(io.BytesIO(uploaded_guideline_file.read()))
            all_texts.extend(texts)
        elif file_type == "pdf":
            texts = extract_text_from_pdf(io.BytesIO(uploaded_guideline_file.read()))
            all_texts.extend(texts)

    # Concatenar o texto extraído de todos os arquivos
    branding_material = "\n\n".join(all_texts)
    
    # Salvar em variável global
    st.session_state["extracted_texts"] = all_texts
    st.success("Texto extraído de todos os arquivos com sucesso!")

if uploaded_image_file is not None:
    st.image(uploaded_image_file, caption='Imagem Carregada', use_container_width=True)
    image = Image.open(uploaded_image_file)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    img_bytes = img_byte_arr.getvalue()
    mime_type = "image/png" if image.format == "PNG" else "image/jpeg"
    
    # Prompt para análise da imagem com base nas diretrizes
    prompt = f"""
    Você está aqui para aprovar imagens de criativos para campanhas de marketing digital para a cooperativa Holambra.
    Se atente ao mínimo e extremo detalhe de tudo que está na imagem, pois você é extremamente detalhista.
    
    O cliente Holambra já deu alguns feedbacks sobre criativos no passado.
    
    Considerando os materiais de branding do cliente e as diretrizes já existentes ({branding_material}) e em {guias},
    diga se a imagem seria aprovada ou não e o que precisa melhorar para ser aprovada.
    """
    
    try:
        with st.spinner('Analisando a imagem...'):
            resposta = modelo_vision.generate_content(
                contents=[prompt, {"mime_type": mime_type, "data": img_bytes}]
            )
            descricao = resposta.text
            st.subheader('Aprovação da Imagem')
            st.write(descricao)
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar a imagem: {e}")
        
if st.button("Remover Arquivo"):
    st.session_state.clear()
    st.experimental_rerun()
