import streamlit as st
from docxtpl import DocxTemplate, RichText
from io import BytesIO
from datetime import datetime
import os

# --- FUNÇÃO PARA DATA EM PORTUGUÊS (FUNCIONA EM QUALQUER PC) ---
def get_data_ptbr():
    meses = {
        1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
        5: "maio", 6: "junho", 7: "julho", 8: "agosto",
        9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
    }
    hoje = datetime.now()
    return f"{hoje.day} de {meses[hoje.month]} de {hoje.year}"

# --- CONFIGURAÇÃO VISUAL ---
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

# --- 🔒 SISTEMA DE LOGIN ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if st.session_state.password_correct:
        return True
    
    st.title("🔒 Acesso Restrito - CTA/SEAD")
    senha_digitada = st.text_input("Digite a senha de acesso:", type="password")
    if st.button("Entrar"):
        try:
            senha_secreta = st.secrets["password"]
        except:
            senha_secreta = "sead123" 
            
        if senha_digitada == senha_secreta:  
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
    return False

if not check_password():
    st.stop()

st.title("⚖️ Sistema de Pareceres CTA/SEAD")

# 1. BANCO DE DADOS - PESSOAL
lista_estagiarios = {
    "GUILHERME MOREIRA MEDEIROS": {"cargo": "Estagiário de Direito – CTA/SEAD"},
    "GERLANE CORREA DA SILVA": {"cargo": "Estagiária de Direito – CTA/SEAD"},
    "JULLIA AYUMI TAKANO BARROS": {"cargo": "Estagiária de Direito – CTA/SEAD"}
}

lista_assessores = {
    "ANDREW MAFRA DE SOUZA": {"cargo": "Assessor Jurídico", "info": "Matrícula n.º 270.303-3A"},
    "CINTIA NASCIMENTO DE SOUZA": {"cargo": "Assessora – CTA/SEAD", "info": "OAB/AM nº 12.376"},
    "INGRID C. DE SÁ R. PACHECO BANDEIRA DE MELO": {"cargo": "Assessora – CTA/SEAD", "info": "OAB/AM nº 12.209"},
    "LAURA GLORIA REBELO": {"cargo": "Assessora – CTA/SEAD", "info": "OAB/AM nº 16.391"},
    "MARINA LINDOSO DE CASTRO": {"cargo": "Assessora – CTA/SEAD", "info": "OAB/AM nº 5.616"},
    "MAURA SPOSITO ANTONY": {"cargo": "Assessora Jurídica – CTA/SEAD", "info": "OAB/AM n.º 6.624"}
}

# 2. HIERARQUIA E CARGOS
oficiais_generico = ["Coronel", "Tenente-Coronel", "Major", "Capitão", "1º Tenente", "2º Tenente"]
oficiais_saude = ["Major", "Capitão", "1º Tenente", "2º Tenente"]
oficiais_saude_cb = ["Coronel", "Tenente-Coronel", "Major", "Capitão", "1º Tenente", "2º Tenente"]
pracas_lista = ["Subtenente", "1º Sargento", "2º Sargento", "3º Sargento", "Cabo", "Soldado"]

cargos_medicos = ["Médico (Graduado)", "Médico (Especialista)", "Médico (Mestre)", "Médico (Doutor)"]

cargos_demais_saude = [
    "Administrador", "Advogado", "Analista de Sistemas", "Arquiteto", "Assistente Social",
    "Bacharel em Computação", "Bibliotecário", "Biólogo", "Cirurgião Dentista", "Comunicador Social",
    "Contador", "Economista", "Enfermeiro", "Engenheiro Ambiental", "Engenheiro Civil",
    "Engenheiro Eletricista", "Epidemiologista", "Estatístico", "Farmacêutico", "Farmacêutico Bioquímico",
    "Físico em Medicina", "Fisioterapeuta", "Fonoaudiólogo", "Geógrafo", "Médico Veterinário",
    "Nutricionista", "Pedagogo", "Pesquisador", "Pesquisador Adjunto", "Pesquisador Assistente",
    "Pesquisador Iniciante", "Pesquisador Titular", "Psicólogo", "Químico", "Sanitarista",
    "Sociólogo", "Técnico", "Terapeuta Ocupacional"
]

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
    },
    "SES": {
        "Médicos": {p: p for p in cargos_medicos},
        "Demais Profissionais": {p: p for p in cargos_demais_saude}
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
    },
    "SES": {
        "Médicos": "Quadro de Médicos da SES",
        "Demais Profissionais": "Quadro de Profissionais de Saúde da SES"
    }
}

