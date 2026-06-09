import streamlit as st
# Importa as funções que criamos no arquivo banco.py
from banco import carregar_do_banco, salvar_no_banco

# Inicializa o estado da sessão carregando os dados direto do banco SQLite
if "transacoes" not in st.session_state:
    st.session_state.transacoes = carregar_do_banco()

# --- CONFIGURAÇÃO DA INTERFACE VISUAL ---
st.set_page_config(page_title="Finanças Pessoais", page_icon="💰", layout="centered")

st.title("💰 Gerenciador de Finanças Pessoais")
st.markdown("Controle seus ganhos e gastos armazenados em um Banco de Dados **SQLite**.")
st.divider()

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
        # 1. Salva de verdade no banco de dados SQLite
        salvar_no_banco(tipo, categoria, valor)
        
        # 2. Atualiza a lista da tela atualizando a sessão direto do banco
        st.session_state.transacoes = carregar_do_banco()
        
        st.success(f"{tipo} registrada no banco de dados com sucesso!")
        st.rerun()

st.divider()

# --- EXTRATO E SALDO ---
st.subheader("📊 Extrato e Saldo Atual")

saldo = 0.0
for t in st.session_state.transacoes:
    if t["tipo"] == "Receita":
        saldo += t["valor"]
    else:
        saldo -= t["valor"]

if saldo < 0:
    st.metric(label="Saldo Total", value=f"R$ {saldo:.2f}", delta="Conta no Vermelho!", delta_color="inverse")
else:
    st.metric(label="Saldo Total", value=f"R$ {saldo:.2f}", delta="Estável")

if st.session_state.transacoes:
    st.markdown("**Histórico de Movimentações (Buscado do Banco):**")
    for t in reversed(st.session_state.transacoes):
        cor = "green" if t["tipo"] == "Receita" else "red"
        st.markdown(f":{cor}[[{t['tipo']}]] **{t['categoria']}**: R$ {t['valor']:.2f}")
else:
    st.info("Nenhuma transação registrada no banco de dados ainda.")