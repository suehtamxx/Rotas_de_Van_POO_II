class Rota:
    """
    Modelo de dados que representa uma viagem/rota no sistema.
    Armazena atributos como origem, destino, paradas e dias, além de manter uma lista estática das rotas carregadas na memória.
    """

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
        paradas="",
        dias_disponiveis="",
        id=None,
    ):
        self.id = id
        self.origem = origem
        self.destino = destino
        self.horario = horario
        self.duracao = duracao
        self.preco = preco
        self.motorista = motorista
        self.ponto_embarque = ponto_embarque
        self.ponto_desembarque = ponto_desembarque
        self.paradas = paradas
        self.dias_disponiveis = dias_disponiveis
        Rota.lista_de_rotas.append(self)

    def to_dict(self):
        return {
            "id": self.id,
            "origem": self.origem,
            "destino": self.destino,
            "horario": self.horario,
            "duracao": self.duracao,
            "preco": self.preco,
            "motorista": self.motorista,
            "ponto_embarque": self.ponto_embarque,
            "ponto_desembarque": self.ponto_desembarque,
            "paradas": self.paradas,
            "dias_disponiveis": self.dias_disponiveis,
        }

    def __str__(self):
        return f"Rota de {self.origem} para {self.destino} ({self.dias_disponiveis})"
