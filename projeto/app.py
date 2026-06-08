import streamlit as st
import json
import os

# Usaremos um arquivo JSON diferente para a versão web para não misturar os testes
ARQUIVO_DADOS = "financas_web.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_dados(transacoes):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(transacoes, f, indent=4, ensure_ascii=False)

# Garante que os dados fiquem salvos na memória da página enquanto ela roda
if "transacoes" not in st.session_state:
    st.session_state.transacoes = carregar_dados()

# --- CONFIGURAÇÃO DA INTERFACE VISUAL ---
st.set_page_config(page_title="Finanças Pessoais", page_icon="💰", layout="centered")

st.title("💰 Gerenciador de Finanças Pessoais")
st.markdown("Controle seus ganhos e gastos com uma interface web moderna e limpa.")
st.divider()

# --- FORMULÁRIO DE CADASTRO ---
st.subheader("➕ Nova Transação")

# Divide a tela em 3 colunas para os campos ficarem lado a lado
col1, col2, col3 = st.columns(3)

with col1:
    tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
with col2:
    categoria = st.text_input("Categoria", placeholder="Ex: Salário, Mercado")
with col3:
    valor = st.number_input("Valor (R$)", min_value=0.0, step=5.0, format="%.2f")

# Botão para cadastrar
if st.button("Registrar Transação", use_container_width=True):
    if categoria.strip() == "" or valor <= 0:
        st.error("Por favor, preencha a categoria e insira um valor maior que zero.")
    else:
        nova_transacao = {"tipo": tipo, "categoria": categoria, "valor": valor}
        st.session_state.transacoes.append(nova_transacao)
        salvar_dados(st.session_state.transacoes)
        st.success(f"{tipo} de R$ {valor:.2f} registrada com sucesso!")
        st.rerun() # Atualiza a tela para mostrar os novos dados

st.divider()

# --- EXTRATO E SALDO ---
st.subheader("📊 Extrato e Saldo Atual")

# Lógica matemática para calcular o saldo final
saldo = 0.0
for t in st.session_state.transacoes:
    if t["tipo"] == "Receita":
        saldo += t["valor"]
    else:
        saldo -= t["valor"]

# Componente visual para mostrar o Saldo Destacado
if saldo < 0:
    st.metric(label="Saldo Total", value=f"R$ {saldo:.2f}", delta="Conta no Vermelho!", delta_color="inverse")
else:
    st.metric(label="Saldo Total", value=f"R$ {saldo:.2f}", delta="Estável")

# Exibe a lista de transações de forma limpa na tela
if st.session_state.transacoes:
    st.markdown("**Histórico de Movimentações:**")
    # Mostra os mais recentes no topo
    for t in reversed(st.session_state.transacoes):
        cor = "green" if t["tipo"] == "Receita" else "red"
        st.markdown(f":{cor}[[{t['tipo']}]] **{t['categoria']}**: R$ {t['valor']:.2f}")
else:
    st.info("Nenhuma transação registrada ainda.")