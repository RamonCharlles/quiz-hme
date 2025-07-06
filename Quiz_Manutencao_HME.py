import streamlit as st
import random
from datetime import datetime
import pandas as pd
import hashlib
import os

# --- Configurações iniciais ---
st.set_page_config(page_title="Quiz Técnico HME", layout="wide")

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
st.title("Quiz Técnico de Manutenção - Frota HME")
st.markdown("---")
st.subheader("Identificação do Colaborador")

nome_usuario = st.text_input("Nome completo:")
registro_interno = st.text_input("Registro interno (código único):")
turno = st.selectbox("Turno:", ["Manhã", "Tarde", "Noite"])
setor = st.text_input("Setor:")
equipamento_foco = st.selectbox(
    "Equipamento de atuação principal:",
    ["LHD ST1030", "Jumbo Boomer S2", "Simbas S7", "Volvo VM360", "Caterpillar 416", "Constellation", "Volvo L120", "JCB 540-170", "Guindaste"]
)

# Gera hash único
registro_hash = hashlib.sha256((nome_usuario+registro_interno).encode()).hexdigest()

# Carrega ranking atual
ranking_df = carregar_ranking()
registro_existente = registro_hash in ranking_df["Registro"].values

if nome_usuario and registro_interno:
    if registro_existente:
        st.error("⚠️ Registro duplicado detectado. Quiz já respondido com esses dados.")
    else:
        # --- Quiz ---
        quiz_data = [
            # adicione blocos completos aqui
        ]
        # inicializa sessão
        if "respostas" not in st.session_state:
            st.session_state["respostas"] = {}

        total_perguntas = 0
        for bloco in quiz_data:
            st.header(bloco["equipamento"])
            for i, pergunta in enumerate(bloco["perguntas"]):
                total_perguntas += 1
                key = f"{bloco['equipamento']}_{i}"
                st.session_state.setdefault(key, None)
                resposta = st.radio(pergunta["pergunta"], pergunta["alternativas"], key=key)

        if st.button("Enviar Quiz"):
            pontuacao = sum(
                1 for bloco in quiz_data for i, p in enumerate(bloco["perguntas"]) 
                if st.session_state[f"{bloco['equipamento']}_{i}"] == p["alternativas"][p["correta"]]
            )
            porcentagem = pontuacao/total_perguntas*100 if total_perguntas else 0

            st.markdown("---")
            st.subheader("Resultado Final")
            st.write(f"Pontuação: {pontuacao}/{total_perguntas}")
            st.write(f"Percentual: {porcentagem:.2f}%")

            # atualiza ranking
            ranking_df = carregar_ranking()  # recarrega sempre
            nova_linha = {
                "Registro": registro_hash,
                "Nome": nome_usuario,
                "Turno": turno,
                "Setor": setor,
                "Equipamento": equipamento_foco,
                "Pontuação": pontuacao,
                "Porcentagem": porcentagem,
                "Data": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            ranking_df = ranking_df.append(nova_linha, ignore_index=True)
            salvar_ranking(ranking_df)

# --- Admin ---
st.markdown("---")
st.subheader("Administração")
user = st.text_input("Admin user:")
psw = st.text_input("Password:", type="password")
if user=="admin" and psw=="senha123":
    df = carregar_ranking()
    st.dataframe(df)
else:
    st.info("Login admin para visualizar ranking.")
