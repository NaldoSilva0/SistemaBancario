from usuario import Usuario
from conta import Conta
from persistencia import Banco
import re
import time


banco = Banco()
conta_logada = None

#FAZ COM QUE O CPF ESTEJA NO FORMATO CERTO NA HORA DE REGISTRAR A CONTA (XXX.XXX.XXX-XX)
def cpf_valido(cpf):
    padrao = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    
    if re.match(padrao, cpf):
        return True
    return False

# FAZ COM QUE A DATA DE NASCIMENTO NA HORA DO REGISTRO ESTEJA NO FORMATO CERTO (DD/MM/AAAA)
def data_valida(data):
    padrao = r"^\d{2}/\d{2}/\d{4}$"
    
    if re.match(padrao, data):
        return True
    return False

# FUNÇÃO PARA VERIFICAR A SENHA E REPETIR
def repetir_senha():
    while True:
        senha = input('Digite a senha: ')
        repSenha = input('Repita a senha: ')

        if senha != repSenha:
            print('As senha não são iguais, tente novamente')
            continue
        return senha

# MENU PARA REGISTRAR UM USUÁRIO
def interface_registrar(banco):
    print("---REGISTRAR CONTA---")
    usuario = input("Digite seu nome de usuário: ")
    if banco.buscar_usuario(usuario):
        print("Erro: Esse usuário já está em uso, tente novamente com outro usuário")
        return
    senha_final = repetir_senha()
    
    while True:
        cpf = input("Digite seu CPF (XXX.XXX.XXX-XX): ")
        if cpf_valido(cpf):
            break
        print("formato inválido! use xxx.xxx.xxx-xx")

    while True:
        data_nascimento = input("Digite sua data de nascimento (DD/MM/AAAA): ")
        if data_valida(data_nascimento):
            break
        print("formato inválido! use DD/MM/AAAA")

    

    novo_user = Usuario(usuario, cpf, data_nascimento)
    novo_id = banco.gerar_id()
    saldo_inicial = 0
    poupança_inicial = 0
    nova_conta = Conta(novo_user, saldo_inicial, poupança_inicial, novo_id, senha_final)

    banco.adicionar_conta(nova_conta)
    print(f"Conta criada com sucesso! ID:{novo_id}")

# FUNÇÃO PARA LOGAR NA CONTA DO USUÁRIO
def logar_conta(banco):
    print("-=-"*20)
    print("---MENU DE LOGIN---")
    

    usuario_login = input("Digite seu usuário: ")

    conta = banco.buscar_usuario(usuario_login)
    if not conta:
        print("Essa conta não está cadastrada.")
        return None

    senha_login = input("Digite sua senha: ")
    if conta:
        if conta['senha'] == senha_login:
            print(f"Login realizado! Seja bem vindo, {usuario_login}!")
            interface_conta(conta, banco)
            return conta

        else:
            print("Senha incorreta!!")
    else:
        print("Usuário não encontrado.")

def sacar_dinheiro_poupanca(conta_logada, banco):
        try:
            valor = float(input("Digite o valor para ser sacado: R$  "))
            
            if valor <= 0:
                print("Valor inválido!")
                return
            
            if valor > conta_logada['poupança']:
                print("O valor digitado é superior ao valor depositado na conta!")
                return

            conta_logada['poupança'] -= valor
            conta_logada['saldo'] += valor

            banco.salvar_dados()
            print("Valor sacado com sucesso!")
        
        except ValueError:
            print("Digite um valor válido!")

# USADO PARA SACAR UM DINHEIRO DO SALDO DA CONTA
def sacar_dinheiro(conta_logada, banco):
    try:
        valor = float(input("Digite o valor para ser sacado: R$  "))
        
        if valor <= 0:
            print("Valor inválido!")
            return
        
        if valor > conta_logada['saldo']:
            print("O valor digitado é superior ao valor depositado na conta!")
            return

        conta_logada['saldo'] -= valor

        banco.salvar_dados()
        print("Valor sacado com sucesso!")
    
    except ValueError:
        print("Digite um valor válido!")

