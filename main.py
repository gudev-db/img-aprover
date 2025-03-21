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

guias_marca = '''
Queremos que nossos clientes nos reconheçam como referência no mercado, confiando em nossa expertise e buscando nossas soluções.

OBJETIVO

Criar uma marca forte para manter a fidelização do nosso público:
Ampliar a presença de marca;
Fortalecer o posicionamento;
Melhorar engajamento.

O objetivo da estratégia para as redes sociais da Holambra Cooperativa é fortalecer a presença digital regional e expandir para novas áreas, além de aumentar o engajamento, posicionar e transmitir confiança ao público.


Reuniões semanais + reunião mensal de pauta + cronogramas agosto, setembro, outubro.

Formato e dimensões de materiais alinhado com cada canal:
Instagram: Carrossel, story, reels, imagem única, motion (vetores)

Facebook e Linkedin: Vídeo extenso, imagem única, motion (vetores)

Youtube: Vídeo extenso, shorts, motion (vetores)

WhatsApp: Vídeos curtos, imagem única, motion (vetores)


Produção de conteúdos reais e de utilidade 
Mostrar processos reais, com erros e acertos gerando sentimento de familiaridade e pertencimento
Processo criativo eficaz pensando nas dores do cliente (como transformar a vida do meu cliente?/Isso faz sentido na vida do meu cliente?)


O setor é figital (físico e digital): Os consumidores navegam entre o mundo físico e digital, utilizando ambos para tomar decisões.

Simplicidade: Valorizam a simplicidade, evitando textos longos e complexos, que não prendem sua atenção.

Descomplicação: Precisam de explicações curtas e diretas; perderão o interesse se o conteúdo for prolixo.

Valorização mútua: Têm grande apreço por marcas e pessoas que demonstram reconhecimento e valorização.

Valorização de opiniões: Procuram por recomendações e histórias de sucesso como base para suas escolhas. Levam em conta opiniões de vizinhos, familiares, influenciadores e do mercado.

Defendem causas com convicção: São firmes em suas crenças e causas.

Praticidade: São diretos e práticos, não têm paciência para desculpas ou comportamentos sentimentais.

Falta de tempo: Valorizam muito seu tempo e preferem interações rápidas e eficientes.


Perfil desconfiado: Tendem a seguir pessoas que já conhecem pessoalmente ou que encontraram em feiras e eventos.

Pesquisa online, compra offline: Embora realizem pesquisas sobre produtos na internet, preferem finalizar a compra com o apoio de um atendimento humano.

Encaminhar e compartilhar – mais do que comentar e dar like: Preferem compartilhar conteúdos relevantes e úteis, especialmente pelo WhatsApp, ao invés de interagir com curtidas e comentários nas redes sociais.

Atenção ao WhatsApp: Prestam muita atenção ao que recebem via WhatsApp e, se algo é realmente bom, preferem compartilhar via print e encaminhar pela conversa.

Preferência por vídeos: Consomem conteúdo audiovisual com maior interesse, valorizando vídeos curtos e diretos.

Comunicação por áudio: Costumam enviar mensagens de áudio ao invés de textos, preferindo a praticidade e rapidez dessa forma de comunicação.


ENTRETER
EDUCAR
INSPIRAR
CONVENCER
DESCOBERTA
DA MARCA
COMPRA
APELO EMOCIONAL
APELO EMOCIONAL
Virais
Memes
Vídeos curtos
Histórias
Dia a dia
Histórias de vida
Antes e depois
Conquistas
Imagens bonitas
Como fazer
Dicas
Passo a passo
Especialistas
Infográfico
Dia a dia
Prova social
Benefícios
Resultados

RELACIONAR
data comemorativa • histórias de clientes • eventos
agroinfluencer • atualização de safra • isso ou aquilo

MAPA DE INTENÇÃO

EDUCAÇÃO
PRODUTOS/SERVIÇOS
INSPIRAÇÃO
RELACIONAMENTO
INSTITUCIONAL E VALORES
Objetivo:
Fortalecer a identidade corporativa enquanto comunicamos os valores e compromissos da empresa.

Conteúdo:
Missão, visão, valores, iniciativas de responsabilidade social, eventos, práticas sustentáveis e conquistas da Cooperativa.

Canais:
Instagram, Facebook, LinkedIn, YouTube e WhatsApp.


INSTITUCIONAL
EDUCAÇÃO
PRODUTOS/SERVIÇOS
RELACIONAMENTO
HISTÓRIAS DE SUCESSO
Objetivo:
Humanizar a marca e mostrar o impacto positivo na vida dos cooperados.

Conteúdo:
Perfis de cooperados de sucesso, entrevistas, histórias inspiradoras, relatos de experiências pessoais.

Canais:
Instagram, Facebook e YouTube.
RESULTADOS E CASOS DE SUCESSO
Objetivo:
Demonstrar os resultados alcançados com os produtos e serviços da Holambra.

Conteúdo:
Estudos de caso, resultados de implementações, depoimentos de clientes.

Canais:
Instagram, LinkedIn e WhatsApp


INSTITUCIONAL
PRODUTOS/SERVIÇOS
INSPIRAÇÃO
RELACIONAMENTO
INOVAÇÕES E TECNOLOGIAS
Objetivo:
Apresentar as últimas inovações e tecnologias do setor agrícola.

Conteúdo:
Novas tecnologias, métodos inovadores de cultivo, ferramentas de precisão agrícola.

Canais:
Instagram, LinkedIn e YouTube.
ESPECIALISTAS E EDUCAÇÃO TÉCNICA
Objetivo:
Reforçar a autoridade da marca e oferecer valor educacional.

Conteúdo:
Assuntos técnicos, vídeos educativos, webinars, entrevistas com especialistas.

Canais:
Instagram, LinkedIn, YouTube e WhatsApp.
SAFRAS E CULTURAS
Objetivo:
Fornecer informações relevantes e contextuais sobre o cotidiano agrícola.

Conteúdo:
Notícias sobre safras, dicas de cultivo, atualizações sobre culturas.

Canais:
Instagram, Facebook, YouTube e WhatsApp.
MERCADO, ANÁLISES E INFORMATIVOS
Objetivo:
Ajudar os produtores na tomada de decisões informadas.

Conteúdo:
Análises de mercado, previsões econômicas, tendências agrícolas, políticas e regulamentos.

Canais:
Instagram, LinkedIn e WhatsApp



Instagram, Facebooke YouTube
Foco em conteúdos visuais, interativos, educativos e de fácil consumo.

LinkedIn
Foco em conteúdos densos, informativos e educativos, priorizando um tom profissional e de posicionamento.

WhatsApp
Foco no relacionamento com o público. Mescla entre conteúdos de fácil consumo com informativos e institucionais.
Estratégia por canal
Abordagem de cada rede social para Holambra Cooperativa



"VALORIZAR
o passado, investir no presente 
e acreditar no futuro.”
Há 60 anos , a Cooperativa Agro Industrial 
Holambra é um verdadeiro modelo de 
cooperativismo de sucesso no Brasil .



POSICIONAMENTO 
DE MARCA
Gerar riqueza e desenvolvimento 
sustentável.FAZ PARTE DA NOSSA ESTRATÉGIA
É preciso um planejamento 
conciso e um posicionamento 
de marca coeso.


UMA MARCA FORTE
U M A  F O R Ç A  M A R C A N T E
E um modelo de negócio que, reconhecidamente, entrega atributos que endossam todas as 
características de uma parceria bem sucedida.
A essência do negócio, desde seus pilares estruturais, passando por seus valores, princípios e pontos de destaque, confirmado s 
por uma pesquisa sólida e bastante completa com cooperados, produtores, empresas e consumidores, que ajudaram a validar 
alguns caminhos e definir o projeto de futuro.



ESSÊNCIA DO NEGÓCIO
FOCO ESTRATÉGICO PROPÓSITO MOTIVAÇÃO
Senso Coletivo
Gerar Riqueza e Desenvolvimento SustentávelEspírito Cooperativista
Trabalhar para produzir mais e melhor para todosRazão de existir O que nos move Chave do sucesso
Excelência Operacional Orientada ao Produtor Respeito à Cultura
Fazemos 
AcontecerValorizamos Nossa 
GenteConstruímos um 
Futuro MelhorAtuamos pelo 
bem comumIncentivamos a 
Proatividade e InovaçãoAgimos com Ética 
e TransparênciaO que nos define
VALORESQualidade Profissionalismo Estrutura Valor AgregadoFORTALEZASO que fazemos bem


ATRAVÉS DA 
INCANSÁVEL 
BUSCA PELA 
Q U A L I D A D E  C O N T Í N U A .RELAÇÕESObcecados  pela qualidade  nasPROCESSOSObcecados  pela qualidade  nos
PRODUTO  FINALObcecados pela qualidade no


CONCEITO DE MARCA
A S S I N A T U R A
Cultura de qualidade.
A busca  constante  pela mais  alta qualidade,  que se reflete  nos 
valores  da cooperativa,  na sua atuação  e em seus  produtos . Uma  
dualidade  que expressa  Cultura  enquanto  valores  e plantio,  
Qualidade  enquanto  excelência  e adjetivos .
Cultura  de Qualidade  em RESULTADOS;
Cultura  de Qualidade  nos NEGÓCIOS;
Cultura  de Qualidade  nos RELACIONAMENTOS;
Cultura  de Qualidade  no ACESSO AO MERCADO;
Cultura  de Qualidade  para CRESCER MAIS; etc.


A PERSONALIDADE 
DA MARCA
P E R S O N A L I D A D E
Arquétipo  do prestativo
Uma  persona  cuidadora,  altruísta  e generosa  — com um 
grande  senso  de coletividade .Nossa marca é cuidadora
Nossa  marca  é feminina .
Mais  do isso, é mãe. De 3 filhos,  vivida,  experiente  e com bagagem . 
Uma mulher  forte,  na casa  dos 50 anos,  já com bastante  repertório,  
mas que segue  aprendendo,  ávida  por novidades .
É conectada,  antenada,  confiável,  de fala simples .
Profissional,  exigente,  justa  e amiga .
Sempre  acessível,  defende  com unhas  e dentes  seus  filhos .


A VOZ DA MARCA
P E R S O N A L I D A D E
Coletivo  acima  do indivíduoSempre na 1ª pessoa do plural
Em uma cooperativa,  a voz da coletividade  prevalece  sobre  
quaisquer  perspectivas  individuais . Por isso, nossa  marca  
deve  se expressar,  preferencialmente  na 1ª pessoa  do plural .
Dessa  forma,  geramos  mais  proximidade  junto  aos nossos  
diversos  públicos  externos,  e maior  identificação  junto  a todos  
os nossos  públicos . 
Nós somos .
Nós fazemos .
Nós investimos .
Nós conquistamos .
Mas com protagonismo  de liderança .
Indicar  o caminho , dar a direção , mas sempre ir junto .
Nunca  sendo  autoritário .


REVITALIZAMOS A NOSSA MARCA 
SEM PERDER NOSSA ESSÊNCIA
E INSPIRADOS POR ESTE POSICIONAMENTO
E COM BASE NA NOSSA MARCA ATUAL


C O R E S  
O R I G I N A I SC O R E S  
N O V A S
Inspiração na bandeira da Holanda 
(não permite contraste entre azul e 
vermelho)Releitura das cores originais, com intuito 
de promover melhor o contraste entre o 
azul e o vermelhoCORES

PERTENCIMENTOPARTICIPAÇÃO
INTEGRAÇÃOTECNOLOGIA
INOVAÇÃOEXCELÊNCIA
CAPACITAÇÃOCULTURA
RELACIONAMENTOVIVÊNCIACONHECIMENTO
INTEGRIDADEPARCERIACONFIANÇAAPRENDIZADO
CONEXÃO


A COOPERATIVA
Modelo de sucesso no cooperativismo brasileiro, a Holambra Cooperativa Agroindustrial  
chegou aos seus primeiros 60 anos com números que comprovam a sua força e importância 
para o nosso agronegócio:
1 unidade central + 7 filiais
Mais de
62 mil hectares 
cultivadosMais de
R$ 1,8 bilhão
de faturamento
anualUnidade Central de Paranapanema
Mais de
150 agricultores
cooperados
6 7 A Cooperativa A Cooperativa


Atualmente, contamos com 
diversas frentes de trabalho 
e serviços, sendo referência 
nacional na produção de grãos, 
além de termos atuações 
destacadas no beneficiamento 
de cereais, e nos cultivos 
de algodão e diversas frutas 
temperadas tropicais.
Nossa nova marca chega para, 
literalmente, marcar um novo 
momento em nossa trajetória, 
no qual reestruturamos nossos 
negócios e nossa cultura interna, 
prontos para produzir os 
próximos 60 anos de conquistas.Unidade de Takaoka
Unidade Avaré Unidade Central - Paranapanema Unidade Taquarivaí Unidade Takaoka
Unidade São Manuel Unidade Itaberá Unidade Taquari Unidade TaquaritubaUNIDADES
8 9 Brand Book 2021 Holambra Cooperativa Agroindustrial Unidades


TEMPO
1960 1970 1980 1990 2000 2010 2021Nossa Cooperativa foi fundada
em 23 de dezembro de 1960, no 
município de Paranapanema-SP.
Nossos primeiros produtores
chegaram em 1962, sendo parte
deles imigrantes holandeses e outros 
vindos da Cooperativa Agropecuária 
Holambra (esta sediada no
município de Holambra-SP).
Desde então, passamos por 
inúmeras fases, agrupadas aqui 
em nossas décadas de atuação:Destaque para
arroz e milho. Chegada dos 
primeiros produtores, com a 
Cooperativa financiando terras, 
infraestruturas agrícolas e 
benfeitorias, como residências, 
hospital, supermercado, escola 
manutenção de estradas etc.Expansão do
cultivo de soja e algodão, 
com incrementos também 
em flores e frutas. Construção 
de infraestruturas como silos, 
descaroçador de algodão, 
fábrica de polpas,
câmaras frias etc.
Primeira grande reestruturação 
da Cooperativa. 
Direcionamento de recursos 
para irrigação, beneficiando 
cereais e fruticultura. Aumento 
da produção de flores. Consolidação das
lavouras de cereais irrigadas, 
com duas a três culturas por ano,
e expansão da fruticultura. 
Reestruturação técnica e de capital, 
buscando investimentos
para o futuro.
Ampliação das estruturas
de recepção de cereais
(de 30 mil para 120 mil toneladas) 
e beneficiamento de algodão 
(de 15 para 60 fardos/hora). 
Faturamento de
R$ 230 milhões/ano.Chegamos aos 60 anos,
em 2020, com um faturamento 
superior a R$ 1,3 bilhão,
promovendo uma nova estrutura 
organizacional que, desde já, 
prepara a nossa Cooperativa
para os desafios do futuro.Reconhecida pela  
(Revista EXAME) como a
décima melhor empresa do setor 
de cereais e algodão do país. 
O beneficiamento de algodão 
atingiu 75 fardos/hora. Início da 
produção de laranja. Faturamento 
de R$ 420 milhões em 2011.
LINHA DO
Holambra Cooperativa Agroindustrial Brand Book 2021
10 11 Linha do Tempo Linha do Tempo



E VALORESMISSÃO, VISÃO
Vivemos um momento de constantes transformações — no agro, em seus negócios, e nos diversos 
contextos e cenários a eles relacionados. Por isso, realizamos uma profunda imersão para conhecer 
ainda melhor a nossa Cooperativa, as nossas tradições e tudo o que compõe o nosso Jeito de Ser 
Holambra, mantendo a nossa essência de marca forte. 
E, como resultado, promovemos a evolução da nossa cultura interna organizacional, renovando 
nossa Missão, Visão e nossos Valores — que representam os ideais, os comportamentos do dia a 
dia e os resultados que queremos, criando assim a nossa própria identidade. 
Integrados, esses elementos reforçam a importância da contribuição de todos na construção da 
nossa história, traduzem o nosso orgulho em contar com o melhor time, além de nos preparar para 
os desafios de hoje e para as conquistas do futuro.M
ISSÃ
OVISÃO
V
A
LORESFazemos
acontecer
Construímos
um Futuro MelhorValorizamos
Nossa Gente
Atuamos pelo
bem comumAgimos 
com Ética e 
Transparência
Incentivamos
a Proatividade
e InovaçãoSer a referência no
agronegócio em nossa região, 
atuando com excelência em 
gestão, responsabilidade 
social e ambiental.
Gerar riqueza e
desenvolvimento sustentável 
para Cooperados, 
Colaboradores e Parceiros.
12 Missão, Visão e Valores Holambra Cooperativa Agroindustrial



ESSÊNCIA DO NEGÓCIO
BUSINESS DRAW
Fazemos
Acontecer
Compromisso com
o cliente, entregando
resultados com
excelência e agilidade.Valorizamos
Nossa Gente
Respeito a nossa
história, pelas pessoas
e incentivo às
relações de confiança.Qualidade
Rigor na produção vinda
do manejo e da tecnologia no campo,
respeito às normas e aos processos
de trabalho e investimento
em capacitação de pessoal.Respeito à Cultura
Nossa tradição de empreendedorismo e
trabalho resiliente permeia a forma como
queremos ser e é o que nos diferencia. Senso de
responsabilidade e compromisso com a
sociedade e sustentabilidade são o nosso legado.Senso Coletivo
Gerar Riqueza e Desenvolvimento SustentávelEspírito Cooperativista
Trabalhar para produzir mais e melhor para todos
Agimos com Ética
e Transparência
Integridade e
honestidade são a
nossa essência.Profissionalismo
Altíssima percepção profissional do
mercado, com governança que permite
qualificar a equipe, tomar decisões
com base em dados e trabalhar o senso
de dono nos cooperados.Excelência Operacional
Manter-se capacitada para operar em todas as
áreas de forma abrangente, com estrutura
moderna, processos eficientes e alto padrão de
qualidade, permitindo a sinergia completa entre
Cooperativa e Cooperados
Incentivamos a
Proatividade e Inovação
Sempre em busca de
melhoria contínua,
estimulando a mentalidade
digital e de novas tecnologias.Estrutura
Sítios modernos e dimensionados
para absorver o crescimento
planejado, investimento massivo
em pesquisa, desenvolvimento
e parcerias estratégicas pontuais.
o que nos define
VALORESo que fazemos bem
FORTALEZASChave do sucesso
FOCO ESTRATÉGICORazão de existir
PROPÓSITOO que nos move
MOTIVAÇÃO
Atuamos pelo
Bem Comum
Superação dos interesses
individuais em prol do
coletivo, guiados pelo
princípio do cooperativismo.Valor Agregado
Além da qualidade real
das produções, oferecemos serviços
financeiros, inteligência no campo
e assistência técnica, colocando o
produtor sempre em primeiro lugar.Orientar o Produtor
Entender as necessidades dos produtores e agir
com inteligência e agilidade para ofertar
soluções que os auxiliem no dia a dia, do plantio
à colheita, da distribuição à venda, agregando
valor à sua produção.
Construímos um
Futuro Melhor
Construindo o futuro
das próximas gerações
com planejamento
e sustentabilidade.
14 15 Business Draw Brand Book 2021 Business Draw



Arquetipicamente (de acordo
com os modelos estabelecidos
por Carl Jung, criador da 
psicologia analítica), nossa marca 
se apoia nas características
de uma persona prestativa, 
ou seja, cuidadora, altruísta 
e generosa — enfim, com um 
grande senso de coletividade.
Dessa forma, estabelecemos 
que nossa marca tem 
personalidade feminina,
podendo ser representada
(e mais bem compreendida)
pela figura de uma mãe: • mulher forte, na casa dos 50 anos, 
  vivida, experiente e com bagagem 
  (aspectos que tangibilizam a história 
  e a trajetória da nossa Cooperativa); 
 • possui três filhos (que defende  
  com unhas e dentes), cuida e  
  se relaciona com um grupo de pessoas  
  (indica a atuação da cooperativa em  
  prol dos interesses coletivos, ou seja,
  de seus cooperados); 
 • possui um grande repertório, mas 
  segue aprendendo, ávida por 
  novidades (postura fundamental para 
  que continuemos a atravessar os anos 
  sempre em dia com o futuro); 
 • conectada, antenada, confiável, de  fala 
  simples e sempre  acessível (parceira); 
 • profissional, exigente, justa e amiga 
  (expressa o nosso compromisso com a 
  qualidade, como veremos mais à frente).BRAND PERSONA
Prestativa,
cuidadora,
altruísta
e generosa.
Governante
AmanteBobo
da CorteCara ComumInocenteExploradorSábio
Rebelde
Mago
Herói
Cuidador
CriadorCONTROLE
INTIMIDADEPRAZERCOMUNIDADESEGURANÇALIBERDADECOMPREENSÃO
LIBERTAÇÃO
PODER
EXCELÊNCIA
AJUDA
INOVAÇÃORisco e 
e ControleIndependência
e Realização
Estabilidade
e PrazerExcelência
Comunidade
16 17 Brand Persona Brand Persona


(Nós) Somos a Holambra Cooperativa 
Agroindustrial.
(Nós) Produzimos riqueza e resultados
para o agro e para cada um de nós.
(Nós) Temos orgulho de fazer parte
dessa história.
(Nós) Construímos uma cultura
interna abrangente.
(Nós) Na Holambra Cooperativa 
Agroindustrial, contamos com a mais 
completa infraestrutura.
Na Holambra Cooperativa Agroindustrial, 
(nós)  investimos constantemente na 
tecnificação de cultivos.
O que nos move (move a nós) são os
interesses dos nossos cooperados.A Holambra Cooperativa Agroindustrial (ela) 
está entre as mais destacadas do setor.
(Ela) A Cooperativa (impessoal) produz 
resultados e riqueza para seus cooperados
e colaboradores (eles) e para todo o agro.
Os Colaboradores (eles) da Holambra (ela)
têm orgulho de fazer parte de sua história
(a história dela).
A cultura interna da Holambra Cooperativa 
Agroindustrial (dela) é abrangente.
A Holambra (ela) conta com a mais
completa infraestrutura.
A Cooperativa (impessoal) investe 
constantemente na tecnificação de cultivos.
O que move a Holambra (você, ela) são os 
interesses dos cooperados (deles).COMO FALAMOS  SOBRE NÓS COMO EVITAMOS  FALAR SOBRE NÓS
Em uma cooperativa, a voz da coletividade 
prevalece sobre quaisquer perspectivas 
individuais. Por isso, nossa marca deve se 
expressar, preferencialmente na 1a pessoa 
do plural. Dessa forma, geramos mais 
proximidade junto aos nossos diversos 
públicos externos e maior identificação 
junto aos nossos Colaboradores e 
Cooperados. A seguir, mostramos alguns 
exemplos de aplicação desse tom de voz:BRAND
VOICE
18 19 Brand Book 2021 Holambra Cooperativa Agroindustrial Brand Voice


CARACTERÍSTICA
DA VOZ
Coletiva
Qualitativa
Líder
ColaborativaDISCRIÇÃO
Buscamos proximidade 
e identificação junto aos 
nossos diversos públicos.
O que nos move é a busca 
pela máxima qualidade 
em todos as nossas 
frentes de atuação.
Indicamos caminhos e 
possibilidades para um 
crescimento conjunto.
O crescimento de cada 
Colaborador, Cooperado 
e Parceiro, e também da 
nossa comunidade, é o 
nosso crescimento.PALAVRAS
QUE USAMOS
 Pertencimento;
 Participação;
 Integração;
 Relacionamento;
 Tradição.
 Tecnologia;
 Inovação;
 Excelência;
 Capacitação;
 Cultura.
 Relacionamento;
 Vivência;
 Conhecimento;
 Integridade.
 Parceria;
 Confiança;
 Aprendizado;
 Conexão.PALAVRAS
QUE NÃO USAMOS
Individualismo.
Conformismo;
Comodismo;
Aceitação;
Passividade.
Autoritarismo;
Imposição;
Protagonismo
Individual.
Impossibilidade;
Desinteresse;
Indisponibilidade.Da mesma forma, nossa voz de marca aborda características diversas e 
complementares na construção de seus discursos, conforme o quadro a seguir:
Nossa marca
se expressa
na 1a pessoa
do plural.
Brand Voice
 20 21 Brand Book 2021 Brand Voice



 CONCEITO
Cultura de Qualidade.Cultura de Qualidade é a evolução do nosso já antigo posicionamento de 
marca “Excelência no Agronegócio”. Traduz a nossa busca constante pela 
mais alta qualidade, que se reflete em nossos valores, nossa atuação, nossos 
produtos e serviços. Semanticamente, carrega dualidades de sentido que 
geram percepções de marca proprietárias e positivas: 
 • Cultura enquanto valores e plantio. 
 • Qualidade enquanto excelência e compromisso.
Como expressão, permite que nos apropriemos de todos os nossos diferenciais 
de modo claro e afirmativo: 
 • Cultura de Qualidade em RESULTADOS. 
 • Cultura de Qualidade nos NEGÓCIOS. 
 • Cultura de Qualidade nos RELACIONAMENTOS. 
 • Cultura de Qualidade no ACESSO AO MERCADO. 
 • Cultura de Qualidade para CRESCER MAIS etc.Traduz a
nossa busca
constante pela
mais alta
qualidade.
22 23 Conceito Conceito Brand Book 2021 Holambra Cooperativa Agroindustrial




QUALIDADE.
O que essa palavra representa para você?
Para nós, QUALIDADE representa muita 
coisa.
QUALIDADE representa trajetória.
De um povo que partiu da Holanda rumo ao 
Novo Mundo das Américas e, desde 1960,
chegou pra ficar e se expandir cada vez 
mais pelos campos do Brasil — o celeiro
do mundo.
QUALIDADE representa cooperação.
O nosso modelo de trabalho que une 
pessoas, recursos e esforços 
por um mesmo propósito: produzir riqueza 
e desenvolvimento para todos.
QUALIDADE representa ideal.
Uma busca que se renova a cada processo,decisão e negócio, em que a excelência
de hoje é o parâmetro para que possamos
fazer mais e melhor amanhã. 
QUALIDADE representa o nosso orgulho
de pertencer a uma cooperativa que
trabalha pela prosperidade de cada
produtor e de todo o nosso setor.
Essas qualidades marcam a nossa cultura
e o que cultivamos até aqui.
E representam tudo o que ainda vamos
colher em nossa história.
SOMOS A HOLAMBRA
COOPERATIVA AGROINDUSTRIAL
Cultura de Qualidade.
MANIFESTO
25
 24 Brand Book 2021 Holambra Cooperativa Agroindustrial



 O posicionamento “Cultura de Qualidade”
foi “descolado” da aplicação de marca.
Dessa forma, é possível atrelar a descrição
de atuação da Cooperativa, favorecendo o 
entendimento de suas atividades.O respiro ideal da marca corresponde
à largura de um “H”, sendo fácil
de replicar em qualquer formato.
A proporção da marca é
1 x 4 (3 x 12 subdivididos).
A partir de 3 cm/300 pixels
de largura, devemos excluir o
“Cooperativa Agroindustrial”.Sendo assim, seu tamanho
mínimo de redução é de
1 cm/100 pixels.O moinho poderá ser 
usado como uma forma 
abreviada da assinatura.
3 cm/300px 1 cm/100px 1 cm/75pxAlinhada ao novo 
posicionamento, a tipologia 
da marca apresenta uma nova 
fonte, de formas mais leves, 
mas que ainda expressam 
precisão e tecnologia.
As novas cores trazem equilíbrio 
visual à marca, ao mesmo tempo 
em que solidificam a Cooperativa 
Holambra como Agroindústria.O desenho do moinho
trabalha o contraste 
de luz e sombra, 
conferindo mais volume 
e presença ao símbolo.Arrojado e mais figurativo,
o novo design sedimenta 
o moinho como símbolo 
da cultura holandesa 
que forja a identidade da 
Cooperativa.
O ângulo baixo confere ao 
moinho uma posição imponente 
e elevada. De onde quer que se 
olhe, ele está sempre no topo.ARQUITETURA
x
4xDIFERENCIAIS
Holambra Cooperativa Agroindustrial Brand Book 2021
28 29 Logotipo Logotipo





'''

