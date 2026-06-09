import streamlit as st
import banco

# Garante que as tabelas existem no início
banco.conectar_banco()

# Inicializa as variáveis de controle de sessão do usuário
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario_id" not in st.session_state:
    st.session_state.usuario_id = None
if "usuario_nome" not in st.session_state:
    st.session_state.usuario_nome = ""

st.set_page_config(page_title="Finanças Pessoais", page_icon="💰", layout="centered")

# --- TELA DE LOGIN / CADASTRO ---
if not st.session_state.logado:
    st.title("🔑 Acesso ao Sistema")
    
    aba_login, aba_cadastro = st.tabs(["Entrar", "Criar Conta"])
    
    with aba_login:
        st.subheader("Login")
        usuario_login = st.text_input("Usuário", key="login_user")
        senha_login = st.text_input("Senha", type="password", key="login_pass")
        
        if st.button("Entrar", use_container_width=True):
            user_id = banco.verificar_login(usuario_login, senha_login)
            if user_id:
                st.session_state.logado = True
                st.session_state.usuario_id = user_id
                st.session_state.usuario_nome = usuario_login.strip().capitalize()
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
                
    with aba_cadastro:
        st.subheader("Nova Conta")
        usuario_cad = st.text_input("Escolha um Nome de Usuário", key="cad_user")
        senha_cad = st.text_input("Escolha uma Senha", type="password", key="cad_pass")
        
        if st.button("Cadastrar", use_container_width=True):
            if usuario_cad.strip() == "" or senha_cad.strip() == "":
                st.warning("Preencha todos os campos.")
            elif len(senha_cad) < 4:
                st.warning("A senha deve ter pelo menos 4 caracteres.")
            else:
                if banco.criar_usuario(usuario_cad, senha_cad):
                    st.success("Conta criada com sucesso! Faça login na aba ao lado.")
                else:
                    st.error("Este nome de usuário já está em uso.")

# --- TELA PRINCIPAL DO SISTEMA (APÓS LOGIN) ---
else:
    # Cabeçalho com o nome do usuário e botão de sair
    col_user, col_logout = st.columns([4, 1])
    with col_user:
        st.title(f"Olá, {st.session_state.usuario_nome}! 👋")
    with col_logout:
        if st.button("Sair", use_container_width=True):
            st.session_state.logado = False
            st.session_state.usuario_id = None
            st.session_state.usuario_nome = ""
            st.rerun()
            
    st.markdown("Controle seus ganhos e gastos de forma privada e segura.")
    st.divider()

    # Carrega os dados específicos deste usuário
    transacoes = banco.carregar_do_banco(st.session_state.usuario_id)

    # --- FORMULÁRIO DE CADASTRO ---
    st.subheader("➕ Nova Transação")
    col1, col2, col3 = st.columns(3)

    with col1:
        tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
    with col2:
        categoria = st.text_input("Categoria", placeholder="Ex: Salário, Mercado")
    with col3:
        valor = st.number_input("Valor (R$)", min_value=0.0, step=5.0, format="%.2f")

    if st.button("Registrar Transação", use_container_width=True):
        if categoria.strip() == "" or valor <= 0:
            st.error("Por favor, preencha a categoria e insira um valor maior que zero.")
        else:
            banco.salvar_no_banco(st.session_state.usuario_id, tipo, categoria, valor)
            st.success(f"{tipo} registrada com sucesso!")
            st.rerun()

    st.divider()

    # --- EXTRATO E SALDO ---
    st.subheader("📊 Seu Extrato e Saldo")

    saldo = 0.0
    for t in transacoes:
        if t["tipo"] == "Receita":
            saldo += t["valor"]
        else:
            saldo -= t["valor"]

    if saldo < 0:
        st.metric(label="Saldo Total", value=f"R$ {saldo:.2f}", delta="Conta no Vermelho!", delta_color="inverse")
    else:
        st.metric(label="Saldo Total", value=f"R$ {saldo:.2f}", delta="Estável")

    if transacoes:
        st.markdown("**Histórico de Movimentações:**")
        for t in reversed(transacoes):
            cor = "green" if t["tipo"] == "Receita" else "red"
            st.markdown(f":{cor}[[{t['tipo']}]] **{t['categoria']}**: R$ {t['valor']:.2f}")
    else:
        st.info("Você ainda não possui transações cadastradas.")