# USADO PARA DEPOSITAR UM DINHEIRO NO SALDO DA CONTA
def depositar_dinheiro(conta_logada, banco):
    print("---DEPOSITAR---")
    valor = float(input("Digite o valor para depositar na conta: "))
    if valor <= 0:
        print("Digite um valor válido!")
        raise
    else:
        conta_logada['saldo'] += valor

        banco.salvar_dados()
        print("Valor depositado em sua conta!")

# MENU QUE ABRE APÓS VOCÊ COMPLETAR O LOGIN
def interface_conta(conta_logada, banco):
    while True:
        print('-=-'*20)
        print("---MENU DA CONTA---")

        print(f"USUÁRIO: {conta_logada['usuario']['nome']} | ID: {conta_logada['id']}")
        print(f"SALDO: R${conta_logada['saldo']}")

        print("-=-"*20)
        
        print("[1]- Sacar")
        print("[2]- Depositar")
        print("[3]- Transferir")
        print("[4]- Poupança")
        print("[5]- Informações")
        print("[6]- Sair")

        resposta = input("Digite a opção de seu desejo: ")

        if resposta == '1':
            sacar_dinheiro(conta_logada, banco)

        elif resposta == '2':
            depositar_dinheiro(conta_logada, banco)

        elif resposta == '3':
            transferir_dinheiro(conta_logada, banco)

        elif resposta == '4':
            interface_poupanca(conta_logada, banco)
        #elif resposta == '5':

        elif resposta == '6':
            print("Saindo de sua conta...")
            time.sleep(1.5)
            break

        #else:
            #print("Opção inválida! digite algo válido.")

# O USUÁRIO ESCREVE O ID DO DESTINATÁRIO, O SISTEMA VERIFICA SE EXISTE E MOSTRA O NOME DO USUÁRIO QUE ESTÁ VINCULADO AO ID, SE TUDO FOR CONFIRMADO, A TRANSFERÊNCIA É REALIZADA
def transferir_via_id(conta_logada, banco):
    print("TRANSFERÊNCIA")
    id_conta_destino = int(input("Digite o ID da conta que deseja transferir dinheiro: "))
    id_existe = banco.buscar_conta_id(id_conta_destino)

    if id_conta_destino == conta_logada["id"]:
        print("Você não pode fazer uma transferência para sí mesmo")
        return

    if id_existe == None:
        print("O ID não existe ou está incorreto")
        return
    else:
        print(f"O usuário que está vínculado à esse ID é: {banco.buscar_conta_por_id(id_conta_destino)}")
        confirmar_pessoa = input("Essa é a pessoa que você quer realizar a transferência? [S/n]: ").lower()
        if confirmar_pessoa == "n":
            print("Retornando para o menu...")
            time.sleep(1.5)
        elif confirmar_pessoa == "s":
            valor_transferir = float(input("Digite o valor que deseja transferir: "))
            
            transferir = banco.transferir_id(conta_logada['id'], id_conta_destino, valor_transferir)
            if transferir == False:
                print("o saldo da transferência é maior que o saldo da conta")
            elif transferir == True:
                print("Transferência feita com sucesso!!")
                return
            else:
                print("Digite uma opção válida!")

        else:
            print("Digite uma opção válida!")
            return

