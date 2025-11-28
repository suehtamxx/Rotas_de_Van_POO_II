import threading
from models.rotas import Rota
from controllers.client_rotas import (
    listar_rotas, 
    cadastrar_rota_api, 
    cadastrar_usuario_api, 
    login_api
)

# Variável para armazenar o usuário logado na sessão atual
usuario_atual = None

def carregar_dados_iniciais():
    """Chamado ao abrir o App para puxar rotas do servidor"""
    print(">>> (App): Buscando rotas no servidor Flask...")
    # Pega do servidor
    rotas_servidor = listar_rotas()
    
    # Atualiza a memória local do App
    if rotas_servidor:
        Rota.lista_de_rotas = rotas_servidor
        print(f">>> (App): {len(Rota.lista_de_rotas)} rotas carregadas.")
    else:
        print(">>> (App): Nenhuma rota encontrada ou erro de conexão.")


def cadastrar_usuario(nome, email, senha, telefone, tipo_usuario="cliente"):
    # Chama a API e retorna (True/False, Mensagem)
    sucesso, mensagem = cadastrar_usuario_api(nome, email, senha, telefone, tipo_usuario)
    return sucesso, mensagem

def validar_login(email, senha):
    global usuario_atual
    # Chama a API e retorna (True, Msg, ObjetoUsuario)
    sucesso, mensagem, usuario = login_api(email, senha)
    
    if sucesso and usuario:
        usuario_atual = usuario
        return usuario # Retorna o dicionário/objeto do usuário
    return None


def encontrar_rota_por_origem_destino(origem, destino):
    """
    Busca na lista local (Rota.lista_de_rotas) que já foi carregada do servidor.
    Usada pela barra de pesquisa da Tela Principal.
    """
    for rota in Rota.lista_de_rotas:
        if rota.origem.lower() == origem.lower() and rota.destino.lower() == destino.lower():
            return rota
    return None

def cadastrar_nova_rota(origem, destino, horario, duracao, preco, motorista, ponto_embarque, ponto_desembarque):
    """
    Cria a rota localmente e envia para o servidor em background.
    """
    # 1. Cria objeto Rota (para aparecer na tela imediatamente)
    nova_rota = Rota(origem, destino, horario, duracao, preco, motorista, ponto_embarque, ponto_desembarque)
    
    # 2. Adiciona na lista local (visual)
    Rota.lista_de_rotas.append(nova_rota)

    # 3. Função interna para rodar na Thread (não travar a tela)
    def _enviar_para_api():
        print(">>> (Thread): Enviando rota para o servidor...")
        sucesso = cadastrar_rota_api(nova_rota)
        if sucesso:
            print(">>> (Thread): Rota sincronizada com sucesso no Banco de Dados.")
        else:
            print(">>> (Thread): Erro ao salvar rota no servidor (mas ela aparece localmente).")

    # Inicia a thread
    t = threading.Thread(target=_enviar_para_api)
    t.start()
    
    return True

# Carrega as rotas assim que o controler é importado pelo App
carregar_dados_iniciais()