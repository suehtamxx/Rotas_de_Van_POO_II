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
        Rota.lista_de_rotas.append(self)

    def __str__(self):
        return f"Rota de {self.origem} para {self.destino} com {self.motorista}"


Rota(
    origem="Oeiras",
    destino="UFPI",
    horario="07:30",
    duracao="90 min",
    preco="R$ 10,00",
    motorista="José Lucas",
    ponto_embarque="Praça 1 (Oeiras)",
    ponto_desembarque="Estacionamento da UFPI (Picos)",
)
Rota(
    origem="São José",
    destino="UFPI",
    horario="07:00",
    duracao="50 min",
    preco="R$ 15,00",
    motorista="Maria Antônia",
    ponto_embarque="Posto Central (São José)",
    ponto_desembarque="Entrada Principal da UFPI (Picos)",
)
Rota(
    origem="Pio IX",
    destino="UFPI",
    horario="07:50",
    duracao="50 min",
    preco="R$ 16,00",
    motorista="Carlos Eduardo",
    ponto_embarque="Rodoviária de Pio IX",
    ponto_desembarque="Biblioteca da UFPI (Picos)",
)
