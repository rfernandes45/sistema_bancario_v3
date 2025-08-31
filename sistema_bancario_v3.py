# Importações necessárias
from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

# --- Classes de Domínio ---

class Cliente:
    """
    Classe que representa um cliente do banco.
    Possui um endereço e uma lista de contas.
    """
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        """Realiza uma transação em uma das contas do cliente."""
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Adiciona uma nova conta para o cliente."""
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """
    Classe que representa um cliente do tipo Pessoa Física.
    Herda de Cliente e adiciona atributos específicos.
    """
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    """
    Classe que representa uma conta bancária.
    Contém um saldo, número, agência, um cliente associado e um histórico de transações.
    """
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Método de fábrica para criar uma nova conta."""
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        """
        Realiza um saque na conta. Retorna True se bem-sucedido, False caso contrário.
        """
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

    def depositar(self, valor):
        """
        Realiza um depósito na conta. Retorna True se bem-sucedido, False caso contrário.
        """
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False


class ContaCorrente(Conta):
    """
    Classe que representa uma Conta Corrente, com regras específicas.
    Herda de Conta.
    """
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0

    def sacar(self, valor):
        """
        Sobrescreve o método sacar para incluir regras de limite e número de saques.
        """
        if valor > self._limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False
        
        if self._numero_saques >= self._limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False
        
        # Chama o método sacar da classe pai para a lógica principal
        sucesso_saque = super().sacar(valor)
        
        if sucesso_saque:
            self._numero_saques += 1
        
        return sucesso_saque

    def __str__(self):
        """Representação em string da conta para exibição."""
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    """
    Classe que armazena o histórico de transações de uma conta.
    """
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """Adiciona uma transação ao histórico com data e hora."""
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    """Classe base abstrata para todas as transações."""
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    """Classe que representa a transação de saque."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Registra a transação de saque na conta."""
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """Classe que representa a transação de depósito."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Registra a transação de depósito na conta."""
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

# --- Funções Auxiliares do Menu ---

def exibir_menu():
    """Exibe o menu de opções e retorna a escolha do usuário."""
    menu = """
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo Usuário
    [nc]\tNova Conta
    [lc]\tListar Contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    """Filtra um cliente da lista com base no CPF."""
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    """Recupera a conta de um cliente. Assume um cliente com uma única conta."""
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0]

def depositar_valor(clientes):
    """Função para orquestrar a operação de depósito."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: R$ "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

def sacar_valor(clientes):
    """Função para orquestrar a operação de saque."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: R$ "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

def exibir_extrato_cliente(clientes):
    """Função para orquestrar a exibição do extrato."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if conta:
        print("\n================ EXTRATO ================")
        transacoes = conta.historico.transacoes
        if not transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in transacoes:
                print(f"{transacao['tipo']}:\t\tR$ {transacao['valor']:.2f}")
        print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
        print("==========================================")

def criar_cliente(clientes):
    """Função para orquestrar a criação de um novo cliente."""
    cpf = input("Informe o CPF (somente números): ")
    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe um cliente com este CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")

def criar_nova_conta(numero_conta, clientes, contas):
    """Função para orquestrar a criação de uma nova conta."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! Criação de conta encerrada. @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")

def listar_todas_contas(contas):
    """Função para listar todas as contas criadas."""
    print("\n================ CONTAS ================")
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            print(str(conta))
            print("-" * 38)
    print("==========================================")


def main():
    """Função principal que executa o sistema bancário."""
    clientes = []
    contas = []

    while True:
        opcao = exibir_menu()

        if opcao == 'd':
            depositar_valor(clientes)
        elif opcao == 's':
            sacar_valor(clientes)
        elif opcao == 'e':
            exibir_extrato_cliente(clientes)
        elif opcao == 'nu':
            criar_cliente(clientes)
        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            criar_nova_conta(numero_conta, clientes, contas)
        elif opcao == 'lc':
            listar_todas_contas(contas)
        elif opcao == 'q':
            print("Obrigado por usar nosso sistema. Volte sempre!")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()
