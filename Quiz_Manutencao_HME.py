import streamlit as st
import random
from datetime import datetime
import pandas as pd
import hashlib
import os

# --- Configurações iniciais ---
st.set_page_config(page_title="Quiz Técnico HME", layout="wide")

# Exibe logo
st.image("logo_empresa.png", width=200)  # Substitua pelo nome do seu arquivo de logo

# Caminho fixo para o ranking
RANKING_FILE = os.path.join(os.path.dirname(__file__), "ranking.csv")

# Funções de I/O
def carregar_ranking():
    if os.path.exists(RANKING_FILE):
        return pd.read_csv(RANKING_FILE)
    return pd.DataFrame(columns=["Registro", "Nome", "Turno", "Setor", "Equipamento", "Pontuação", "Porcentagem", "Data"])

def salvar_ranking(df):
    df.to_csv(RANKING_FILE, index=False)

# --- Identificação do colaborador ---
st.title("📊 Quiz Técnico de Manutenção - Frota HME")
st.markdown("---")
st.subheader("🧑‍🔧 Identificação do Colaborador")

nome_usuario = st.text_input("Nome completo:")
registro_interno = st.text_input("Registro interno (código único):")
turno = st.selectbox("Turno:", ["Manhã", "Tarde", "Noite"])
setor = st.text_input("Setor:")
equipamento_foco = st.selectbox(
    "Equipamento de atuação principal:",
    ["LHD ST1030", "Jumbo Boomer S2", "Simbas S7", "Volvo VM360", "Caterpillar 416", "Constellation", "Volvo L120", "JCB 540-170", "Guindaste"]
)

registro_hash = hashlib.sha256((nome_usuario + registro_interno).encode()).hexdigest()

ranking_df = carregar_ranking()
registro_existente = registro_hash in ranking_df["Registro"].values

if nome_usuario and registro_interno:
    if registro_existente:
        st.error("⚠️ Registro duplicado detectado. Quiz já respondido com esses dados.")
    else:
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

        if "respostas" not in st.session_state:
            st.session_state["respostas"] = {}

        total_perguntas = 0
        for bloco in quiz_data:
            st.markdown(f"### 📘 {bloco['equipamento']}")
            for i, pergunta in enumerate(bloco["perguntas"]):
                total_perguntas += 1
                key = f"{bloco['equipamento']}_{i}"
                with st.expander(f"🔧 {pergunta['pergunta']}"):
                    resposta = st.radio("Escolha:", pergunta["alternativas"], key=key)
                    st.session_state["respostas"][key] = resposta

        if st.button("🚀 Enviar Quiz"):
            pontuacao = sum(
                1
                for bloco in quiz_data
                for i, p in enumerate(bloco["perguntas"])
                if st.session_state["respostas"].get(f"{bloco['equipamento']}_{i}") == p["alternativas"][p["correta"]]
            )
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

            # Atualiza ranking
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

            # Exibe ranking top 5
            st.markdown("---")
            st.subheader("🏅 Ranking dos 5 Melhores")
            top5 = ranking_df.sort_values(by="Porcentagem", ascending=False).head(5)
            st.table(top5[["Nome", "Setor", "Pontuação", "Porcentagem", "Data"]])

# --- Administração ---
st.markdown("---")
st.subheader("🔐 Administração")
admin_user = st.text_input("Admin user:")
admin_pass = st.text_input("Password:", type="password")
if admin_user == "admin" and admin_pass == "senha123":
    df = carregar_ranking()
    st.dataframe(df)
else:
    st.info("Login admin para visualizar ranking.")

