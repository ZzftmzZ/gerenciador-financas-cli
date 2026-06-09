import sqlite3
import os
import bcrypt

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
NOME_BANCO = os.path.join(PASTA_ATUAL, "financas.db")

def conectar_banco():
    """Garante que o banco de dados e as tabelas existam."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    
    # 1. Tabela de Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    
    # 2. Tabela de Finanças (Agora com a coluna usuario_id)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            valor REAL NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)
    conexao.commit()
    conexao.close()

# --- FUNÇÕES DE USUÁRIO ---

def criar_usuario(usuario, senha_limpa):
    """Cadastra um novo usuário criptografando a senha."""
    conectar_banco()
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    
    # Criptografa a senha antes de salvar
    senha_bytes = senha_limpa.encode('utf-8')
    senha_cripto = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode('utf-8')
    
    try:
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario.strip().lower(), senha_cripto))
        conexao.commit()
        sucesso = True
    except sqlite3.IntegrityError:
        sucesso = False # Usuário já existe
        
    conexao.close()
    return sucesso

def verificar_login(usuario, senha_limpa):
    """Verifica se o usuário existe e se a senha está correta."""
    conectar_banco()
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id, senha FROM usuarios WHERE usuario = ?", (usuario.strip().lower(),))
    resultado = cursor.fetchone()
    conexao.close()
    
    if resultado:
        usuario_id, senha_cripto = resultado
        # Verifica se a senha digitada bate com a criptografada do banco
        if bcrypt.checkpw(senha_limpa.encode('utf-8'), senha_cripto.encode('utf-8')):
            return usuario_id
    return None

# --- FUNÇÕES DE FINANÇAS (VINCULADAS AO USUÁRIO) ---

def salvar_no_banco(usuario_id, tipo, categoria, valor):
    """Insere uma transação vinculada ao ID do usuário logado."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO financas (usuario_id, tipo, categoria, valor) 
        VALUES (?, ?, ?, ?)
    """, (usuario_id, tipo, categoria.strip().capitalize(), valor))
    conexao.commit()
    conexao.close()

def carregar_do_banco(usuario_id):
    """Busca APENAS as transações do usuário logado."""
    conectar_banco()
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    
    cursor.execute("SELECT tipo, categoria, valor FROM financas WHERE usuario_id = ?", (usuario_id,))
    linhas = cursor.fetchall()
    conexao.close()
    
    lista_transacoes = []
    for linha in linhas:
        lista_transacoes.append({
            "tipo": linha[0],
            "categoria": linha[1],
            "valor": linha[2]
        })
    return lista_transacoes