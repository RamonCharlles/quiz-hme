import streamlit as st
import random
from datetime import datetime
import pandas as pd
import hashlib
import os

# --- Configurações iniciais ---
st.set_page_config(page_title="Quiz Técnico HME", layout="wide")

# Exibe logo com proteção
try:
    st.image("logo_empresa.png", width=200) # Comentado: Remova o comentário se tiver o arquivo local
    st.markdown("<!-- Substitua esta linha por st.image('caminho/para/sua/logo.png', width=200) -->")
except Exception:
    st.warning("⚠️ Logo não encontrada. Verifique se o arquivo 'logo_empresa.png' está na pasta correta ou remova a linha de imagem.")

# Caminho fixo para o ranking
RANKING_FILE = os.path.join(os.path.dirname(__file__), "ranking.csv")

# Funções de I/O
def carregar_ranking():
    if os.path.exists(RANKING_FILE):
        return pd.read_csv(RANKING_FILE)
    return pd.DataFrame(columns=["Registro", "Nome", "Turno", "Setor", "Equipamento", "Pontuação", "Porcentagem", "Data"])

def salvar_ranking(df):
    df.to_csv(RANKING_FILE, index=False)

def zerar_ranking():
    salvar_ranking(pd.DataFrame(columns=["Registro", "Nome", "Turno", "Setor", "Equipamento", "Pontuação", "Porcentagem", "Data"]))

# --- Identificação do colaborador ---
st.title("📊 Quiz Técnico de Manutenção - Frota HME")
st.markdown("---")
st.subheader("🧑‍🔧 Identificação do Colaborador")

nome_usuario = st.text_input("Nome completo:")
registro_interno = st.text_input("Registro interno (código único):")
turno_selecionado = st.selectbox("Turno:", ["ADM", "A", "B", "C", "D"]) # Renomeado para evitar conflito
setor = st.text_input("Setor:")
equipamento_foco = st.selectbox(
    "Equipamento de atuação principal:",
    ["LHD ST1030", "Jumbo Boomer S2", "Simbas S7", "Volvo VM360", "Caterpillar 416", "Constellation", "Volvo L120", "JCB 540-170", "Guindaste", "Outros Sistemas/Geral"]
) # Adicionado "Outros Sistemas/Geral" para focar nas perguntas mais amplas

# Gerar hash para o registro (para evitar duplicações por nome/registro)
registro_hash = hashlib.sha256((nome_usuario + registro_interno).encode()).hexdigest()

ranking_df = carregar_ranking()
registro_existente = registro_hash in ranking_df["Registro"].values

# --- Seção de Acesso ao Ranking Protegida por Senha ---
st.markdown("---")
st.subheader("🔒 Acesso ao Ranking de Participantes")
senha_ranking = st.text_input("Digite a senha para visualizar o ranking:", type="password", key="senha_ranking_input")

if senha_ranking: # Verifica se algo foi digitado na senha
    if senha_ranking == "admin123": # Senha correta
        st.success("Acesso liberado ao ranking completo.")
        if not ranking_df.empty:
            st.dataframe(ranking_df)
            if st.button("🔴 Zerar Ranking (Ação Irreversível)", key="zerar_ranking_btn"):
                zerar_ranking()
                st.success("Ranking zerado com sucesso!")
                st.experimental_rerun() # Recarrega a página para mostrar o ranking vazio
        else:
            st.info("Nenhum resultado registrado ainda.")
    else: # Senha incorreta
        st.error("Senha incorreta.")
# --- Fim da Seção de Acesso ao Ranking ---

