import datetime
class Conta:
    

    def __init__(self, usuario, saldo, poupanca, id, senha, ):
        self.usuario = usuario
        self.saldo = saldo
        self.poupanca = poupanca
        self.senha = senha
        self.id = id
    
    def to_dict(self):
        return {
            "id": self.id,
            "senha": self.senha,
            "saldo": self.saldo,
            "poupança": self.poupanca,
            "usuario": self.usuario.to_dict(),
            "ultimo_rendimento": datetime.datetime.now().isoformat()
        }