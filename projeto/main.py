# IMPORTANTE: Importar as funções dos outros arquivos do seu projeto
from adicionar_transacao import adicionar_transacao
from exibir_extrato import exibir_extrato, salvar_dados, carregar_dados

# Já começa o programa puxando o que foi salvo no arquivo JSON
transacoes = carregar_dados()

def exibir_menu():
    print("\n=== GERENCIADOR DE FINANÇAS INTERATIVO ===")
    print("1. Adicionar Receita (Ganho)")
    print("2. Adicionar Despesa (Gasto)")
    print("3. Ver Extrato e Saldo Atual")
    print("4. Sair")
    print("==========================================")

def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção (1-4): ")

        if opcao == "1":
            adicionar_transacao("Receita", transacoes)
            salvar_dados(transacoes)  # Salva automaticamente após adicionar
        elif opcao == "2":
            adicionar_transacao("Despesa", transacoes)
            salvar_dados(transacoes)  # Salva automaticamente após adicionar
        elif opcao == "3":
            exibir_extrato(transacoes)
        elif opcao == "4":
            print("Saindo... Seus dados foram salvos. Até logo!")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Executa o programa principal
if __name__ == "__main__":
    main()