class Rota():
	rotas = []  # Lista de rotas disponíveis
	def __init__(self, nome, paradas, horario):
		self.nome = nome
		self.paradas = paradas
		self.horario = horario
		Rota.rotas.append(self)

	def __str__(self):
		return f"{self.nome} - {self.horario}"
