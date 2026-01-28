import streamlit as st
from docxtpl import DocxTemplate
from io import BytesIO
from datetime import datetime
import locale
import os
import time

# Configuração de data
try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except:
    pass

def add_bg():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://img.freepik.com/fotos-gratis/cimento-de-textura-cinza-grunge_53876-95555.jpg?semt=ais_hybrid&w=740&q=80");
             background-attachment: fixed;
             background-size: cover;
         }}
         .stTabs [data-baseweb="tab-list"] {{
             gap: 10px;
             background-color: rgba(255, 255, 255, 0.5);
             padding: 10px;
             border-radius: 10px;
         }}
         /* Estilo para a tela de login */
         .stTextInput input {{
             background-color: rgba(255, 255, 255, 0.9);
         }}
         .block-container {{
             background-color: rgba(255, 255, 255, 0.9);
             border-radius: 15px;
             padding: 3rem !important;
             box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
             margin-top: 2rem;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg()

# --- 🔒 SISTEMA DE LOGIN (NOVIDADE) ---
def check_password():
    """Retorna True se o usuário tiver a senha correta."""
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    st.title("🔒 Acesso Restrito - CTA/SEAD")
    st.markdown("Este sistema é de uso exclusivo interno.")
    
    senha = st.text_input("Digite a senha de acesso:", type="password")
    
    if st.button("Entrar"):
        # DEFINA SUA SENHA AQUI (Ex: "sead")
        if senha == "paralelepipedo":  
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
    return False

if not check_password():
    st.stop()  # Para a execução aqui se não tiver logado

# --- 🔓 SE PASSOU DAQUI, MOSTRA O SISTEMA ---

st.title("⚖️ Sistema de Pareceres CTA/SEAD")

# 1. BANCO DE DADOS
lista_estagiarios = {
    "GUILHERME MOREIRA MEDEIROS": {"cargo": "Estagiário de Direito – CTA/SEAD"},
    "GERLANE CORREA DA SILVA": {"cargo": "Estagiária de Direito – CTA/SEAD"},
    "JULLIA AYUMÉ TAKANO BARROS": {"cargo": "Estagiária de Direito – CTA/SEAD"}
}

lista_assessores = {
    "ANDREW MAFRA DE SOUZA": {"cargo": "Assessor Jurídico", "info": "Matrícula n.º 270.303-3A"},
    "CINTIA NASCIMENTO DE SOUZA": {"cargo": "Assessora – CTA/SEAD", "info": "OAB/AM nº 12.376"},
    "INGRID C. DE SÁ R. PACHECO BANDEIRA DE MELO": {"cargo": "Assessora – CTA/SEAD", "info": "OAB/AM nº 12.209"},
    "LAURA GLORIA REBELO": {"cargo": "Assessora – CTA/SEAD", "info": "OAB/AM nº 16.391"},
    "MARINA LINDOSO DE CASTRO": {"cargo": "Assessora – CTA/SEAD", "info": "OAB/AM nº 5.616"},
    "MAURA SPOSITO ANTONY": {"cargo": "Assessora Jurídica – CTA/SEAD", "info": "OAB/AM n.º 6.624"}
}

# 2. HIERARQUIA
oficiais_generico = ["Coronel", "Tenente-Coronel", "Major", "Capitão", "1º Tenente", "2º Tenente"]
oficiais_saude = ["Major", "Capitão", "1º Tenente", "2º Tenente"]
oficiais_saude_cb = ["Coronel", "Tenente-Coronel", "Major", "Capitão", "1º Tenente", "2º Tenente"]
pracas_lista = ["Subtenente", "1º Sargento", "2º Sargento", "3º Sargento", "Cabo", "Soldado"]

hierarquia_postos = {
    "PMAM": {
        "Oficiais Combatentes": {p: p for p in oficiais_generico},
        "Praças Combatentes": {p: p for p in pracas_lista},
        "Saúde": {p: p for p in oficiais_saude},
        "Administração": {p: p for p in ["Capitão", "1º Tenente", "2º Tenente"]}
    },
    "CBMAM": {
        "Oficiais Combatentes": {p: p for p in oficiais_generico},
        "Quadro Complementar (Médico)": {p: p for p in oficiais_saude_cb},
        "Quadro Complementar (Enfermeiro)": {p: p for p in oficiais_saude_cb},
        "Quadro Complementar (Dentista)": {p: p for p in oficiais_saude_cb},
        "Quadro Complementar (Farmacêutico)": {p: p for p in oficiais_saude_cb},
        "Quadro Complementar (Assistente Social)": {p: p for p in oficiais_saude_cb},
        "Oficiais Adm": {p: p for p in oficiais_saude_cb},
        "Praças Combatentes": {p: p for p in pracas_lista},
        "Praças Complementares": {p: p for p in pracas_lista}
    },
    "PCAM": {
        "Servidores": {"Delegado": "Delegado", "Investigador": "Investigador", "Escrivão": "Escrivão", "Perito": "Perito"}
    }
}

nomes_quadros_extenso = {
    "PMAM": {
        "Oficiais Combatentes": "Quadro de Oficiais Policiais Militares (QOPM)",
        "Praças Combatentes": "Quadro de Praças Policiais Militares (QPPM)",
        "Saúde": "Quadro de Oficiais de Saúde (QOS)",
        "Administração": "Quadro de Oficiais de Administração (QOA)"
    },
    "CBMAM": {
        "Oficiais Combatentes": "Quadro de Oficiais Combatentes",
        "Quadro Complementar (Médico)": "Quadro Complementar de Oficiais (Médico)",
        "Quadro Complementar (Enfermeiro)": "Quadro Complementar de Oficiais (Enfermeiro)",
        "Quadro Complementar (Dentista)": "Quadro Complementar de Oficiais (Dentista)",
        "Quadro Complementar (Farmacêutico)": "Quadro Complementar de Oficiais (Farmacêutico)",
        "Quadro Complementar (Assistente Social)": "Quadro Complementar de Oficiais (Assistente Social)",
        "Oficiais Adm": "Quadro de Oficiais de Administração",
        "Praças Combatentes": "Quadro de Praças Combatentes",
        "Praças Complementares": "Quadro Complementar de Praças"
    },
    "PCAM": {
        "Servidores": "Quadro de Servidores da Polícia Civil"
    }
}

# --- INTERFACE ---
aba1, aba2, aba3 = st.tabs(["🏢 Instituição", "📝 Dados do Parecer", "🖋️ Assinaturas"])

with aba1:
    st.subheader("Selecione a Carreira")
    c1, c2, c3 = st.columns(3)
    with c1: orgao_sel = st.selectbox("Órgão:", list(hierarquia_postos.keys()))
    with c2: quadro_sel = st.selectbox("Quadro:", list(hierarquia_postos[orgao_sel].keys()))
    with c3: posto_sel = st.selectbox("Posto/Graduação:", list(hierarquia_postos[orgao_sel][quadro_sel].keys()))

with aba2:
    st.subheader(f"Informações - {orgao_sel}")
    col_n, col_a = st.columns([2, 1])
    with col_n: num_parecer = st.text_input("Nº Parecer SEAD:")
    with col_a: ano_parecer = st.text_input("Ano:", value=str(datetime.now().year))

    num_p_dct, num_p_ajai = "", ""
    if orgao_sel == "PMAM":
        c_d, c_a = st.columns(2)
        with c_d: num_p_dct = st.text_input("Nº Parecer DCT:")
        with c_a: num_p_ajai = st.text_input("Nº Parecer AJAI:")

    st.markdown("---")
    nome = st.text_input("Interessado (MAIÚSCULAS):")
    col_m, col_p = st.columns(2)
    with col_m: mat = st.text_input("Matrícula:")
    with col_p: proc = st.text_input("Nº SIGED:")

    col_cur, col_car = st.columns([2, 1])
    with col_cur: curso = st.text_input("Nome do Curso:")
    with col_car: carga = st.text_input("Carga Horária:")

    data_req = st.text_input("Data do Requerimento:")
    genero = st.selectbox("Gênero:", ["Masculino", "Feminino"])
    
    if genero == "Masculino":
        artigo, pronome, tratamento, interessado, demandante, autor = "pelo", "ele", "O servidor", "O Interessado", "do Demandante", "do autor"
    else:
        artigo, pronome, tratamento, interessado, demandante, autor = "pela", "ela", "A servidora", "A Interessada", "da Demandante", "da autora"
    
    resumo = st.text_area("Conclusão Técnica (Recuo 4cm):", height=150)

with aba3:
    st.subheader("Finalização")
    col_e, col_as = st.columns(2)
    with col_e: sel_est = st.selectbox("Estagiário(a):", list(lista_estagiarios.keys()))
    with col_as: sel_ass = st.selectbox("Assessor(a):", list(lista_assessores.keys()))

    st.markdown("---")
    nome_modelo = f"modelo_{orgao_sel}.docx"
    caminho_modelo = os.path.join(os.getcwd(), nome_modelo)
    
    if os.path.exists(caminho_modelo):
        st.success(f"Modelo {nome_modelo} pronto.")
    else:
        st.error(f"Erro: Modelo {nome_modelo} não encontrado.")

    botao = st.button("🚀 GERAR PARECER", type="primary")

if botao:
    if not os.path.exists(caminho_modelo):
        st.error("Erro técnico: O arquivo de modelo não está na pasta.")
    else:
        try:
            doc = DocxTemplate(caminho_modelo)
            p_word = hierarquia_postos[orgao_sel][quadro_sel][posto_sel]
            q_extenso = nomes_quadros_extenso[orgao_sel][quadro_sel]
            
            dados = {
                "NUM_PARECER": f"{num_parecer}/{ano_parecer}",
                "PARECER_DCT": num_p_dct, "PARECER_AJAI": num_p_ajai,
                "NOME": nome, "MATRICULA": mat, "POSTO": p_word, "QUADRO": q_extenso,
                "CURSO": curso, "CARGA_HORARIA": carga, "PROCESSO": proc, "DATA_REQ": data_req,
                "ARTIGO": artigo, "ELE": pronome, "TRATAMENTO": tratamento, 
                "INTERESSADO": interessado, "DEMANDANTE": demandante,
                "AUTOR": autor,
                "RESUMO_DCT": resumo, "EU": sel_est, 
                "MEU_CARGO": lista_estagiarios[sel_est]["cargo"],
                "ASSINANTE_DIREITA": sel_ass, 
                "CARGO_DIREITA": lista_assessores[sel_ass]["cargo"],
                "INFO_DIREITA": lista_assessores[sel_ass]["info"],
                "COORDENADOR": "DANILO ALBERTO GRACIANO DE ALBURQUEQUE", 
                "COORD_CARGO": "Coordenador - CTA/SEAD", "COORD_OAB": "OAB/AM n.º 14.661",
                "DIA_ATUAL": datetime.now().strftime("%d de %B de %Y")
            }
            
            doc.render(dados)
            buf = BytesIO()
            doc.save(buf)
            buf.seek(0)
            st.success(f"Parecer de {nome} gerado com sucesso!")
            st.download_button("📥 Baixar Parecer", buf, f"Parecer_{orgao_sel}_{nome}.docx")
        except Exception as e:
            st.error(f"Erro: {e}")