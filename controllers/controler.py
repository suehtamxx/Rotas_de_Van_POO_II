usuarios = []

def cadastrar_usuario(nome, email, senha, telefone):
	for usuario in usuarios:
		if usuario['email'] == email:
			return False
	usuarios.append({
		'nome': nome,
		'email': email,
		'senha': senha,
		'telefone': telefone
	})
	return True

def validar_login(email, senha):
	for usuario in usuarios:
		if usuario['email'] == email and usuario['senha'] == senha:
			return True
	return False
