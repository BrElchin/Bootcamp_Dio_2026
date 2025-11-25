def menu():
    return """
    ================ MENU ================
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nu] Novo usuário
    [nc] Nova conta
    [lc] Listar contas
    [q]  Sair
    => """

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print(f"Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    if any(u["cpf"] == cpf for u in usuarios):
        print("Já existe usuário com esse CPF!")
        return
    nome = input("Nome completo: ")
    data_nasc = input("Data de nascimento (dd/mm/aaaa): ")
    logradouro = input("Logradouro: ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade_estado = input("Cidade/Sigla estado (ex: São Paulo/SP): ")
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade_estado}"
    usuarios.append({"nome": nome, "data_nascimento": data_nasc, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    return next((u for u in usuarios if u["cpf"] == cpf), None)

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("Usuário não encontrado!")
    return None

def listar_contas(contas):
    for conta in contas:
        print("=" * 50)
        print(f"Agência:\t{conta['agencia']}")
        print(f"Conta:\t\t{conta['numero_conta']}")
        print(f"Titular:\t{conta['usuario']['nome']}")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta_seq = 1

    while True:
        opcao = input(menu()).lower()
        if opcao == "d":
            valor = float(input("Valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == "s":
            valor = float(input("Valor do saque: "))
            saldo, numero_saques = sacar(saldo=saldo, valor=valor, extrato=extrato,
                                        limite=limite, numero_saques=numero_saques,
                                        limite_saques=LIMITE_SAQUES)
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == "nu":
            criar_usuario(usuarios)
        elif opcao == "nc":
            conta = criar_conta(AGENCIA, numero_conta_seq, usuarios)
            if conta:
                contas.append(conta)
                numero_conta_seq += 1
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            print("Obrigado por usar o sistema!")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