campanhas = '''
Respeitar o
respiro da marca, 
a largura de um “H”.
A assinatura deve
ser aplicada blocada
pelo Holambra. 
Sempre deve ser escrita
em caixa alta e baixa na fonte 
Gibson Semi-Bold.Sempre aplicar
o ponto-final.APLICAÇÃO GRÁFICA DA ASSINATURA
Cultura de Qualidade.
Cultura de Qualidade.Cultura de Qualidade.Cultura de Qualidade.
Cultura de Qualidade.
CULTURA DE QUALIDADE.Cultura de Qualidade.Não aplicar cores diferentes do logo A cor da assinatura deve ser a mesma do logo
Não utilize fontes light/book/regular
Não utilize caixa alta na assinaturaNão utilize outras famílias de fontes
Não usar a assinatura maior que o logo A priori, não existe uma “regra” que determine em quais situações o nosso posicionamento “Cultura e Qualidade” 
deva ou não deva ser aplicado junto à marca. O mais indicado é que essa avaliação seja feita, caso a caso, pelo 
departamento de marketing e demais áreas envolvidas nas comunicações. Todavia, elencamos a seguir algumas 
situações nas quais entendemos que o uso do posicionamento possa ser mais ou menos indicado.SITUAÇÕES MAIS PERTINENTES
 
 • Campanhas de mídia
  (sobre marcas, produtos, 
  serviços etc.).
 
 • Ações de relacionamento 
  junto a cooperados, parceiros 
  e demais públicos de 
  relacionamento negocial.
 
 • Comunicações institucionais 
  internas, bem como ações
  de fomento ao pertencimento 
  e à cultura, por parte do RH e 
  de áreas parceiras/ correlatas.
 
 • Esforços digitais
  de amplo alcance.
SITUAÇÕES MENOS PERTINENTES:
 
 • Peças institucionais
  de longa vida.
 
 • Posts e inserções
  digitais pontuais.
34 35 Aplicações Aplicações Brand Book 2021 Holambra Cooperativa Agroindustrial

'''


