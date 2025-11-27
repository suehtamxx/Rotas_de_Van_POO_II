import json
import threading
from models.rotas import Rota

usuarios = []
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_ROTAS = "rotas.json"


# --- Funções de Usuário  ---
def salvar_usuarios_em_arquivo(lista_de_usuarios):

    try:
        with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
            json.dump(lista_de_usuarios, f, indent=4)
        print(">>> (Thread): Usuários salvos com sucesso.")
    except Exception as e:
        print(f">>> (Thread): Erro ao salvar usuários: {e}")

def carregar_usuarios_do_arquivo():
    """Tenta carregar os usuários do arquivo JSON no início."""
    global usuarios
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            usuarios_carregados = json.load(f)
            
        usuarios = []
        for u in usuarios_carregados:
            if "tipo_usuario" not in u:
                u["tipo_usuario"] = "cliente"
            usuarios.append(u)

        print(f">>> (App): {len(usuarios)} usuários carregados.")
    except FileNotFoundError:
        print(
            ">>> (App): Arquivo de usuários não encontrado. Começando com lista vazia."
        )
        usuarios = []
    except json.JSONDecodeError:
        print(">>> (App): Erro ao ler o arquivo JSON. Começando com lista vazia.")
        usuarios = []


def cadastrar_usuario(nome, email, senha, telefone, tipo_usuario):
    for usuario in usuarios:
        if usuario["email"] == email:
            return False

    novo_usuario = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "telefone": telefone,
        "tipo_usuario": tipo_usuario,
    }

    usuarios.append(novo_usuario)

    print(">>> (GUI): Iniciando thread para salvar usuários...")
    lista_para_salvar = list(usuarios)

    thread_de_salvamento = threading.Thread(
        target=salvar_usuarios_em_arquivo, args=(lista_para_salvar,)
    )
    thread_de_salvamento.start()

    return True


def validar_login(email, senha):
    for usuario in usuarios:
        if usuario["email"] == email and usuario["senha"] == senha:
            if "tipo_usuario" not in usuario:
                usuario["tipo_usuario"] = "cliente"
            return usuario
    return None


# --- Funções de Rota ---
def encontrar_rota_por_origem_destino(origem, destino):
    for rota in Rota.lista_de_rotas:
        if (
            rota.origem.lower() == origem.lower()
            and rota.destino.lower() == destino.lower()
        ):
            return rota
    return None


def salvar_rotas_em_arquivo(lista_de_rotas):

    try:
        lista_para_salvar = [rota.to_dict() for rota in lista_de_rotas]

        with open(ARQUIVO_ROTAS, "w", encoding="utf-8") as f:
            json.dump(lista_para_salvar, f, indent=4)
        print(">>> (Thread): Rotas salvas com sucesso.")
    except Exception as e:
        print(f">>> (Thread): Erro ao salvar rotas: {e}")


def carregar_rotas_do_arquivo():
    try:
        with open(ARQUIVO_ROTAS, "r", encoding="utf-8") as f:
            rotas_carregadas = json.load(f)

        Rota.lista_de_rotas = []
        for r_dict in rotas_carregadas:
            nova_rota = Rota(
                origem=r_dict["origem"],
                destino=r_dict["destino"],
                horario=r_dict["horario"],
                duracao=r_dict["duracao"],
                preco=r_dict["preco"],
                motorista=r_dict["motorista"],
                ponto_embarque=r_dict["ponto_embarque"],
                ponto_desembarque=r_dict["ponto_desembarque"],
            )
            Rota.lista_de_rotas.append(nova_rota)

        print(f">>> (App): {len(Rota.lista_de_rotas)} rotas carregadas.")
    except FileNotFoundError:
        print(">>> (App): Arquivo de rotas não encontrado. Começando com lista vazia.")
        Rota.lista_de_rotas = []
    except json.JSONDecodeError:
        print(
            ">>> (App): Erro ao ler o arquivo JSON de rotas. Começando com lista vazia."
        )
        Rota.lista_de_rotas = []


def cadastrar_nova_rota(
    origem,
    destino,
    horario,
    duracao,
    preco,
    motorista,
    ponto_embarque,
    ponto_desembarque,
):
    """
    Cria uma nova rota, adiciona na lista e inicia thread para salvar.
    """
    nova_rota = Rota(
        origem=origem,
        destino=destino,
        horario=horario,
        duracao=duracao,
        preco=preco,
        motorista=motorista,
        ponto_embarque=ponto_embarque,
        ponto_desembarque=ponto_desembarque,
    )
    Rota.lista_de_rotas.append(nova_rota)

    print(">>> (GUI): Iniciando thread para salvar rotas...")
    lista_para_salvar = list(Rota.lista_de_rotas)

    thread_de_salvamento = threading.Thread(
        target=salvar_rotas_em_arquivo, args=(lista_para_salvar,)
    )
    thread_de_salvamento.start()

    return True


carregar_usuarios_do_arquivo()
carregar_rotas_do_arquivo()
