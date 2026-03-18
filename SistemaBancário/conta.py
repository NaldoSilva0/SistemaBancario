import datetime
class Conta:
    

    def __init__(self, usuario, saldo, poupanca, id, senha, logs ):
        self.usuario = usuario
        self.saldo = saldo
        self.poupanca = poupanca
        self.senha = senha
        self.id = id
        self.logs = logs
    
    def to_dict(self):
        return {
            "id": self.id,
            "senha": self.senha,
            "saldo": self.saldo,
            "poupança": self.poupanca,
            "usuario": self.usuario.to_dict(),
            "ultimo_rendimento": datetime.datetime.now().isoformat(),
            "logs": self.logs
        }