simbolo = '''
SÍMBOLO
Presente desde a primeira versão do nosso logo,
o moinho é o símbolo que representa diretamente a 
herança cultural holandesa e a história da Cooperativa. 
Nesta nova versão, o moinho ganhou um desenho 
renovado, que lhe confere modernidade, dinamismo 
e movimento, de modo a poder representar a marca 
inclusive de maneira isolada.
MAS, ATENÇÃO: 
 •  em casos extremos, o uso do moinho como 
  símbolo pode substituir o logotipo completo;
 • a aplicação do moinho pode ser explorada
  graficamente de forma total ou parcial (cortada),
  desde que o símbolo esteja sempre preenchido;
 • deve-se evitar o uso do moinho em forma outline
  (apenas o contorno do símbolo).Aplicação apenas nas cores primárias.
Proibido o uso nas cores
secundárias e complementares.Não aplicar apenas
como contorno.
36 37 Brand Book 2021 Holambra Cooperativa Agroindustrial Símbolo Símbolo




'''

cores = '''
NOSSAS CORESPRIMÁRIAS
Sob inspiração da bandeira holandesa (assim como na marca original), 
foram selecionados novos tons, constituindo uma paleta de cores 
coerente com o novo posicionamento. O azul, mais fechado e sério, 
tem a intenção de elevar a marca a um padrão mais corporativo e 
industrial. O vermelho (warm red) contrasta com o azul de maneira mais 
equilibrada e harmônica, sem vibração (principalmente quando vista 
em telas, no padrão de cores RGB). Este vermelho, ainda, distancia-se 
dos tons de vermelho tradicionais (magenta 100% / yelow 100%).
Bandeira da Holanda Releitura dos tonsC0 M86 Y63 K0
R239 G51 B64
Pantone 032CC100 M71 Y10 K47
R0 G58 B112
Pantone 654C
C95 M41 Y10 K0
R0 G118 B168
Pantone 7690 CGradiente dos
tons de azulFoi estabelecida, ainda, uma paleta 
secundária, baseada em tons frios (cinzas), 
que dão suporte às cores principais sem 
conflitos de tonalidades. 
C00 M00 Y00 K00
R255 G255 B255
C33 M18 Y13 K40
R124 G135 B142
Pantone 430 CC21 M11 Y9 K23
R162 G170 B173
Pantone 429 C
C65 M43 Y26 K78
R51 G63 B72
Pantone 432 CSECUNDÁRIAS
38 39 Nossas Cores Nossas Cores



Também como cores 
secundárias, recorremos a 
uma maior variedade de tons 
relacionados à marca — porém, 
de uso restrito — que deve 
sempre ser acompanhado 
e aprovado pelo departamento 
de marketing.
C95 M53 Y0 K0
R0 G103 B185
Pantone 2144 C
C60 M9 Y10 K0
R98 G181 B229
Pantone 2915 CC0 M45 Y94 K0
R255 G158 B27
Pantone 1375 C
C65 M0 Y100 K0
R120 G190 B32
Pantone 368 CC75 M0 Y38 K0
R0 G191 B179
Pantone 3262 C
C60 M87 Y5 K0
R122 G65 B131
Pantone 7662 CC2 M13 Y88 K14
R207 G176 B35
Pantone 7752 C
C0 M93 Y79 K0
R228 G0 B43
Pantone 185 CPALETA COMPLEMENTAR:
MISSÃO, VISÃO E VALORESMAPA DE PROPORÇÃO
DO USO DAS CORES
Holambra Cooperativa Agroindustrial Brand Book 2021
40 41 Paleta de Cores Paleta de Cores


'''