mapa_porcentagem = {
    "25%": "25% (vinte e cinco por cento)",
    "30%": "30% (trinta por cento)",
    "35%": "35% (trinta e cinco por cento)"
}

locais_ses = {
    "Secretaria de Estado de Saúde - SES": "SES",
    "Fundação de Hematologia e Hemoterapia do Amazonas - FHEMOAM": "FHEMOAM",
    "Fundação de Medicina Tropical do Amazonas - FMT/AM": "FMT/AM",
    "Fundação de Dermatologia Tropical e Venereologia Alfredo da Matta - FUAHM": "FUAHM",
    "Fundação Centro de Controle de Oncologia - FCECON": "FCECON",
    "Fundação Hospital Adriano Jorge - FHAJ": "FHAJ",
    "Fundação de Vigilância em Saúde - FVS": "FVS"
}

# --- INTERFACE GRÁFICA ---
aba1, aba2, aba3 = st.tabs(["🏢 Instituição", "📝 Dados do Parecer", "🖋️ Assinaturas"])

with aba1:
    st.subheader("Selecione a Carreira")
    c1, c2, c3 = st.columns(3)
    with c1: orgao_sel = st.selectbox("Órgão:", list(hierarquia_postos.keys()))
    with c2: quadro_sel = st.selectbox("Quadro:", list(hierarquia_postos[orgao_sel].keys()))
    with c3: posto_sel = st.selectbox("Cargo/Classe:", list(hierarquia_postos[orgao_sel][quadro_sel].keys()))

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
    
    sel_lotacao_completa = ""
    if orgao_sel == "SES":
        st.markdown("##### 🏥 Dados Específicos SES")
        sel_lotacao_completa = st.selectbox("Lotação:", list(locais_ses.keys()))

    st.markdown("---")
    nome = st.text_input("Interessado (MAIÚSCULAS):")
    col_m, col_p = st.columns(2)
    with col_m: mat = st.text_input("Matrícula:")
    with col_p: proc = st.text_input("Nº SIGED:")

    col_cur, col_car = st.columns([2, 1])
    with col_cur: 
        curso = st.text_input("Nome do Curso (Ex: Saúde Pública):")
    with col_car: 
        carga = st.text_input("Carga Horária (Ex: 408h):")

    superior_pertinencia = st.text_input("Quem atestou a pertinência? (Ex: Diretora de Vigilância Hospitalar):")

    col_data, col_porc = st.columns(2)
    with col_data:
        data_req = st.text_input("Data do Requerimento:")
    with col_porc:
        sel_porc = st.selectbox("Percentual da Gratificação:", ["25%", "30%", "35%"])
        texto_porcentagem = mapa_porcentagem.get(sel_porc, sel_porc)

    genero = st.selectbox("Gênero:", ["Masculino", "Feminino"])
    
    if genero == "Masculino":
        artigo, pronome, tratamento, interessado, demandante, autor = "pelo", "ele", "O servidor", "O Interessado", "do Demandante", "do autor"
        termo_servidor = "servidor"
        termo_requerente = "o requerente"
        termo_do_servidor = "do servidor"
    else:
        artigo, pronome, tratamento, interessado, demandante, autor = "pela", "ela", "A servidora", "A Interessada", "da Demandante", "da autora"
        termo_servidor = "servidora"
        termo_requerente = "a requerente"
        termo_do_servidor = "da servidora"
    
    st.markdown("##### ⚠️ Condicionantes do Parecer")
    c_legit = st.checkbox("Condicionar Legitimidade? (Certificado/Histórico)")
    c_ident = st.checkbox("Juntar documento de identidade?")

    resumo = "" 
    if orgao_sel != "SES":
        resumo = st.text_area("Conclusão Técnica (Recuo 4cm):", height=150)

