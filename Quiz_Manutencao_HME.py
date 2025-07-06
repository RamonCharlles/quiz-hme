import streamlit as st
import random
from datetime import datetime
import pandas as pd
import hashlib

@st.cache_data
def carregar_ranking():
    try:
        return pd.read_csv("ranking.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Registro", "Nome", "Turno", "Setor", "Equipamento", "Pontuação", "Porcentagem", "Data"])

def salvar_ranking(df):
    df.to_csv("ranking.csv", index=False)

ranking_df = carregar_ranking()

st.set_page_config(page_title="Quiz Técnico HME", layout="wide")
# st.image("LOGO PA.png", width=200)  # Desabilitado para evitar erro se não existir
st.title("Quiz Técnico de Manutenção - Frota HME")
st.markdown("---")

st.subheader("Identificação do Colaborador")
nome_usuario = st.text_input("Nome completo:")
registro_interno = st.text_input("Registro interno (código único):")
turno = st.selectbox("Turno:", ["Manhã", "Tarde", "Noite"])
setor = st.text_input("Setor:")
equipamento_foco = st.selectbox("Equipamento de atuação principal:", ["LHD ST1030", "Jumbo Boomer S2", "Simbas S7", "Volvo VM360", "Caterpillar 416", "Constellation", "Volvo L120", "JCB 540-170", "Guindaste"])

registro_hash = hashlib.sha256((nome_usuario + registro_interno).encode()).hexdigest()
registro_existente = registro_hash in ranking_df["Registro"].values

if nome_usuario and registro_interno:
    if registro_existente:
        st.error("⚠️ Já existe um registro com esse nome e código interno. Participação duplicada não é permitida.")
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

        st.session_state.setdefault("respostas", {})

        total_perguntas = 0
        for bloco in quiz_data:
            st.header(f"Equipamento: {bloco['equipamento']}")
            perguntas = bloco["perguntas"]
            for idx, pergunta in enumerate(perguntas):
                total_perguntas += 1
                key_radio = f"{bloco['equipamento']}_pergunta_{idx}"
                resposta = st.radio(pergunta["pergunta"], pergunta["alternativas"], key=key_radio)
                st.session_state["respostas"][key_radio] = resposta

        if st.button("Enviar Quiz"):
            pontuacao = 0
            for bloco in quiz_data:
                perguntas = bloco["perguntas"]
                for idx, pergunta in enumerate(perguntas):
                    key_radio = f"{bloco['equipamento']}_pergunta_{idx}"
                    resposta_usuario = st.session_state["respostas"].get(key_radio)
                    if resposta_usuario:
                        if pergunta["alternativas"].index(resposta_usuario) == pergunta["correta"]:
                            pontuacao += 1

            porcentagem = pontuacao / total_perguntas * 100 if total_perguntas else 0

            st.markdown("---")
            st.subheader("📊 Resultado Final")
            st.write(f"**Pontuação:** {pontuacao} de {total_perguntas}")
            st.write(f"**Percentual de acerto:** {porcentagem:.2f}%")
            st.progress(porcentagem / 100)

            if porcentagem >= 80:
                st.success("Excelente desempenho! 👏")
            elif porcentagem >= 50:
                st.warning("Bom, mas pode melhorar! 💡")
            else:
                st.error("Recomenda-se revisão técnica. 📘")

            nova_linha = pd.DataFrame({
                "Registro": [registro_hash],
                "Nome": [nome_usuario],
                "Turno": [turno],
                "Setor": [setor],
                "Equipamento": [equipamento_foco],
                "Pontuação": [pontuacao],
                "Porcentagem": [porcentagem],
                "Data": [datetime.now().strftime("%Y-%m-%d %H:%M")]
            })
            ranking_df = pd.concat([ranking_df, nova_linha], ignore_index=True)
            salvar_ranking(ranking_df)

st.markdown("---")
st.subheader("🔒 Acesso Administrativo")
admin_user = st.text_input("Usuário administrador:")
admin_pass = st.text_input("Senha:", type="password")

if admin_user == "admin" and admin_pass == "senha123":
    st.success("Acesso concedido ao ranking completo.")
    st.subheader("🏆 Ranking dos 5 Melhores")
    top5 = ranking_df.sort_values(by="Porcentagem", ascending=False).head(5)
    st.dataframe(top5.reset_index(drop=True))

    st.markdown("---")
    st.subheader("📊 Filtros do Dashboard")
    filtro_turno = st.multiselect("Filtrar por Turno:", options=ranking_df["Turno"].unique())
    filtro_setor = st.multiselect("Filtrar por Setor:", options=ranking_df["Setor"].unique())
    filtro_eqp = st.multiselect("Filtrar por Equipamento:", options=ranking_df["Equipamento"].unique())

    df_filtrado = ranking_df.copy()
    if filtro_turno:
        df_filtrado = df_filtrado[df_filtrado["Turno"].isin(filtro_turno)]
    if filtro_setor:
        df_filtrado = df_filtrado[df_filtrado["Setor"].isin(filtro_setor)]
    if filtro_eqp:
        df_filtrado = df_filtrado[df_filtrado["Equipamento"].isin(filtro_eqp)]

    st.dataframe(df_filtrado.reset_index(drop=True))
else:
    st.info("Digite suas credenciais de administrador para visualizar o ranking e o dashboard.")