degrade = '''
CONSTRUÇÃO DO DEGRADÊ APLICAÇÃO DO DEGRADÊ
Para que as peças tenham a mesma identidade, foi criada 
uma regra na construção do degradê, que deve ser aplicado 
seguindo as orientações ao lado, onde o ponto de transição 
das cores é de 75% da área total.
Sua aplicação deve seguir as instruções abaixo, onde 
primeiro é isolado um quadrado visual, e, na sequência,  
o degradê começa com a parte mais clara a partir do canto 
superior e a mais escura no canto inferior direito.0% 75% 100%
45O45O
45O45O
45O
Degradê aplicado a 180Oponto de transição
Degradê aplicado a -90OCanto invertido Canto invertidoInversão de cores
Holambra Cooperativa Agroindustrial Brand Book 2021
42 43 Paleta de Cores Paleta de Cores


'''

elemento_graf = '''
ELEMENTO
GRÁFICO
Nossa nova marca conta com um elemento 
gráfico extraído de seu próprio símbolo: 
a hélice de pás do moinho. 
Sua forma geométrica pode ser explorada 
de diversas formas, como cortes, 
close-ups e detalhes que ajudam a 
diversificar a comunicação sem perder 
a essência e a unidade visual da própria 
marca. O elemento gráfico também pode ser 
usado em composições com fotos e cores, 
gerando novas formas e combinações. 
A ideia é que este elemento tenha ampla 
liberdade criativa de uso. As aprovações 
de sua aplicação, porém, ficam a critério do 
nosso departamento de marketing.Extraímos a hélice de pás
do moinho para ter um elemento
gráfico proprietário que
fortaleça a comunicação.As versões coloridas só 
podem ser usadas rebaixadas 
em fundo branco. 
A aplicação correta da hélice
é de 45O, podendo ser animada 
(girando) desde que termine
sua rotação na posição inicial.Aplicação apenas nas cores primárias.
Proibido o uso nas cores
secundárias e complementares.Só  a versão branca
pode ser usada rebaixada
em fundo colorido.
Só  a versão branca
pode ser usada rebaixada
em fundo colorido.
44 45 Elementos Gráficos Elementos Gráficos Brand Book 2021 Holambra Cooperativa Agroindustrial

'''

