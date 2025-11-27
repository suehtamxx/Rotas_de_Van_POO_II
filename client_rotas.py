import requests
from models.rotas import Rota

base_url = 'http://127.0.01:5000'
def listar_rotas():
	try:
		response = requests.get(f"{base_url}/rotas")
		if response.status_code == 200:
			lista_json = response.json()
			objetos_rotas = []
			for rota in lista_json:
				nova_rota = Rota(rota['origem'], rota['destino'], rota['horario'], rota['duracao'], rota['preco'], rota['motorista'], rota['ponto_embarque'], rota['ponto_desembarque'])
				objetos_rotas.append(nova_rota)
			return objetos_rotas
		else:
			print(f"Erro ao listar rotas: {response.status_code}")
			return []
	except requests.exceptions.ConnectionError as e:
		print(f"Erro ao conectar ao servidor: {e}")
		return []
	
def cadastrar_rota_api(rota_obj):
	dados = rota_obj.to_dict()
	try:
		response = requests.get(f"{base_url}/rotas", json=dados)
		return response.status_code == 201
	except requests.exceptions.ConnectionError:
		print("Erro de conexão ao tentar cadastrar.")
		return False