# O USUÁRIO ESCREVE O CPF DO DESTINATÁRIO, O SISTEMA VERIFICA SE EXISTE E MOSTRA O NOME DO USUÁRIO QUE ESTÁ VINCULADO AO CPF, SE TUDO FOR CONFIRMADO, A TRANSFERÊNCIA É REALIZADA
def transferir_via_cpf(conta_logada, banco):
    print("TRANSFERÊNCIA")
    cpf_conta_destino = input("Digite o CPF da conta que deseja transferir dinheiro (xxx.xxx.xxx-xx):  ")
    cpf_existe = banco.buscar_conta_cpf(cpf_conta_destino)

    if cpf_existe == conta_logada["usuario"]["cpf"]:
        print("Você não pode realizar transferência para a sua própria conta!")

    if cpf_existe == None:
        print("CPF não está registrado ou está incorreto!")
    
    else:
        print(f"O usuário que está vinculado á esse CPF é {banco.buscar_conta_por_cpf(cpf_conta_destino)}")
        destinatario_correto = input("O usuário que deseja transferir está correto? [S/N]: ").lower()
        if destinatario_correto == 'n':
            print("Retornando para o menu!")
            time.sleep(1.5)
            return
        
        elif destinatario_correto == 's':
            valor_transferir = float(input("Digite o valor que queira transferir: "))

            transferir = banco.transferir_cpf(conta_logada["usuario"]['cpf'], cpf_conta_destino, valor_transferir)
            if transferir == False:
                print("o saldo da transferência é maior que o saldo da conta")

            elif transferir == True:
                print("Transferência feita com sucesso!!")
                return
            else:
                print("Digite uma opção válida!")
                return

# FUNÇÃO FEITA PARA VISUALIZAR O SALDO QUE ESTÁ NA POUPANÇA DA CONTA LOGADA
def visualizar_poupanca(conta_logada):
    print('---Saldo---')
    print(f"Saldo: R$ {conta_logada['poupança']}")
    print("------")
    input("Pressione ENTER para voltar ao menu")

def guardar_dinheiro_poupança(conta_logada, banco):
    print("-=-" *20)
    print("---Deposito---")

    valor = float(input("Digite o valor que deseja depositar em sua poupança: "))
    verificacao = banco.depositar_poupança(conta_logada, valor)
    if verificacao == False:
        print("O valor digitado é maior que o saldo da conta, ou é inválido!")
    elif verificacao == True:
        print("Valor depositado em sua poupança com sucesso!!")

# MENU DO SISTEMA DE POUPANÇA,
def interface_poupanca(conta_logada, banco):
    while True:
        print("-=-" * 20)
        print("---POUPANÇA---")

        print('[1]- Abrir saldo da poupança')
        print('[2]- Guardar dinheiro')
        print('[3]- Sacar dinheiro')
        print('[4]- Retornar')

        resposta = input("Digite a opção que desejar: ")

        if resposta == '1':
            banco.calcular_juros(conta_logada)
            visualizar_poupanca(conta_logada)
        elif resposta == '2':
            guardar_dinheiro_poupança(conta_logada, banco)
        elif resposta == '3':
            sacar_dinheiro_poupanca(conta_logada, banco)
        elif resposta == '4':
            print("Retornando ao menu...")
            time.sleep(1.5)
            break
        else:
            print("Opção inválida!")
    
# MENU PARA TRANSFERIR DINHEIRO DE UMA CONTA PARA OUTRA, COM A OPÇÃO DE CPF OU ID DA CONTA
def transferir_dinheiro(conta_logada, banco):
    print("---MENU DE TRANSFERÊNCIA---")
    print("Escolha a opção que desejar")

    print("-=-"*20)

    print("[1]-ID")
    print("[2]-CPF")

    resposta = input("DIgite a opção desejada: ")

    if resposta == "1":
        transferir_via_id(conta_logada, banco)
    elif resposta == "2":
        transferir_via_cpf(conta_logada, banco)
    else:
        print("Oção inválida!")

# MENU INICIAL DO CÓDIGO, TUDO FUNCIONA APARTIR DELE
while True:
    print("---MENU INICIAL---")

    print("[1]-REGISTRAR CONTA")
    print("[2]-LOGAR CONTA")
    print("[3]-SAIR DO SISTEMA")

    resposta = input("Digite a opção desejada: ")
    if resposta == '1':
        interface_registrar(banco)

    elif resposta == '2':
        logar_conta(banco)

    elif resposta == '3':
        print("Agradecemos por usar nossos serviços!")
        break
    else:
        print("Digite uma opção válida!!")
        