layout = '''
ARQUITETURA DE LAYOUT
A seguir estabeleceremos uma forma de manter a 
proporção da nova marca independentemente do 
seu formato. Seja um folder ou um outdoor, através 
de um cálculo simples, é possível assegurar uma boa 
visibilidade do logo.
Para descobrir o tamanho mínimo em uma arte, 
você deve encontrar a maior área (largura ou altura). 
Feito isso, deve se dividir essa área em cinco 
partes iguais.
Pronto! Assim você garante uma boa visibilidade e os 
materiais ganham sinergia entre si.
Acompanhe ao lado alguns exemplos:maior área = x áreas iguais = x
maior área = xmaior área = xmaior área = x
maior área = xmaior área = x1/5x
1/5x
1/5x1/5x1/5x1/5x
1/5x de larguraATENÇÃO
Essa é uma regra 
elaborada para 
estabelecer um padrão 
mínimo. O logo pode 
ser maior que 1/5
da maior área visual, 
mas nunca menor.
48 49 Elementos Gráficos Elementos Gráficos Brand Book 2021 Holambra Cooperativa Agroindustrial

'''

tipografia = '''

TIPOGRAFIA
Para fortalecer a identidade da 
marca, foi escolhida uma família 
tipográfica com capacidade de se 
ajustar aos mais diversos meios.
Sua flexibilidade, que vai desde uma 
fonte THIN até uma fonte HEAVY, 
permite que sejam explorados 
diversos caminhos gráficos, gerando
diferentes percepções de acordo
com cada necessidade, porém, sem
perder a identidade principal.
Essa tipografia pode ser utilizada 
tanto em caixa alta como baixa, com 
ou sem alteração no espaçamento 
entre letras ou linhas (dependendo 
de cada material).
Gibson Thin Italic
Gibson Book
Gibson Book Italic
Uso preferencial
para textos corridosGibson Medium
Gibson Medium ItalicUso preferencial
para subtítulos
Gibson Bold
Gibson Bold ItalicUso preferencial
para títulosGibson Light
Gibson Light Italic
Gibson Italic
Gibson Regular
Gibson SemiBold
Gibson SemiBold Italic
Gibson Heavy
Gibson Heavy Italic
Holambra Cooperativa Agroindustrial Brand Book 2021
50 51 Tipografia Tipografia


'''

