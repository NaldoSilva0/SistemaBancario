from usuario import Usuario
from conta import Conta
from persistencia import Banco
import re
import time
from datetime import datetime


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
    padrao = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    
    while True:
        print("\nSua senha deve ter no mínimo 8 caracteres, incluindo:")
        print("Letra maiúscula, minúscula, número e caractere especial (@$!%*?&)")

        senha = input('Digite a senha: ')
        if not re.match(padrao, senha):
            print("Os requisitos de senha não foram atendidos!")
            continue
        
        repetir_senha = input("Repita a senha: ")
        
        if repetir_senha != senha:
            print("As senhas não são iguais! tente novamente.")
            continue
        return senha


# MENU PARA REGISTRAR UM USUÁRIO
def interface_registrar(banco):
    print("---REGISTRAR CONTA---")
    while True: 
        usuario = input("Digite seu nome de usuário: ").strip()
        if len(usuario) >= 3 and usuario.replace(" ", "").isalpha():
            break
        else:
            print("Nome inválido! Use somente letras e use no mínimo 3 caracteres")
            return


    if banco.buscar_usuario(usuario):
        print("Erro: Esse usuário já está em uso, tente novamente com outro usuário")
        return
    senha_final = repetir_senha()
    
    while True:
        cpf = input("Digite seu CPF (XXX.XXX.XXX-XX): ")
        valido = cpf_valido(cpf)
        if valido == False:
            print("Formato inválido! use xxx.xxx.xxx-xx")
            continue
        
        verificar = banco.cpf_em_uso(cpf, banco.contas)
        if verificar == True:
            print("Esse cpf já está vinculado em uma conta!")
            continue
        else:
            break
           

    while True:
        data_nascimento = input("Digite sua data de nascimento (DD/MM/AAAA): ")
        
        try: 

            data_obj = datetime.strptime(data_nascimento, "%d/%m/%Y")
            ano_atual = datetime.now().year
            if 1941 <= data_obj.year <= ano_atual:
                break
            else:
                print("Data de nascimento fora do aceitável")

        except ValueError:
            print("Data inválida, Digite no formato correto DD/MM/AAAA")
 

    novo_user = Usuario(usuario, cpf, data_nascimento)
    novo_id = banco.gerar_id()
    saldo_inicial = 0
    poupança_inicial = 0
    logs = []
    nova_conta = Conta(novo_user, saldo_inicial, poupança_inicial, novo_id, senha_final, logs)

    banco.adicionar_conta(nova_conta)
    print(f"Conta criada com sucesso! ID:{novo_id}")

# FUNÇÃO PARA LOGAR NA CONTA DO USUÁRIO
def logar_conta(banco):
    print("-=-"*20)
    print("---MENU DE LOGIN---")
    

    usuario_login = input("Digite seu usuário ou seu cpf: ")

    conta = banco.buscar_usuario(usuario_login) or banco.buscar_usuario_por_cpf(usuario_login)
    if not conta:
        print("Essa conta não está cadastrada.")
        return None

    senha_login = input("Digite sua senha: ")
    if conta:
        if conta['senha'] == senha_login:
            banco.salvar_logs(conta, "Login realizado")
            print('-'*30)
            print(f"Login realizado! Seja bem vindo, {conta['usuario']['nome']}!")
            interface_conta(conta, banco)
            return conta

        else:
            print("Senha incorreta!!")
    else:
        print("Usuário não encontrado.")

# SACA O DINHEIRO QUE ESTÁ NA POUPANÇA DA CONTA
def sacar_dinheiro_poupanca(conta_logada, banco):
        try:
            valor = float(input("Digite o valor para ser sacado: R$  "))
            
            if valor <= 0:
                print("Valor inválido!")
                return
            
            if valor > conta_logada['poupança']:
                print("O valor digitado é superior ao valor depositado na conta!")
                return

            conta_logada['poupança'] = round(conta_logada['poupança'] - valor, 2)
            conta_logada['saldo'] = round(conta_logada['saldo'] + valor, 2)

            banco.salvar_dados()
            banco.salvar_logs(conta_logada, "Sacou dinheiro da poupança")
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
        banco.salvar_logs(conta_logada, "Sacou dinheiro")
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
        banco.salvar_logs(conta_logada, "Depositou dinheiro")
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

        elif resposta == '5':
            informações_da_conta(conta_logada)

        elif resposta == '6':
            banco.salvar_logs(conta_logada, "Deslogou da conta")
            print("Saindo de sua conta...")
            time.sleep(1.5)
            break

        else:
            print("Opção inválida! digite algo válido.")

