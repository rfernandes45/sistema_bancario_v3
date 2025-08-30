# Módulo de texto para exibir o menu de opções ao usuário.
menu = """
================ MENU ================
[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[q]\tSair
=> """

# Variáveis para armazenar o estado da conta.
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

# Loop principal do sistema.
while True:

    # Exibe o menu e captura a opção do usuário.
    opcao = input(menu)

    # --- Operação de Depósito ---
    if opcao == "d":
        print("---------- Depósito ----------")
        try:
            valor = float(input("Informe o valor do depósito: R$ "))

            if valor > 0:
                saldo += valor
                # Adiciona a transação ao extrato com a formatação correta.
                extrato += f"Depósito:\t\tR$ {valor:.2f}\n"
                print("\n=== Depósito realizado com sucesso! ===")
            else:
                print("\n@@@ Operação falhou! O valor informado é inválido. Tente novamente. @@@")

        except ValueError:
            print("\n@@@ Operação falhou! Por favor, insira um número válido. @@@")

    # --- Operação de Saque ---
    elif opcao == "s":
        print("---------- Saque ----------")
        try:
            valor = float(input("Informe o valor do saque: R$ "))

            excedeu_saldo = valor > saldo
            excedeu_limite = valor > limite
            excedeu_saques = numero_saques >= LIMITE_SAQUES

            if excedeu_saldo:
                print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

            elif excedeu_limite:
                print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}. @@@")

            elif excedeu_saques:
                print("\n@@@ Operação falhou! Número máximo de saques diários atingido. @@@")
            
            elif valor > 0:
                saldo -= valor
                # Adiciona a transação ao extrato com a formatação correta.
                extrato += f"Saque:\t\t\tR$ {valor:.2f}\n"
                numero_saques += 1
                print("\n=== Saque realizado com sucesso! Retire o dinheiro na boca do caixa. ===")

            else:
                print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        
        except ValueError:
            print("\n@@@ Operação falhou! Por favor, insira um número válido. @@@")


    # --- Operação de Extrato ---
    elif opcao == "e":
        print("\n================ EXTRATO ================")
        # Verifica se o extrato está em branco.
        if not extrato:
            print("Não foram realizadas movimentações.")
        else:
            print(extrato)
        
        # Exibe o saldo atual com a formatação correta.
        print(f"\nSaldo:\t\t\tR$ {saldo:.2f}")
        print("==========================================")

    # --- Opção de Sair ---
    elif opcao == "q":
        print("Obrigado por usar nosso sistema. Volte sempre!")
        break

    # --- Opção Inválida ---
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")