# --- Definição das Perguntas do Quiz ---
# Este é o banco de perguntas atualizado, baseado nas suas últimas solicitações
# e no formato do novo script.
quiz_data_completo = {
    "LHD ST1030": [
        {
            "pergunta": "Quais são os principais parâmetros monitorados pelo sistema RCS (Sistema de Controle e Monitoramento) durante a operação da ST1030 para otimizar a produtividade e segurança?",
            "alternativas": [
                "Temperatura do operador, pressão dos pneus e consumo de combustível.",
                "Pressão do sistema hidráulico, velocidade de deslocamento, carga transportada e status dos freios.",
                "RPM do motor, nível de óleo da transmissão e estado da suspensão.",
                "Abertura da caçamba, tempo de ciclo e rotação das rodas."
            ],
            "correta": 1,
            "explicacao": "O RCS monitora parâmetros operacionais críticos como pressão hidráulica, velocidade e carga para garantir operação eficiente e segura, alertando sobre condições anormais."
        },
        {
            "pergunta": "Como o sistema de freio SAHR (Spring Applied, Hydraulically Released) atua na LHD ST1030 e qual sua principal característica de segurança?",
            "alternativas": [
                "Libera a frenagem ao aplicar pressão hidráulica e aplica por molas na perda de pressão, garantindo segurança contra falhas.",
                "Aplica frenagem por comando elétrico do operador e libera por molas.",
                "Atua somente em descidas acima de 20% de inclinação e é liberado por pressão de ar.",
                "É um freio auxiliar usado apenas em emergência e não possui mecanismo de segurança contra falha hidráulica."
            ],
            "correta": 0,
            "explicacao": "O SAHR é um sistema 'fail-safe': as molas mantêm os freios aplicados por padrão. A pressão hidráulica é necessária para liberá-los. Em caso de perda de pressão, os freios são automaticamente aplicados, aumentando a segurança."
        },
        {
            "pergunta": "Qual a consequência mais grave de uma falha no sistema de direção articulada da ST1030 durante a operação em rampa?",
            "alternativas": [
                "Aumento do consumo de combustível.",
                "Perda de controle direcional, risco de colisão ou tombamento.",
                "Desgaste prematuro dos pneus dianteiros.",
                "Ativação automática do sistema de combate a incêndio."
            ],
            "correta": 1,
            "explicacao": "A direção articulada é vital para o controle da máquina. Sua falha, especialmente em rampas, pode levar à perda total de controle, com consequências graves para a segurança."
        }
    ],
    "Jumbo Boomer S2": [
        {
            "pergunta": "Qual a função primária do sistema ABC Regular no Jumbo Boomer S2 e como ele contribui para a eficiência da perfuração?",
            "alternativas": [
                "Automatizar a perfuração com base em um padrão definido (plano de fogo), otimizando a precisão e o tempo de ciclo.",
                "Corrigir automaticamente falhas no sistema de ar comprimido, garantindo a continuidade da perfuração.",
                "Regular o consumo de diesel baseado na carga de perfuração, visando economia de combustível.",
                "Manter o alinhamento automático do braço hidráulico em relação ao solo, independentemente da inclinação."
            ],
            "correta": 0,
            "explicacao": "O ABC Regular automatiza o ciclo de perfuração seguindo um plano pré-definido, o que melhora a precisão dos furos e reduz o tempo de perfuração, aumentando a produtividade."
        },
        {
            "pergunta": "Quais impactos uma calibração incorreta no ABC Regular pode causar na operação do Jumbo Boomer S2?",
            "alternativas": [
                "Aumento da vida útil dos sensores e componentes eletrônicos.",
                "Perfurações imprecisas (desvio de furos), sobrecarga de componentes e redução da vida útil das brocas e hastes.",
                "Redução do consumo de combustível e menor emissão de poluentes.",
                "Desgaste uniforme da barra de perfuração e maior estabilidade do equipamento."
            ],
            "correta": 1,
            "explicacao": "Uma calibração incorreta do ABC Regular compromete a precisão da perfuração, levando a desvios que podem danificar as ferramentas, sobrecarregar o equipamento e, em última instância, impactar a segurança e a produtividade."
        },
        {
            "pergunta": "Como a tecnologia de perfuração 'face drilling' (perfuração de frente) é otimizada pelo Boomer S2 e qual seu benefício principal?",
            "alternativas": [
                "Utiliza apenas brocas de grande diâmetro para perfurações rápidas.",
                "Permite perfurar múltiplos furos em um padrão preciso e simultâneo, reduzindo o tempo de ciclo e otimizando o desmonte.",
                "Foca na perfuração vertical para instalação de cabos de sustentação.",
                "É um método exclusivo para perfuração de rochas muito macias, sem a necessidade de explosivos."
            ],
            "correta": 1,
            "explicacao": "O Boomer S2 é projetado para perfuração de frente, onde furos são feitos em padrões específicos para otimizar a fragmentação da rocha após a detonação, resultando em desmontes mais eficientes e seguros."
        }
    ],
    "Simbas S7": [], # Adicione perguntas específicas para Simbas S7 aqui, se desejar
    "Volvo VM360": [], # Adicione perguntas específicas para Volvo VM360 aqui, se desejar
    "Caterpillar 416": [], # Adicione perguntas específicas para Caterpillar 416 aqui, se desejar
    "Constellation": [], # Adicione perguntas específicas para Constellation aqui, se desejar
    "Volvo L120": [], # Adicione perguntas específicas para Volvo L120 aqui, se desejar
    "JCB 540-170": [], # Adicione perguntas específicas para JCB 540-170 aqui, se desejar
    "Guindaste": [], # Adicione perguntas específicas para Guindaste aqui, se desejar
    "Outros Sistemas/Geral": [ # Perguntas gerais de manutenção, elétrica e outros sistemas
        {
            "pergunta": "Um equipamento tem um MTTR (Tempo Médio para Reparo) alto. Qual das seguintes situações é a causa mais provável?",
            "alternativas": [
                "As inspeções preventivas não estão sendo feitas corretamente.",
                "O almoxarifado não possui peças de reposição críticas em estoque.",
                "O operador está utilizando o equipamento de forma agressiva.",
                "O equipamento está operando em um ambiente com muita poeira."
            ],
            "correta": 1,
            "explicacao": "A ausência de peças essenciais prolonga diretamente o período em que a máquina fica parada, aguardando o componente para o reparo."
        },
        {
            "pergunta": "Para aumentar o MTBF (Tempo Médio Entre Falhas) de uma carregadeira ST1030, qual seria a ação mais eficaz?",
            "alternativas": [
                "Contratar mais mecânicos para a equipe de manutenção.",
                "Implementar um plano de manutenção preventiva mais rigoroso, com trocas de componentes baseadas no tempo de uso.",
                "Comprar ferramentas de diagnóstico mais modernas para a oficina.",
                "Manter um estoque maior de peças de reposição."
            ],
            "correta": 1,
            "explicacao": "A manutenção preventiva atua para corrigir problemas antes que eles causem uma parada, aumentando o tempo de operação contínua entre as falhas."
        },
        {
            "pergunta": "A equipe de manutenção percebe que as mangueiras hidráulicas das ST1030 estão rompendo muito antes do tempo de vida esperado. Qual é a causa raiz mais provável a ser investigada primeiro?",
            "alternativas": [
                "Falta de treinamento da equipe de manutenção em reparos hidráulicos.",
                "A pressão de trabalho do sistema hidráulico pode estar desregulada e acima do especificado.",
                "O manual técnico do equipamento está desatualizado.",
                "O almoxarifado não tem as abraçadeiras corretas em estoque."
            ],
            "correta": 1,
            "explicacao": "Uma pressão excessiva no sistema força os componentes, como mangueiras, a trabalharem além do seu limite de projeto, causando falhas prematuras."
        },
        {
            "pergunta": "Qual é a relação correta entre MTBF, MTTR e a Disponibilidade de um equipamento?",
            "alternativas": [
                "Para aumentar a Disponibilidade, devemos aumentar tanto o MTBF quanto o MTTR.",
                "A Disponibilidade não tem relação direta com MTBF e MTTR.",
                "Para aumentar a Disponibilidade, devemos diminuir o MTBF e aumentar o MTTR.",
                "Para aumentar a Disponibilidade, devemos aumentar o MTBF e diminuir o MTTR."
            ],
            "correta": 3,
            "explicacao": "A máxima disponibilidade é alcançada quando o equipamento funciona pelo maior tempo possível (alto MTBF) e, quando falha, é consertado o mais rápido possível (baixo MTTR)."
        },
        {
            "pergunta": "Um mantenedor recebe um chamado de que uma carregadeira parou de funcionar. Qual deve ser o primeiro passo ao chegar na máquina?",
            "alternativas": [
                "Verificar o nível do óleo hidráulico e do motor.",
                "Começar a desmontar o componente que apresentou a última falha.",
                "Conversar com o operador para entender os sintomas e o que aconteceu antes da falha.",
                "Requisitar imediatamente as peças que mais costumam falhar para este modelo."
            ],
            "correta": 2,
            "explicacao": "O operador é a principal fonte de informação. Entender os sintomas (ruídos, perda de força, alarmes) é crucial para guiar o diagnóstico de forma eficiente."
        },
        {
            "pergunta": "O principal objetivo de um programa de Manutenção Preventiva é:",
            "alternativas": [
                "Consertar os equipamentos o mais rápido possível após a quebra.",
                "Reduzir a probabilidade de falhas e o desgaste dos componentes.",
                "Documentar todas as falhas que ocorrem nos equipamentos.",
                "Reduzir o custo das peças de reposição compradas."
            ],
            "correta": 1,
            "explicacao": "A manutenção preventiva atua proativamente para manter o equipamento em condições ideais, trocando peças e fazendo ajustes para evitar paradas inesperadas."
        },
        {
            "pergunta": "Várias carregadeiras ST1030 estão apresentando falhas intermitentes no sistema elétrico, principalmente em sensores. Qual é a solução de longo prazo mais eficaz?",
            "alternativas": [
                "Substituir o sensor defeituoso sempre que a falha ocorrer.",
                "Treinar os operadores para não forçar o sistema elétrico.",
                "Realizar uma análise para proteger melhor os chicotes e conectores contra umidade e vibração.",
                "Manter um grande estoque de todos os tipos de sensores."
            ],
            "correta": 2,
            "explicacao": "Problemas intermitentes em sensores são frequentemente causados por mau contato ou danos em chicotes e conectores. Melhorar a proteção ataca a causa raiz."
        },
        {
            "pergunta": "Qual indicador de manutenção mede o tempo médio que um equipamento opera sem apresentar nenhuma falha que necessite de reparo?",
            "alternativas": [
                "MTTR (Mean Time To Repair)",
                "Disponibilidade",
                "MTBF (Mean Time Between Failures)",
                "Backlog"
            ],
            "correta": 2,
            "explicacao": "MTBF mede especificamente o tempo médio de operação de um equipamento entre uma falha e a próxima."
        },
        {
            "pergunta": "A falta de acesso a manuais técnicos e diagramas claros durante um reparo impacta negativamente qual indicador?",
            "alternativas": [
                "MTTR (Tempo Médio para Reparo)",
                "MTBF (Tempo Médio Entre Falhas)",
                "Custo de Peças",
                "Vida útil do equipamento"
            ],
            "correta": 0,
            "explicacao": "A dificuldade em encontrar informações técnicas leva a um diagnóstico mais lento e a um processo de reparo mais demorado, aumentando o tempo total da máquina parada."
        },
        {
            "pergunta": "A gestão identifica que a causa principal do baixo MTBF é o uso de peças de reposição de baixa qualidade. Qual seria a decisão gerencial mais correta?",
            "alternativas": [
                "Aumentar a frequência das inspeções preventivas.",
                "Homologar fornecedores e comprar apenas peças originais ou de qualidade comprovada, mesmo que mais caras.",
                "Treinar a equipe para fazer os reparos mais rapidamente.",
                "Culpar a equipe de manutenção pelos reparos que não duram."
            ],
            "correta": 1,
            "explicacao": "Atacar a causa raiz requer uma mudança na política de compras, priorizando a qualidade e a durabilidade para garantir que os reparos sejam mais duradouros."
        },
        # Perguntas de sistemas gerais (já existentes no script anterior)
        {
            "pergunta": "Em um sistema de combate a incêndio automático para HME, além dos sensores de calor, qual outro tipo de sensor pode ser crucial para uma detecção precoce e confiável em ambientes com poeira e vibração?",
            "alternativas": [
                "Sensores de umidade.",
                "Sensores de pressão atmosférica.",
                "Sensores de fumaça e/ou detecção de chamas por infravermelho/UV.",
                "Sensores de nível de combustível."
            ],
            "correta": 2,
            "explicacao": "Em ambientes HME, a detecção de chamas por infravermelho/UV ou fumaça pode complementar os sensores de calor, oferecendo uma resposta mais rápida a diferentes tipos de incêndio, especialmente em locais de difícil acesso ou com rápida propagação."
        },
        {
            "pergunta": "Qual a principal vantagem de um sistema de lubrificação centralizada progressiva em uma escavadeira de grande porte, comparado à lubrificação manual?",
            "alternativas": [
                "Redução do consumo de combustível em 15%.",
                "Eliminação total da necessidade de inspeções visuais nos pontos de lubrificação.",
                "Lubrificação precisa e contínua dos pontos críticos durante a operação, reduzindo o desgaste e aumentando a disponibilidade.",
                "Aumento da velocidade de deslocamento da máquina em terrenos irregulares."
            ],
            "correta": 2,
            "explicacao": "Sistemas centralizados garantem que cada ponto receba a quantidade correta de lubrificante no tempo certo, mesmo com a máquina em operação, minimizando o desgaste e maximizando o tempo de atividade sem paradas para lubrificação manual."
        },
        {
            "pergunta": "No sistema Common Rail de um motor a diesel HME, qual a função do sensor de pressão do rail e qual o impacto de sua falha?",
            "alternativas": [
                "Medir a temperatura do combustível e ajustar a rotação do motor.",
                "Monitorar a pressão do óleo lubrificante e ativar o modo de segurança.",
                "Medir a pressão do combustível no rail para que a ECU controle a injeção; sua falha pode causar perda de potência ou parada do motor.",
                "Controlar a abertura das válvulas de admissão e escape."
            ],
            "correta": 2,
            "explicacao": "O sensor de pressão do rail é vital para o controle preciso da injeção. Uma leitura incorreta ou sua falha impede que a ECU module a injeção corretamente, resultando em problemas de desempenho ou falha total do motor."
        },
        {
            "pergunta": "Em um sistema hidráulico de um caminhão fora de estrada, qual a função primordial do trocador de calor (radiador de óleo hidráulico) e o que acontece se ele falhar?",
            "alternativas": [
                "Aumentar a viscosidade do óleo para melhorar a vedação.",
                "Filtrar partículas contaminantes do óleo hidráulico.",
                "Resfriar o óleo hidráulico para manter sua viscosidade e propriedades; sua falha leva ao superaquecimento e degradação do óleo.",
                "Aquecer o óleo hidráulico para melhor fluxo em baixas temperaturas."
            ],
            "correta": 2,
            "explicacao": "O trocador de calor dissipa o calor gerado no sistema hidráulico. Sua falha causa superaquecimento, que degrada rapidamente o óleo (perda de viscosidade e aditivos), danificando bombas, válvulas e cilindros."
        },
        {
            "pergunta": "Qual o procedimento correto para a calibração de pneus em veículos pesados de mineração e qual o risco de fazê-la com pneus quentes?",
            "alternativas": [
                "Medir a pressão apenas com o veículo em movimento e ajustar para o máximo da especificação.",
                "Calibrar a qualquer temperatura, pois o calor não afeta a leitura.",
                "Realizar a calibração com pneus frios, seguindo a especificação do fabricante; pneus quentes resultam em leitura superestimada e subcalibragem.",
                "Calibrar sempre acima da pressão recomendada para maior segurança."
            ],
            "correta": 2,
            "explicacao": "A pressão interna do pneu aumenta com o calor. Calibrar pneus quentes usando a tabela de pressão a frio resultará em uma pressão real abaixo do ideal quando o pneu esfriar, causando desgaste irregular e maior consumo de combustível."
        },
        {
            "pergunta": "Ao descartar fluidos e resíduos perigosos (ex: óleos usados, filtros contaminados) de equipamentos HME, qual a prática mais adequada e em conformidade com a legislação ambiental?",
            "alternativas": [
                "Despejar em qualquer terreno baldio ou rede de esgoto para descarte rápido.",
                "Queimar os resíduos para reduzir seu volume e impacto.",
                "Armazenar em recipientes apropriados e identificados, e enviar para empresas de tratamento ou reciclagem autorizadas por órgãos ambientais.",
                "Enterrar os resíduos em valas para que se decomponham naturalmente."
            ],
            "correta": 2,
            "explicacao": "O descarte inadequado de resíduos perigosos causa contaminação do solo e da água, além de resultar em multas e sanções legais. A prática correta é a destinação final por empresas especializadas e licenciadas."
        },
        {
            "pergunta": "No programa 7S (ou 5S estendido), qual 'S' é responsável por criar um ambiente de trabalho onde a disciplina e a padronização das boas práticas são mantidas ao longo do tempo?",
            "alternativas": [
                "Seiri (Senso de Utilização).",
                "Seiton (Senso de Organização).",
                "Shitsuke (Senso de Autodisciplina/Manutenção).",
                "Seiketsu (Senso de Padronização)."
            ],
            "correta": 2,
            "explicacao": "Shitsuke é o 'S' da autodisciplina, garantindo que os hábitos e padrões estabelecidos pelos outros 'S' sejam seguidos consistentemente por todos, tornando-os parte da cultura da equipe."
        },
        {
            "pergunta": "Qual a principal função do alternador em um equipamento HME e o que acontece se ele falhar durante a operação?",
            "alternativas": [
                "Apenas armazenar energia para a partida do motor.",
                "Converter energia mecânica do motor em energia elétrica para carregar a bateria e alimentar todos os sistemas elétricos; sua falha leva ao esgotamento da bateria e parada do equipamento.",
                "Controlar a temperatura do motor através da circulação de refrigerante.",
                "Filtrar impurezas do combustível antes da injeção."
            ],
            "correta": 1,
            "explicacao": "O alternador é o gerador de energia elétrica do veículo. Se ele falha, a bateria não é recarregada e os sistemas elétricos param de funcionar à medida que a carga da bateria se esgota, levando à parada do equipamento."
        },
        {
            "pergunta": "Em grandes motores elétricos de HME, qual o principal benefício da utilização de um sistema de partida estrela-triângulo?",
            "alternativas": [
                "Aumentar o torque inicial do motor para partidas mais rápidas.",
                "Reduzir a corrente de partida (pico de corrente) e o estresse mecânico no motor e na rede elétrica.",
                "Diminuir a velocidade máxima de operação do motor para maior segurança.",
                "Aumentar o consumo de energia durante a partida para aquecer o motor."
            ],
            "correta": 1,
            "explicacao": "A partida estrela-triângulo reduz a tensão aplicada aos enrolamentos do motor durante a partida, o que diminui a corrente de pico e o torque inicial, protegendo o motor e a infraestrutura elétrica contra sobrecargas."
        },
        {
            "pergunta": "Em um sistema elétrico de HME, um dispositivo de proteção contra fuga de corrente elétrica (como um DR ou RCD) atua principalmente para proteger contra qual tipo de falha e qual o risco associado?",
            "alternativas": [
                "Sobrecarga de corrente em um circuito, protegendo os cabos contra superaquecimento.",
                "Curto-circuito fase-fase, evitando danos aos componentes elétricos.",
                "Fuga de corrente para a terra, protegendo pessoas contra choques elétricos e prevenindo incêndios causados por falhas de isolamento.",
                "Subtensão, garantindo que os equipamentos recebam a voltagem mínima necessária."
            ],
            "correta": 2,
            "explicacao": "Dispositivos DR (Diferencial Residual) são essenciais para a segurança, detectando pequenas correntes que 'fogem' do circuito normal para a terra, indicando um risco de choque elétrico ou incêndio, e desarmando rapidamente."
        },
        {
            "pergunta": "Em equipamentos HME modernos, qual a principal finalidade do barramento de comunicação CAN (Controller Area Network) e como ele melhora o diagnóstico de falhas?",
            "alternativas": [
                "Transmitir apenas sinais de áudio e vídeo para o operador.",
                "Conectar fisicamente os componentes mecânicos do motor para maior robustez.",
                "Permitir a comunicação digital bidirecional e eficiente entre diferentes módulos de controle eletrônico (ECUs), facilitando o diagnóstico de falhas e a interação entre sistemas.",
                "Gerar energia elétrica para os sistemas de iluminação e segurança."
            ],
            "correta": 2,
            "explicacao": "O CAN bus é a espinha dorsal da comunicação eletrônica em HME, permitindo que ECUs de motor, transmissão, freios, etc., compartilhem dados. Isso é crucial para o diagnóstico, pois falhas em um sistema podem ser rapidamente identificadas e correlacionadas com outros."
        },
        {
            "pergunta": "A perfuratriz Epiroc COP 1838MUX+ é reconhecida por sua capacidade de perfurar rochas de alta dureza. Qual tecnologia de martelo de perfuração contribui significativamente para essa capacidade?",
            "alternativas": [
                "Martelo de fundo (DTH) com sistema de ar comprimido de baixa pressão.",
                "Martelo de superfície com tecnologia de impacto hidráulico de alta frequência e energia.",
                "Martelo elétrico com sistema de vibração de baixa intensidade.",
                "Martelo pneumático com acionamento manual."
            ],
            "correta": 1,
            "explicacao": "A COP 1838MUX+ utiliza um martelo de superfície com tecnologia hidráulica avançada que gera alta frequência e energia de impacto, permitindo a perfuração eficiente mesmo em rochas muito duras."
        }
    ]
}

