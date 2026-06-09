import sqlite3
import os

# TRUQUE DO CAMINHO: Descobre automaticamente a pasta onde este arquivo está salvo
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
NOME_BANCO = os.path.join(PASTA_ATUAL, "financas.db")

def conectar_banco():
    """Garante que o banco de dados e a tabela existam."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    
    # Cria a tabela usando comandos SQL reais
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            valor REAL NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

def salvar_no_banco(tipo, categoria, valor):
    """Insere um novo registro de transação no banco."""
    conectar_banco()  # Garante que a tabela existe antes de inserir
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    
    # O uso de '?' garante segurança contra SQL Injection
    cursor.execute("""
        INSERT INTO financas (tipo, categoria, valor) 
        VALUES (?, ?, ?)
    """, (tipo, categoria, valor))
    
    conexao.commit()
    conexao.close()

def carregar_do_banco():
    """Busca os dados no banco e converte para o formato que o Streamlit lê."""
    conectar_banco()  # Garante que a tabela existe antes de ler
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    
    cursor.execute("SELECT tipo, categoria, valor FROM financas")
    linhas = cursor.fetchall()
    conexao.close()
    
    # Converte as tuplas do banco em uma lista de dicionários
    lista_transacoes = []
    for linha in linhas:
        lista_transacoes.append({
            "tipo": linha[0],
            "categoria": App_formata_categoria(linha[1]),
            "valor": linha[2]
        })
    return lista_transacoes

def App_formata_categoria(texto):
    """Garante que o texto da categoria fique limpo e padronizado."""
    return str(texto).strip().capitalize()