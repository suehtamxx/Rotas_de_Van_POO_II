usuarios = []


def cadastrar_usuario(nome, email, senha, telefone):
    for usuario in usuarios:
        if usuario["email"] == email:
            return False
    usuarios.append(
        {"nome": nome, "email": email, "senha": senha, "telefone": telefone}
    )
    return True


def validar_login(email, senha):
    for usuario in usuarios:
        if usuario["email"] == email and usuario["senha"] == senha:
            return usuario
    return None


from models.rotas import Rota


def encontrar_rota_por_origem_destino(origem, destino):

    for rota in Rota.lista_de_rotas:
        if (
            rota.origem.lower() == origem.lower()
            and rota.destino.lower() == destino.lower()
        ):
            return rota
    return None
