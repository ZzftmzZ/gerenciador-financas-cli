import json
import os

def salvar_dados(transacoes):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(transacoes, f, indent=4, ensure_ascii=False)

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []  # Retorna uma lista vazia se o arquivo não existir ainda

ARQUIVO_DADOS = "financas.json"

def exibir_extrato(transacoes):  # <-- Adicionado 'transacoes' aqui
    print("\n=== EXTRATO DA CONTA ===")
    if not transacoes:
        print("Nenhuma transação registrada ainda.")
        print("Saldo Atual: R$ 0.00")
        return

    saldo = 0.0
    for t in transacoes:
        # Exibe cada linha formatada
        print(f"[{t['tipo']}] {t['categoria']}: R$ {t['valor']:.2f}")
        
        # Lógica matemática do saldo
        if t['tipo'] == "Receita":
            saldo += t['valor']
        else:
            saldo -= t['valor']
            
    print("------------------------")
    if saldo < 0:
        print(f"SALDO ATUAL: R$ {saldo:.2f} (Atenção: Conta no vermelho!)")
    else:
        print(f"SALDO ATUAL: R$ {saldo:.2f}")
    print("========================")