iconografia = '''
LINGUAGEM
ICONOGRÁFICA
O uso de ícones e vetores é muito recorrente na comunicação atual. 
Daí a necessidade de padronizar o estilo gráfico da Cooperativa por 
meio de uma linguagem específica e bem definida.
Diferentemente da marca, que adotou um padrão com mais presença 
e volume no símbolo do moinho, utilizando contraste (luz e sombra), 
a iconografia escolhida trabalha linhas leves, com alto poder  
de síntese — formas simples e de fácil entendimento —, podendo 
auxiliar graficamente quaisquer conteúdos gerados pela marca.
A seguir, exemplificamos a medida-padrão a ser adotada para a 
criação de novos ícones, que deverão ser previamente aprovados 
pelo departamento de marketing.512 px
400 px
stroke 7 pts
(mínimo).512 px
400 px
52 53 Iconografia Brand Book 2021 Holambra Cooperativa Agroindustrial Iconografia

'''


fotografia = '''
LINGUAGEM
FOTOGRÁFICA
A linguagem fotográfica da marca deve refletir o novo 
posicionamento, evidenciando a qualidade em todos os 
aspectos, seja naquilo que ela expressa, seja pela forma 
como foi produzida.
As fotografias usadas para qualquer tipo de 
comunicação devem, sempre que possível, ser bem 
nítidas, contrastantes e saturadas, sem muitos efeitos 
de cor (salvo preto e branco, ou, em alguns casos, 
duotones), para realçar as cores naturais, principalmente 
em paisagens rurais. A utilização de luz natural, pessoas 
reais e retratos verdadeiros aproximam nossos parceiros 
e colaboradores.
As fotos aéreas são muito importantes no universo agro. 
Por isso o cuidado com a nitidez deve ser redobrado.
Holambra Cooperativa Agroindustrial Brand Book 2021
54 55 Fotografia Fotografia
'''

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