# Lógica para selecionar perguntas com base no equipamento de foco
perguntas_selecionadas = []
if equipamento_foco in quiz_data_completo and equipamento_foco != "Outros Sistemas/Geral":
    perguntas_selecionadas.extend(quiz_data_completo[equipamento_foco])
    # Se houver menos de 10 perguntas específicas, complementa com perguntas gerais
    if len(perguntas_selecionadas) < 10:
        perguntas_gerais_disponiveis = [q for q in quiz_data_completo["Outros Sistemas/Geral"] if q not in perguntas_selecionadas]
        random.shuffle(perguntas_gerais_disponiveis)
        perguntas_selecionadas.extend(perguntas_gerais_disponiveis[:(10 - len(perguntas_selecionadas))])
elif equipamento_foco == "Outros Sistemas/Geral":
    # Se o foco for "Outros Sistemas/Geral", seleciona 10 perguntas aleatórias dessa categoria
    perguntas_selecionadas.extend(random.sample(quiz_data_completo["Outros Sistemas/Geral"], min(10, len(quiz_data_completo["Outros Sistemas/Geral"]))))
else:
    # Caso o equipamento não tenha perguntas específicas e não seja "Outros Sistemas/Geral",
    # pega 10 perguntas aleatórias da categoria "Outros Sistemas/Geral" como fallback
    random.shuffle(quiz_data_completo["Outros Sistemas/Geral"])
    perguntas_selecionadas.extend(quiz_data_completo["Outros Sistemas/Geral"][:10])