# INFORMAÇÕES DA CONTA LOGADA
def informações_da_conta(conta_logada):
    while True:
        print("-=-"*20)
        print("---INFORMAÇÕES---")
        print("[1]-Visualizar dados cadastrais")
        print("[2]-Mudar senha")
        print('[3]-Registro de entrada')
        print("[4]-Voltar")

        resposta = input("Digite a opção que desejar: ")

        if resposta == '1':
            informações_cadastrais(conta_logada)
        elif resposta == '2':
            trocar_senha(conta_logada, banco)
        elif resposta == '3':
            registro_entrada(conta_logada)
        elif resposta == '4':
            print("Retornando ao menu...")
            time.sleep(1.5)
            break

# EXIBIR AS INFORMAÇÕES DA CONTA (cpf, id, etc)
def informações_cadastrais(conta_logada):
    print("="*30)
    print("     DETALHES DA CONTA:")
    print("="*30)
    print(f"Usuário: {conta_logada["usuario"]["nome"]}")
    print(f"CPF: {conta_logada["usuario"]["cpf"]}")
    print(f"Data nascimento: {conta_logada["usuario"]['data_nascimento']}")
    print(f"id: {conta_logada["id"]}")
    print("-"*30)
    print(f"saldo CC: R${conta_logada["saldo"]}")
    print(f"Saldo poupança: R${conta_logada["poupança"]}")
    print("="*30)
    input("Pressione ENTER para retornar ao menu...")

# EXIBI O REGISTRO DE ENTRADA DA CONTA LOGADA
def registro_entrada(conta_logada):
    print("\n"  + "=" *30)
    print("    ---LOG DE ENTRADA---")
    print("="*30)

    if not conta_logada['logs']:
        print("Informações não encontradas!")

    for linha in conta_logada['logs']:
        print(f"- {linha}\n")
    print("-"*50)
    input("Pressione ENTER para voltar ao menu")

# USADO PARA TROCAR A SENHA ATUAL DA CONTA
def trocar_senha(conta_logada, banco):
    print("---Senha---")
    continuar_parar = input("Você tem certeza que deseja trocar a senha atual? [S/N]: ").lower()
    if continuar_parar == 'n':
        print("Retornando ao menu...")
        time.sleep(1.5)
        return
    elif continuar_parar == 's':
        senha_final = input("Digite a senha atual de sua conta: ")
        if senha_final != conta_logada['senha']:
            print("Senha incorreta!")

        else:
            if conta_logada['senha'] == senha_final:
                print("---NOVA SENHA---")
                nova_senha = repetir_senha()

                conta_logada['senha'] = nova_senha
                banco.salvar_dados()
                banco.salvar_logs(conta_logada, "Alterou a senha")
                print("Senha alterada com sucesso!!")

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
                banco.salvar_logs(conta_logada, "Transferiu via ID")
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
                banco.salvar_logs(conta_logada, "Transferiu via CPF")
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

# FUNÇÃO DE DEPOSITAR O DINHEIRO DA CONTA CORRENTE PARA A POUPANLA
def guardar_dinheiro_poupança(conta_logada, banco):
    print("-=-" *20)
    print("---Deposito---")

    valor = float(input("Digite o valor que deseja depositar em sua poupança: "))
    verificacao = banco.depositar_poupança(conta_logada, valor)
    if verificacao == False:
        print("O valor digitado é maior que o saldo da conta, ou é inválido!")
    elif verificacao == True:
        banco.salvar_logs(conta_logada, "Depositou dinheiro na poupança")
        print("Valor depositado em sua poupança com sucesso!!")

# MENU DO SISTEMA DE POUPANÇA
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
    print("[3]- Voltar")

    resposta = input("DIgite a opção desejada: ")

    if resposta == "1":
        transferir_via_id(conta_logada, banco)
    elif resposta == "2":
        transferir_via_cpf(conta_logada, banco)
    elif resposta == '3':
        print("Retornando ao menu...")
        time.sleep(1.5)
        return
    else:
        print("Opção inválida!")

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
        
