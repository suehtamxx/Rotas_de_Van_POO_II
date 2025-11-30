import requests
from models.rotas import Rota

"""Este arquivo faz as requisições HTTP do cliente para o servidor."""

base_url = "http://127.0.0.1:5000"


def listar_rotas():
    """
    Faz requisição GET ao servidor para obter a lista de rotas e converte para objetos Rota.
    """
    try:
        response = requests.get(f"{base_url}/rotas")
        if response.status_code == 200:
            lista_json = response.json()
            objetos_rotas = []
            for rota in lista_json:
                # O banco retorna uma tupla. As novas colunas estão no final (índices 9 e 10).
                # Verificamos o tamanho para evitar erros em bases antigas sem essas colunas.
                paradas = rota[9] if len(rota) > 9 else ""
                dias = rota[10] if len(rota) > 10 else ""

                r = Rota(
                    id=rota[0],
                    origem=rota[1],
                    destino=rota[2],
                    horario=rota[3],
                    duracao=rota[4],
                    preco=rota[5],
                    motorista=rota[6],
                    ponto_embarque=rota[7],
                    ponto_desembarque=rota[8],
                    paradas=paradas,
                    dias_disponiveis=dias,
                )
                objetos_rotas.append(r)
            return objetos_rotas
        else:
            print(f"Erro ao listar rotas: {response.status_code}")
            return []
    except requests.exceptions.ConnectionError as e:
        print(f"Erro ao conectar ao servidor: {e}")
        return []


def cadastrar_rota_api(rota_obj):
    """
    Faz requisição POST ao servidor para enviar os dados de uma nova rota.
    """
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
        print("Não foi possivel conectar ao servidor.")
        return False, "Erro de conexão."


def cadastrar_usuario_api(nome, email, senha, telefone, tipo_usuario):
    """
    Faz requisição POST ao servidor para cadastrar um novo usuário.
    """
    dados = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "telefone": telefone,
        "tipo_usuario": tipo_usuario,
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
    """
    Faz requisição POST ao servidor para autenticar um usuário e receber seus dados.
    """
    try:
        response = requests.post(
            f"{base_url}/usuarios/login", json={"email": email, "senha": senha}
        )

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