random.shuffle(perguntas_selecionadas) # Embaralha as perguntas selecionadas final

if nome_usuario and registro_interno and not registro_existente:
    st.markdown("---")
    st.subheader(f"📝 Quiz para {nome_usuario} ({equipamento_foco})")
    
    modo_treinamento = st.checkbox("🧪 Ativar modo treinamento (com dicas extras)", value=True)

    with st.form("quiz_form"):
        score = 0
        respostas_usuario = []
        total_perguntas_quiz = len(perguntas_selecionadas)

        for idx, pergunta_obj in enumerate(perguntas_selecionadas):
            with st.expander(f"Questão {idx + 1}. {pergunta_obj['pergunta']}", expanded=True):
                # Embaralha as alternativas para cada pergunta
                alternativas_embaralhadas = random.sample(pergunta_obj['alternativas'], len(pergunta_obj['alternativas']))
                
                resposta_selecionada = st.radio(
                    "Escolha:", 
                    alternativas_embaralhadas, 
                    key=f"q_{equipamento_foco}_{idx}"
                )
                st.session_state[f"q_{equipamento_foco}_{idx}"] = resposta_selecionada # Armazena a resposta na session_state

                # Adiciona a resposta selecionada, a correta e a explicação para a lista de respostas do usuário
                respostas_usuario.append({
                    "pergunta": pergunta_obj['pergunta'],
                    "resposta_usuario": resposta_selecionada,
                    "resposta_correta": pergunta_obj['alternativas'][pergunta_obj['correta']],
                    "explicacao": pergunta_obj['explicacao']
                })

                if modo_treinamento:
                    st.info(f"💡 Dica: {pergunta_obj['explicacao'].split('.')[0]}.")

        submit = st.form_submit_button("✅ Enviar Respostas")

        if submit:
            for resp_info in respostas_usuario:
                if resp_info["resposta_usuario"] == resp_info["resposta_correta"]:
                    score += 1

            porcentagem = (score / total_perguntas_quiz * 100) if total_perguntas_quiz else 0
            
            st.markdown("---")
            st.subheader("🎯 Resultado Final")
            st.write(f"**Pontuação:** {score}/{total_perguntas_quiz}")
            st.write(f"**Percentual de Acertos:** {porcentagem:.2f}%")
            st.progress(score / total_perguntas_quiz)

            if porcentagem >= 90:
                st.success("🏆 Excelente! Você demonstrou alto domínio técnico.")
            elif porcentagem >= 70:
                st.info("👏 Bom trabalho! Ainda há espaço para melhorar.")
            elif porcentagem >= 50:
                st.warning("⚠️ Atenção! Revise alguns conceitos.")
            else:
                st.error("❌ Baixo desempenho. Reforço técnico recomendado.")

            # Atualiza ranking
            df_atual = carregar_ranking()
            nova_linha_df = pd.DataFrame([{  
                "Registro": registro_hash,
                "Nome": nome_usuario,
                "Turno": turno_selecionado, # Usando a variável corrigida
                "Setor": setor,
                "Equipamento": equipamento_foco,
                "Pontuação": score,
                "Porcentagem": porcentagem,
                "Data": datetime.now().strftime("%Y-%m-%d %H:%M")
            }])
            ranking_df = pd.concat([df_atual, nova_linha_df], ignore_index=True)
            salvar_ranking(ranking_df)

            st.markdown("## 📘 Explicações de Cada Questão")
            for i, resp_info in enumerate(respostas_usuario):
                cor = "✅" if resp_info["resposta_usuario"] == resp_info["resposta_correta"] else "❌"
                st.markdown(f"**{i+1}. {resp_info['pergunta']}**\n\n{cor} Sua resposta: *{resp_info['resposta_usuario']}* — Resposta correta: *{resp_info['resposta_correta']}*\n\n> {resp_info['explicacao']}")

else:
    if not nome_usuario or not registro_interno:
        st.info("🔒 Por favor, preencha seu nome completo e registro interno para iniciar o quiz.")
    elif registro_existente:
        st.error("⚠️ Registro duplicado detectado. Quiz já respondido com esses dados. Por favor, utilize um registro diferente ou contate o administrador.")
