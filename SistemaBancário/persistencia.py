import json
import os
from datetime import datetime

class Banco:
    def __init__(self, arquivo='dados.json'):
        self.arquivo = arquivo
        self.contas = self.carregar_dados()
# Carrega todos os dados dos usuários
    def carregar_dados(self):
        if not os.path.exists(self.arquivo):
            return []
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            return []

# Salva informações do usuário
    def salvar_dados(self):
        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(self.contas, arquivo, indent=4, ensure_ascii=False)

# Adiciona a conta recem criada no arquivo Json
    def adicionar_conta(self, nova_conta):
        self.contas.append(nova_conta.to_dict()) 
        self.salvar_dados()

# Verifica se o usuário existe nos dados
    def buscar_usuario(self, nome_digitado):
        for conta in self.contas:
            if conta['usuario']['nome'] == nome_digitado:
                return conta
        return None

# Busca a conta que eást vinculado ao id digitado
    def buscar_conta_id(self, id):
        for conta in self.contas:
            if conta['id'] == id:
                return conta
        return None

# Busca a conta que está vinculado ao cpf digitado
    def buscar_conta_cpf(self, cpf):
        for conta in self.contas:
            if conta["usuario"]["cpf"] == cpf:
                return conta
        return None

# Busca a conta pelo cpf e retorna o nome do usuário
    def buscar_conta_por_cpf(self, cpf_destino):
        for conta in self.contas:
            if conta["usuario"]["cpf"] == cpf_destino:
                return conta['usuario']['nome']
        return None

# Busca a conta pelo id e retorna o nome do usuário
    def buscar_conta_por_id(self, id_destino):
        for conta in self.contas:
            if conta["id"] == id_destino:
                return conta["usuario"]['nome']
        return None

# Usado para transferir dinheiro pelo id
    def transferir_id(self, id_origem, id_destino, valor):
        conta_origem = self.buscar_conta_id(id_origem)
        conta_destino = self.buscar_conta_id(id_destino)

        if conta_origem is None or conta_destino is None:
            return False

        if conta_origem['saldo'] < valor:
            return False
        
        conta_origem['saldo'] -= valor
        conta_destino['saldo'] += valor

        self.salvar_dados()
        return True

# Usado para transferir dinheiro pelo cpf
    def transferir_cpf(self, cpf_origem, cpf_destino, valor):
        conta_origem = self.buscar_conta_cpf(cpf_origem)
        conta_destino = self.buscar_conta_cpf(cpf_destino)

        if conta_origem is None or conta_destino is None:
            return False

        if conta_origem['saldo'] < valor:
            return False
        
        conta_origem['saldo'] -= valor
        conta_destino['saldo'] += valor

        self.salvar_dados()
        return True

# Depositar o dinheiro na poupança da conta logada
    def depositar_poupança(self, conta, valor):
        self.conta = conta

        if conta['saldo'] < valor:
            return False
        
        conta['saldo'] = round(conta['saldo'] - valor, 2)
        conta['poupança'] = round(conta['poupança'] + valor,2)

        self.salvar_dados()
        return True

# Calcula os juros da poupança
    def calcular_juros(self, conta):
        data_agora = datetime.now()
        ultimo_rendimento = datetime.fromisoformat(conta['ultimo_rendimento'])

        diferenca = data_agora - ultimo_rendimento
        minutos_passado = int(diferenca.total_seconds() // 60)

        if minutos_passado >= 1:
            taxa = 0.01
            rendimento = conta['poupança'] * taxa * minutos_passado
            conta['poupança'] = round(conta['poupança'] + rendimento, 2)

            conta['ultimo_rendimento'] = data_agora.isoformat()
            self.salvar_dados()
            return True
        return False

# Gera um novo id de acordo com o id anterior sempre sendo +1
    def gerar_id(self):
        if not self.contas:
            return 1
        
        return self.contas[-1]['id'] + 1





