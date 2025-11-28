import requests
from models.rotas import Rota

base_url = 'http://127.0.0.1:5000'
def listar_rotas():
	try:
		response = requests.get(f"{base_url}/rotas")
		if response.status_code == 200:
			lista_json = response.json()
			objetos_rotas = []
			for rota in lista_json:
				r = Rota(origem=rota[1], destino=rota[2], horario=rota[3], duracao=rota[4], preco=rota[5],
			 	motorista=rota[6], ponto_embarque=rota[7], ponto_desembarque=rota[8], id=rota[0])
				objetos_rotas.append(r)
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
		response = requests.post(f"{base_url}/rotas", json=dados)
		
		if response.status_code == 201:
			return True, "Rota cadastrada com sucesso."
		else:
			try:
				msg_erro = response.json().get("erro", "Erro desconhecido no servidor.")
			except:
				msg_erro = f"erro {response.status_code}"
			return False, msg_erro
	except requests.exceptions.ConnectionError:
		return False, print("Não foi possivel conectar ao servidor.")
		

def cadastrar_usuario_api(nome, email, senha, telefone, tipo_usuario):
	dados = {
		"nome": nome, "email": email, "senha": senha, "telefone": telefone, "tipo_usuario": tipo_usuario
	}
	try:
		response = requests.post(f"{base_url}/usuarios/cadastro", json=dados)

		if response.status_code == 201:
			return True, "Usuario cadastrado com sucesso."
		else:
			try:
				msg_erro = response.json().get("erro", "Erro desconhecido no servidor.")
			except:
				msg_erro = f"erro {response.status_code}"
			return False, msg_erro
	except requests.exceptions.ConnectionError:
		return False, "Não foi possivel conectar ao servidor."

def login_api(email, senha):
	try:
		response = requests.post(f"{base_url}/usuarios/login", json={"email": email, "senha": senha})

		if response.status_code == 200:
			dados = response.json()

			return True, "Login realizado", dados.get("usuario")
		else:
			try:
				msg_erro = response.json().get("erro", "Erro de autenticação.")
			except:
				msg_erro = "Erro ao tentar logar."
			return False, msg_erro, None
	except requests.exceptions.ConnectionError:
		return False, "Erro de conexão com o servidor.", None
	