with aba3:
    st.subheader("Finalização")
    col_e, col_as = st.columns(2)
    with col_e: sel_est = st.selectbox("Estagiário(a):", list(lista_estagiarios.keys()))
    with col_as: sel_ass = st.selectbox("Assessor(a):", list(lista_assessores.keys()))

    st.markdown("---")
    
    # --- LÓGICA DE SELEÇÃO DO MODELO WORD ---
    if orgao_sel == "SES":
        if quadro_sel == "Médicos":
            nome_modelo = "modelo_SES_MEDICO.docx"
        else:
            nome_modelo = "modelo_SES_OUTROS.docx"
    else:
        nome_modelo = f"modelo_{orgao_sel}.docx"
    
    caminho_modelo = os.path.join(os.getcwd(), nome_modelo)
    
    if os.path.exists(caminho_modelo):
        st.success(f"Modelo selecionado: {nome_modelo}")
    else:
        st.error(f"Erro: Modelo {nome_modelo} não encontrado na pasta.")

    botao = st.button("🚀 GERAR PARECER", type="primary")

# --- GERAÇÃO DO DOCUMENTO ---
if botao:
    if not os.path.exists(caminho_modelo):
        st.error("Erro técnico: O arquivo de modelo não está na pasta.")
    else:
        try:
            doc = DocxTemplate(caminho_modelo)
            p_word = hierarquia_postos[orgao_sel][quadro_sel][posto_sel]
            q_extenso = nomes_quadros_extenso[orgao_sel][quadro_sel]
            
            # --- LÓGICA SES INTELIGENTE ---
            lei_regencia = ""
            alinea_medico = "X"
            citacao_lei_formatada = ""
            tipo_pos_graduacao = "Pós-Graduação Lato Sensu"
            sigla_lotacao = ""
            
            if orgao_sel == "SES":
                sigla_lotacao = locais_ses.get(sel_lotacao_completa, "")
                
                txt_a = "a) Curso de Especialista: 25% (vinte e cinco por cento);"
                txt_b = "b) Curso de Mestrado: 30% (trinta por cento);"
                txt_c = "c) Curso de Doutorado: 35% (trinta e cinco por cento)."
                
                # Tipo de Pós
                if "25%" in sel_porc: 
                    tipo_pos_graduacao = "Pós-Graduação Lato Sensu"
                elif "30%" in sel_porc:
                    tipo_pos_graduacao = "Pós-Graduação Stricto Sensu, Mestrado em"
                elif "35%" in sel_porc:
                    tipo_pos_graduacao = "Pós-Graduação Stricto Sensu, Doutorado em"
                else:
                    tipo_pos_graduacao = "Pós-Graduação Lato Sensu"

                # >>> LÓGICA PARA MÉDICOS (Lei 70)
                if quadro_sel == "Médicos":
                    lei_regencia = "Lei Promulgada nº 70, de 14 de julho de 2009"
                    
                    if "25%" in sel_porc: alinea_medico = "a"
                    elif "30%" in sel_porc: alinea_medico = "b"
                    elif "35%" in sel_porc: alinea_medico = "c"
                    else: alinea_medico = "a"

                # >>> LÓGICA PARA OUTROS PROFISSIONAIS (Lei 3.469)
                else: 
                    lei_regencia = "Lei nº 3.469, de 24 de dezembro de 2009"
                    
                    if "25%" in sel_porc: alinea_medico = "a"
                    elif "30%" in sel_porc: alinea_medico = "b"
                    elif "35%" in sel_porc: alinea_medico = "c"
                    else: alinea_medico = "a"
                
                # >>> GERAÇÃO DO RICHTEXT (Negrito na Alínea Correta)
                rt = RichText()
                if "25%" in sel_porc: rt.add(f"{txt_a} [grifo nosso]\n", font='Arial', bold=True)
                else: rt.add(f"{txt_a}\n", font='Arial')
                
                if "30%" in sel_porc: rt.add(f"{txt_b} [grifo nosso]\n", font='Arial', bold=True)
                else: rt.add(f"{txt_b}\n", font='Arial')
                
                if "35%" in sel_porc: rt.add(f"{txt_c} [grifo nosso]", font='Arial', bold=True) 
                else: rt.add(f"{txt_c}", font='Arial')
                
                citacao_lei_formatada = rt 

            # --- CONDICIONANTES COM NEGRITO E ARIAL 10 (RICHTEXT) ---
            txt_cond_legitimidade = ""
            if c_legit:
                rt_legit = RichText()
                # size=20 equivale a 10pt no Word
                rt_legit.add("A concessão da benesse pleiteada ficará condicionada à ", font='Arial', size=20)
                rt_legit.add("legitimidade do Certificado e do Histórico Escolar", font='Arial', size=20, bold=True)
                rt_legit.add(". A veracidade e autenticidade dos dados ali contidos deverão ser atestadas pela "
                             "Instituição de Ensino Superior responsável pela emissão dos referidos documentos, recaindo sobre está a "
                             "responsabilidade pela confirmação das informações. O Órgão concedente, por sua vez, ficará responsável "
                             "pela verificação dessa chancela institucional.", font='Arial', size=20)
                txt_cond_legitimidade = rt_legit

            txt_cond_identidade = ""
            if c_ident:
                rt_ident = RichText()
                rt_ident.add("Ressalte-se, por oportuno, que a efetiva concessão e a consequente implementação "
                             "financeira da Gratificação de Curso encontram-se igualmente condicionadas à imprescindível ", font='Arial', size=20)
                # Usa a tag termo_do_servidor
                rt_ident.add(f"juntada de cópia legível do documento de identidade oficial {termo_do_servidor}", font='Arial', size=20, bold=True)
                rt_ident.add(" aos autos, providência que se configura como requisito formal indispensável para a correta qualificação "
                             "do interessado e para a segurança jurídica do ato administrativo, devendo tais pendências serem saneadas "
                             "antes do desfecho final do processo.", font='Arial', size=20)
                txt_cond_identidade = rt_ident
            
            dados = {
                "NUM_PARECER": f"{num_parecer}/{ano_parecer}",
                "PARECER_DCT": num_p_dct, "PARECER_AJAI": num_p_ajai,
                "NOME": nome, "MATRICULA": mat, "POSTO": p_word, "QUADRO": q_extenso,
                "CURSO": curso, "CARGA_HORARIA": carga, "PROCESSO": proc, "DATA_REQ": data_req,
                "ARTIGO": artigo, "ELE": pronome, "TRATAMENTO": tratamento, 
                "INTERESSADO": interessado, "DEMANDANTE": demandante,
                "AUTOR": autor,
                "SERVIDOR": termo_servidor,
                "DO_SERVIDOR": termo_do_servidor, 
                "REQUERENTE": termo_requerente,
                "LEI": lei_regencia,
                "ALINEA": alinea_medico,
                "LOTACAO": sel_lotacao_completa,
                "SIGLA": sigla_lotacao,
                "SUPERIOR_PERTINENCIA": superior_pertinencia,
                "PORCENTAGEM": texto_porcentagem,
                "CITACAO_LEI": citacao_lei_formatada,
                "TIPO_POS": tipo_pos_graduacao,
                "CONDICAO_LEGITIMIDADE": txt_cond_legitimidade,
                "CONDICAO_IDENTIDADE": txt_cond_identidade,
                "RESUMO_DCT": resumo, "EU": sel_est, 
                "MEU_CARGO": lista_estagiarios[sel_est]["cargo"],
                "ASSINANTE_DIREITA": sel_ass, 
                "CARGO_DIREITA": lista_assessores[sel_ass]["cargo"],
                "INFO_DIREITA": lista_assessores[sel_ass]["info"],
                "COORDENADOR": "DANILO ALBERTO GRACIANO DE ALBURQUEQUE", 
                "COORD_CARGO": "Coordenador - CTA/SEAD", "COORD_OAB": "OAB/AM n.º 14.661",
                "DIA_ATUAL": get_data_ptbr()
            }
            
            doc.render(dados)
            buf = BytesIO()
            doc.save(buf)
            buf.seek(0)
            
            # --- NOME DO ARQUIVO PERSONALIZADO ---
            # 1. Trata o Número do Parecer (Se vazio, vira XXX)
            num_arq = num_parecer if num_parecer.strip() else "XXX"
            
            # 2. Trata o Processo (Troca / por -)
            proc_limpo = proc.replace("/", "-").replace("\\", "-")
            
            # 3. Trata a Sigla (Usa a lotação para SES ou o Órgão para os outros)
            if orgao_sel == "SES" and sigla_lotacao:
                sigla_arq = sigla_lotacao
            else:
                sigla_arq = orgao_sel
            
            # 4. Monta o Nome Final
            nome_arquivo = f"Parecer nº {num_arq}.{ano_parecer}-Proc.nº {proc_limpo} ({sigla_arq})- {nome} (Grat. de Curso).docx"
            
            st.success(f"Parecer de {nome} gerado com sucesso!")
            st.download_button("📥 Baixar Parecer", buf, nome_arquivo)
            
        except Exception as e:
            st.error(f"Erro: {e}")