class Usuario:
    def __init__(self, usuario, cpf, data_nascimento):
        self.nome = usuario
        self.cpf = cpf
        self.data_nascimento = data_nascimento

    def to_dict(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento
        }