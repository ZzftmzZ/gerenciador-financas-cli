def adicionar_transacao(tipo, transacoes):  # <-- Adicionado 'transacoes' aqui
    print(f"\n--- Adicionando {tipo} ---")
    categoria = input("Digite a categoria (ex: Salário, Alimentação, Lazer): ").strip()
    
    try:
        valor = float(input("Digite o valor (ex: 150.50): "))
        if valor <= 0:
            print("O valor deve ser maior que zero!")
            return
    except ValueError:
        print("Valor inválido! Digite apenas números e use ponto para os centavos.")
        return

    # Cria o dicionário da transação
    nova_transacao = {
        "tipo": tipo,
        "categoria": categoria,
        "valor": valor
    }
    
    # Adiciona na nossa lista
    transacoes.append(nova_transacao)
    print(f"{tipo} de R$ {valor:.2f} adicionada com sucesso!")