import json
import os

class Banco:
    def __init__(self, arquivo='dados.json'):
        self.arquivo = arquivo
        self.contas = self.carregar_dados()

    def carregar_dados(self):
        if not os.path.exists(self.arquivo):
            return []
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            return []

    def salvar_dados(self):
        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(self.contas, arquivo, indent=4, ensure_ascii=False)

    def adicionar_conta(self, nova_conta):
        self.contas.append(nova_conta.to_dict()) 
        self.salvar_dados()

    def buscar_usuario(self, nome_digitado):
        for conta in self.contas:
            if conta['usuario']['nome'] == nome_digitado:
                return conta
        return None
    
    def buscar_conta_id(self, id):
        for conta in self.contas:
            if conta['id'] == id:
                return conta
        return None

    def buscar_conta_cpf(self, cpf):
        for conta in self.contas:
            if conta["usuario"]["cpf"] == cpf:
                return conta
        return None
    
    def buscar_conta_por_cpf(self, cpf_destino):
        for conta in self.contas:
            if conta["usuario"]["cpf"] == cpf_destino:
                return conta['usuario']['nome']
        return None
    
    def buscar_conta_por_id(self, id_destino):
        for conta in self.contas:
            if conta["id"] == id_destino:
                return conta["usuario"]['nome']
        return None
    
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
    
    def gerar_id(self):
        if not self.contas:
            return 1
        
        return self.contas[-1]['id'] + 1





