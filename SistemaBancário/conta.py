class Conta:
    def __init__(self, usuario, saldo, id, senha):
        self.usuario = usuario
        self.saldo = saldo
        self.senha = senha
        self.id = id
    
    def to_dict(self):
        return {
            "id": self.id,
            "senha": self.senha,
            "saldo": self.saldo,
            "usuario": self.usuario.to_dict()
        }