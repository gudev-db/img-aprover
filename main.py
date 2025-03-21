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


st.set_page_config(layout="wide")

# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

# Inicializa os modelos do Gemini
modelo_vision = genai.GenerativeModel("gemini-2.0-flash", generation_config={"temperature": 0.1})
modelo_texto = genai.GenerativeModel("gemini-1.5-flash")

with open('data.txt', 'r') as file:
    # Lendo o conteúdo do arquivo e salvando em uma variável
    conteudo = file.read()


def extract_text_from_pptx(file):
    prs = Presentation(file)
    slides_text = []
    for slide in prs.slides:
        slide_text = ""
        for shape in slide.shapes:
            if hasattr(shape, "text"):
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

st.title("Aprovação de Imagens e Correção de Textos")

tipo_aprovacao = st.selectbox("Selecione o tipo de conteúdo:", ["Imagem", "Texto", "Conteúdo de Campanha"])


guias_param = modelo_texto.generate_content(f'''O cliente Holambra enviou alguns comentários sobre a aprovação de alguns criativos prévios em {guias}, extraia parâmetros de aprovação com base 
nesses comentários e os salve em formato de texto para serem utilizados em análises futuras.''')




if tipo_aprovacao == "Imagem":
    uploaded_image_file = st.file_uploader("Envie uma imagem para aprovação (.jpg, .jpeg, .png)", type=["jpg", "jpeg", "png"])

    if uploaded_image_file is not None:
        st.image(uploaded_image_file, caption='Imagem Carregada', use_container_width=True)
        image = Image.open(uploaded_image_file)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format)
        img_bytes = img_byte_arr.getvalue()
        mime_type = "image/png" if image.format == "PNG" else "image/jpeg"

        prompt = f"""
        Você está avaliando uma imagem para campanhas da Holambra Cooperativa Agroindustrial.
        
        Você é um especialista em design gráfico.
        
        Considere os seguintes parâmetros de aprovação de criativos do cliente: ({guias_param}).
        Se não o for, não as mencione.

        
        Além disso, aqui está o material de referência enviado para embasar sua análise (esse material se refere a como a marca deve se apresentar ao público. Veja se a imagem subida atende a 
        esses requisitos (analise atentamente a imagem subida para garantir que ela atende a essas diretrizes. Você deve analisar profundamente a imagem de uma forma que você possa dizer
        com toda certeza se ela atente aos requisitos):

        BEGIN DIRETRIZES
        # Guias de Marca
        - {guias_marca}
        # Iconografia
        - {iconografia}
        # Fotografia
        - {fotografia}
       
        # Elementos gráficos
        - {elemento_graf}
        
        # Símbolos
        - {simbolo}
        # Diretrizes de campanhas
        - {campanhas}
        END DIRETRIZES
         
        - Analise a imagem por inteiro levando em conta as diretrizes.
        - Analise e compreenda cada aspecto e elemento da imagem.
        
        O Seu papel é pegar as diretrizes, analisar a imagem e, com base nelas, dizer se a imagen seria aprovada ou não e porquê.

        - Não me repita de volta as diretrizes
        
        - Você não deve me dizer que algo deve ser verificado. VOCÊ é quem verifica.

        - Seu retorno deve ser bullet points justificando o porque a imagem é aprovada ou não. Detalhando quais atributos da imagem subida não se alinham com as diretrizes do cliente



        Siga esse fluxo:
        Aprendizado com diretrizes > Análise da imagem > entendimento de se a imagem se alinha com as diretrizes > aprovação ou não da imagem com justificativas 
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

elif tipo_aprovacao == "Texto":
    texto_para_correcao = st.text_area("Cole o texto que deseja corrigir:")

    if st.button("Corrigir Texto"):
        if texto_para_correcao.strip() or texto_extraido.strip():
            prompt_texto = f"""
            Você é um revisor de textos altamente detalhista.
            Aqui está o material de referência extraído do arquivo enviado:
           {guias_marca}
            
            E aqui está o texto que precisa ser revisado:
            {texto_para_correcao}

            Com base no material de referência, nos feedbacks prévios ({guias} e {guias_marca}) e no branding da Holambra, revise o texto e sugira melhorias para melhorar clareza, impacto e adequação ao contexto.
            """

            try:
                with st.spinner('Analisando e corrigindo o texto...'):
                    
                    resposta_texto = modelo_texto.generate_content(prompt_texto)
                    texto_corrigido = resposta_texto.text
                    st.subheader("Texto Corrigido:")
                    st.write(texto_corrigido)
            except Exception as e:
                st.error(f"Ocorreu um erro ao processar o texto: {e}")
        else:
            st.warning("Por favor, insira um texto ou envie um arquivo para análise.")

elif tipo_aprovacao == "Conteúdo de Campanha":
    descricao_campanha = st.text_area("Descreva brevemente a campanha desejada:")

    if st.button("Gerar Conteúdo"):
        if descricao_campanha.strip():
            prompt_campanha = f"""
            Você é um redator publicitário especializado.
            Baseado na seguinte descrição: {descricao_campanha},
            e considerando os parâmetros da Holambra ({guias_param}),
            gere um texto de campanha atrativo e persuasivo. 

            Considerando as diretrizes de marca:
            {conteudo}

            Seja bem detalhista.

            Primeiramente, me descreva com exatidão, detalhe, investigatividade, palpabilidade, ao mínimo detalhe e em um parágrafo bem extenso, o que há na imagem e todos os atributos da imagem.

            
            Você não deve dizer que o criativo 'deve seguir os documentos fornecidos'. Com base no que você aprendeu com os ditos documentos, diga 
            exatamente o que deve ser feito. Qual imagem exata e detalhada para seguir o guia de marca? Quais icones usar? Como a fotografia deve ser?
            Qual tipografia usar? Como deve ser o layout? Quais elementos gráficos utilizar? Se usar degradê, como ele deve ser usado? Qual paleta de cor usar?
            Quais símbolos utilizar? O que utilizar das diretrizes da campanha nessa campanha? Você deve me dizer exatamente o que deve ser feito. Você é o criador
            com base no que você aprendeu. Não referencie os documentos de aprendizado na sua resposta. Você deve extrair o conteúdo delas, aprender o que a Holambra
            espera do uso de sua marca e construir os criativos de campanha. Não seja vago. Um designer gráfico deve poder ler a sua descrição se saber exatamente o que
            deve ser feito. Traga palpabilidade na sua resposta. Descreva em parágrafos de 3 a 5 frases cada elemento que você traz.

            - Você não deve me falar sobre as diretrizes para a criação da campanha. Você me deve descrever como ela o é.

            
            """
            try:
                with st.spinner('Gerando conteúdo de campanha...'):
                    resposta_campanha = modelo_texto.generate_content(prompt_campanha)
                    st.subheader("Conteúdo de Campanha Gerado:")
                    st.write(resposta_campanha.text)
            except Exception as e:
                st.error(f"Erro ao gerar conteúdo: {e}")
        else:
            st.warning("Por favor, insira uma descrição da campanha.")

if st.button("Limpar e Reiniciar"):
    st.session_state.clear()
    st.experimental_rerun()
