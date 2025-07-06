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
    st.image("logo_empresa.png", width=200)
except Exception:
    st.warning("⚠️ Logo não encontrada. Verifique se o arquivo 'logo_empresa.png' está na pasta correta.")

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
turno = st.selectbox("Turno:", ["Dia", "Noite", "Revezamento", "ADM"])
letra = st.selectbox("Letra:", ["ADM", "A", "B", "C", "D"])
setor = st.selectbox("Setor:", [
    "Mecânico HME", "Elétrico HME", "BORRACHARIA",
    "CAUDEIRARIA", "AUXILIAR TÉCNICO HME", "OUTROS"
])
equipamento_foco = st.selectbox("Equipamento de atuação principal:", [
    "LHD ST1030", "Jumbo Boomer S2", "Simbas S7",
    "Volvo VM360", "Caterpillar 416", "Constellation",
    "Volvo L120", "JCB 540-170", "Guindaste"
])

# Validação de número
if registro_interno and not registro_interno.isdigit():
    st.error("❌ Por favor, insira apenas números no registro interno.")
    st.stop()

registro_hash = hashlib.sha256((nome_usuario + registro_interno).encode()).hexdigest()
ranking_df = carregar_ranking()
registro_existente = registro_hash in ranking_df["Registro"].values

if nome_usuario and registro_interno and not registro_existente:

    # --- Quiz com perguntas técnicas ---
    quiz_data = [
        {
            "equipamento": "LHD ST1030",
            "perguntas": [
                {
                    "pergunta": "Quais são os principais parâmetros monitorados pelo sistema RCS durante a operação da ST1030?",
                    "alternativas": [
                        "Temperatura do operador, pressão dos pneus e consumo de combustível",
                        "Pressão do sistema hidráulico, velocidade de deslocamento, carga transportada",
                        "RPM do motor, nível de óleo da transmissão e estado da suspensão",
                        "Abertura da caçamba, tempo de ciclo e rotação das rodas",
                    ],
                    "correta": 1
                },
                {
                    "pergunta": "Como o sistema de freio SAHR atua na LHD ST1030?",
                    "alternativas": [
                        "Libera a frenagem ao aplicar pressão hidráulica",
                        "Aplica frenagem por comando elétrico do operador",
                        "Atua somente em descidas acima de 20% de inclinação",
                        "É um freio auxiliar usado apenas em emergência",
                    ],
                    "correta": 0
                },
            ]
        },
        {
            "equipamento": "Jumbo Boomer S2",
            "perguntas": [
                {
                    "pergunta": "Qual a função do sistema ABC Regular no Boomer S2?",
                    "alternativas": [
                        "Automatizar a perfuração com base em um padrão definido",
                        "Corrigir automaticamente falhas no sistema de ar comprimido",
                        "Regular o consumo de diesel baseado na carga de perfuração",
                        "Manter o alinhamento automático do braço hidráulico",
                    ],
                    "correta": 0
                },
                {
                    "pergunta": "Quais impactos uma calibração incorreta no ABC Regular pode causar?",
                    "alternativas": [
                        "Aumento da vida útil dos sensores",
                        "Perfurações imprecisas e sobrecarga de componentes",
                        "Redução do consumo de combustível",
                        "Desgaste uniforme da barra de perfuração",
                    ],
                    "correta": 1
                },
            ]
        },
    ]

    # Embaralha alternativas na primeira vez
    if "embaralhadas" not in st.session_state:
        st.session_state["embaralhadas"] = {}
        for bloco in quiz_data:
            for i, pergunta in enumerate(bloco["perguntas"]):
                key = f"{bloco['equipamento']}_{i}"
                alternativas = pergunta["alternativas"].copy()
                random.shuffle(alternativas)
                st.session_state["embaralhadas"][key] = alternativas

    if "respostas" not in st.session_state:
        st.session_state["respostas"] = {}

    total_perguntas = 0
    for bloco in quiz_data:
        st.markdown(f"### 📘 {bloco['equipamento']}")
        for i, pergunta in enumerate(bloco["perguntas"]):
            total_perguntas += 1
            key = f"{bloco['equipamento']}_{i}"
            alternativas = st.session_state["embaralhadas"][key]
            with st.expander(f"🔧 {pergunta['pergunta']}", expanded=False):
                resposta = st.radio("Escolha:", alternativas, key=key, index=None)
                st.session_state["respostas"][key] = resposta

    if st.button("🚀 Enviar Quiz"):
        pontuacao = 0
        for bloco in quiz_data:
            for i, pergunta in enumerate(bloco["perguntas"]):
                key = f"{bloco['equipamento']}_{i}"
                resposta_usuario = st.session_state["respostas"].get(key)
                alternativa_correta = pergunta["alternativas"][pergunta["correta"]]
                if resposta_usuario == alternativa_correta:
                    pontuacao += 1

        porcentagem = (pontuacao / total_perguntas * 100) if total_perguntas else 0

        st.markdown("---")
        st.subheader("🎯 Resultado Final")
        st.write(f"**Pontuação:** {pontuacao}/{total_perguntas}")
        st.write(f"**Percentual de Acertos:** {porcentagem:.2f}%")
        st.progress(pontuacao / total_perguntas)

        if porcentagem >= 90:
            st.success("🏆 Excelente! Você demonstrou alto domínio técnico.")
        elif porcentagem >= 70:
            st.info("👏 Bom trabalho! Ainda há espaço para melhorar.")
        elif porcentagem >= 50:
            st.warning("⚠️ Atenção! Revise alguns conceitos.")
        else:
            st.error("❌ Baixo desempenho. Reforço técnico recomendado.")

        # Salva no ranking
        df_atual = carregar_ranking()
        nova_linha_df = pd.DataFrame([{
            "Registro": registro_hash,
            "Nome": nome_usuario,
            "Turno": turno,
            "Setor": setor,
            "Equipamento": equipamento_foco,
            "Pontuação": pontuacao,
            "Porcentagem": porcentagem,
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M")
        }])
        ranking_df = pd.concat([df_atual, nova_linha_df], ignore_index=True)
        salvar_ranking(ranking_df)

        # Exibe top 5
        st.markdown("---")
        st.subheader("🏅 Ranking dos 5 Melhores")
        top5 = ranking_df.sort_values(by="Porcentagem", ascending=False).head(5)
        st.table(top5[["Nome", "Setor", "Pontuação", "Porcentagem", "Data"]])

elif nome_usuario and registro_existente:
    st.error("⚠️ Registro duplicado detectado. Quiz já foi respondido com esses dados.")

# --- Administração ---
st.markdown("---")
st.subheader("🔐 Administração")
admin_user = st.text_input("Admin user:")
admin_pass = st.text_input("Password:", type="password")
if admin_user == "Ramon.Silva" and admin_pass == "PAGOLD672":
    df = carregar_ranking()
    st.dataframe(df)
    if st.button("🗑️ Zerar Ranking"):
        zerar_ranking()
        st.success("✅ Ranking zerado com sucesso.")



    if st.button("🗑️ Zerar Ranking"):
        zerar_ranking()
        st.success("Ranking zerado com sucesso!")
else:
    st.info("Login admin para visualizar ranking.")
