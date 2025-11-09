class Rota:
    lista_de_rotas = []

    def __init__(
        self,
        origem,
        destino,
        horario,
        duracao,
        preco,
        motorista,
        ponto_embarque,
        ponto_desembarque,
    ):
        self.origem = origem
        self.destino = destino
        self.horario = horario
        self.duracao = duracao
        self.preco = preco
        self.motorista = motorista
        self.ponto_embarque = ponto_embarque
        self.ponto_desembarque = ponto_desembarque

    def __str__(self):
        return f"Rota de {self.origem} para {self.destino} com {self.motorista}"

    # converter o objeto em um dicionário (para salvar em JSON)
    def to_dict(self):
        return {
            "origem": self.origem,
            "destino": self.destino,
            "horario": self.horario,
            "duracao": self.duracao,
            "preco": self.preco,
            "motorista": self.motorista,
            "ponto_embarque": self.ponto_embarque,
            "ponto_desembarque": self.ponto_desembarque,
        }
