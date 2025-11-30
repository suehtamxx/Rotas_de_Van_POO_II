import threading
from models.rotas import Rota
from controllers.client_rotas import (
    listar_rotas,
    cadastrar_rota_api,
    cadastrar_usuario_api,
    login_api,
)

"""Este arquivo gerencia a lógica de negócio do lado do cliente (App)."""

usuario_atual = None


def carregar_dados_iniciais():
    """Chamado ao abrir o App para puxar rotas do servidor"""
    print(">>> (App): Buscando rotas no servidor Flask...")
    rotas_servidor = listar_rotas()

    if rotas_servidor:
        Rota.lista_de_rotas = rotas_servidor
        print(f">>> (App): {len(Rota.lista_de_rotas)} rotas carregadas.")
    else:
        print(">>> (App): Nenhuma rota encontrada ou erro de conexão.")


def cadastrar_usuario(nome, email, senha, telefone, tipo_usuario="cliente"):
    """
    Intermediário que envia os dados de cadastro da View para a API.
    """
    sucesso, mensagem = cadastrar_usuario_api(
        nome, email, senha, telefone, tipo_usuario
    )
    return sucesso, mensagem


def validar_login(email, senha):
    """Gerencia o processo de login: chama a API e salva a sessão do usuário localmente."""
    global usuario_atual
    sucesso, mensagem, usuario = login_api(email, senha)

    if sucesso and usuario:
        usuario_atual = usuario
        return usuario
    return None


def encontrar_rotas_por_origem_destino(origem, destino):
    """
    Busca na lista local e retorna TODAS as rotas correspondentes.
    """
    resultados = []
    for rota in Rota.lista_de_rotas:
        if (
            rota.origem.lower().strip() == origem.lower().strip()
            and rota.destino.lower().strip() == destino.lower().strip()
        ):
            resultados.append(rota)
    return resultados


def cadastrar_nova_rota(
    origem,
    destino,
    horario,
    duracao,
    preco,
    motorista,
    ponto_embarque,
    ponto_desembarque,
    paradas,
    dias_disponiveis,
):
    """
    Cria a rota localmente e envia para o servidor em background.
    """
    # 1. Cria objeto Rota (O __init__ já adiciona na lista local)
    nova_rota = Rota(
        origem,
        destino,
        horario,
        duracao,
        preco,
        motorista,
        ponto_embarque,
        ponto_desembarque,
        paradas,
        dias_disponiveis,
    )

    # 2. Thread para salvar no banco
    def _enviar_para_api():
        print(">>> (Thread): Enviando rota para o servidor...")
        sucesso, msg = cadastrar_rota_api(nova_rota)
        if sucesso:
            print(">>> (Thread): Rota sincronizada com sucesso no Banco de Dados.")
        else:
            print(f">>> (Thread): Erro ao salvar rota no servidor: {msg}")

    t = threading.Thread(target=_enviar_para_api)
    t.start()

    return True


# Carrega as rotas assim que o controler é importado pelo App
carregar_dados_iniciais()
