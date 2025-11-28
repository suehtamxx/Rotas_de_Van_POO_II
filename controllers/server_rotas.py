from flask import Flask, jsonify, request
import psycopg2
import re
from werkzeug.security import generate_password_hash, check_password_hash
from config import load_config

app = Flask(__name__)

def get_db_connection():
	config = load_config()
	conn = psycopg2.connect(**config)
	return conn			

@app.route('/rotas', methods=['GET'])
def listar_rotas():
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute('select * from rotas;')
	rotas = cur.fetchall()
	cur.close()
	conn.close()
	return jsonify(rotas)

@app.route('/rotas', methods=['POST'])
def criar_rota():
	nova_rota = request.get_json()
	conn = get_db_connection()
	cur = conn.cursor()
	sql_insert = """
		insert into rotas (origem, destino, horario, duracao, preco, motorista, ponto_embarque, ponto_desembarque)
		values (%s, %s, %s, %s, %s, %s, %s, %s)
		"""
	cur.execute(sql_insert, (
		nova_rota["origem"],
		nova_rota["destino"],
		nova_rota["horario"],
		nova_rota["duracao"],
		nova_rota["preco"],
		nova_rota["motorista"],
		nova_rota["ponto_embarque"],
		nova_rota["ponto_desembarque"],
	))
	
	conn.commit()
	cur.close()
	conn.close()
	
	return jsonify({"message": "Rota criada."}), 201

@app.route('/rotas/search', methods=['GET'])
def search_rota():
	conn = get_db_connection()
	cur = conn.cursor()

	origem = request.args.get('origem')
	destino = request.args.get('destino')
	if not origem or not destino:
		return jsonify({"erro": "Preencha os campos de origem e destino."}), 400
	
	cur.execute('select * from rotas where origem ILIKE %s and destino ILIKE %s;', (origem, destino))
	rotas = cur.fetchall()

	cur.close()
	conn.close()

	return jsonify(
		{
			"origem": origem, 
			"destino": destino, 
			"horario": rotas[0][3]
		})

@app.route('/rotas/<int:id>', methods=['DELETE'])
def delete_rota(id):
	conn = get_db_connection()
	cur = conn.cursor()

	cur.execute('delete from rotas where id = %s;', (id,))
	row = cur.rowcount

	conn.commit()
	cur.close()
	conn.close()
	if row > 0:
		return jsonify({"message": "Rota excluida."}), 200
	elif row == 0:
		return jsonify({"message": "Nenhuma rota foi excluida."}), 404

@app.route('/usuarios/cadastro', methods=['POST'])
def add_usuario():
	novo_user = request.get_json()
	
	nome = novo_user.get('nome')
	email = novo_user.get('email')
	senha = novo_user.get('senha')
	telefone = novo_user.get('telefone')
	tipo = novo_user.get('tipo_usuario', 'cliente')

	if not validar_email(email):
		return jsonify({"erro": "Email invalido."}), 400
	if not validar_senha(senha):
		return jsonify({"erro": "Senha fraca. Minimo 8 caracteres com letras e numeros."}), 400
	
	conn = get_db_connection()
	cur = conn.cursor()

	cur.execute('select id from usuarios where email = %s', (email,))
	if cur.fetchone():
		cur.close()
		conn.close()
		return jsonify({"erro": "Email ja cadastrado"}), 409
	
	senha_hash = generate_password_hash(senha)

	sql = "insert into usuarios (nome, email, senha, telefone, tipo_usuario) values (%s, %s, %s, %s, %s)"
	cur.execute(sql, (nome, email, senha_hash, telefone, tipo))

	conn.commit()
	cur.close()
	conn.close()

	return jsonify({"message": "Usuário criado."}), 201

@app.route('/usuarios/login', methods=['POST'])
def login_user():
	dados = request.get_json()
	email = dados.get('email')
	senha_digitada = dados.get('senha')

	conn = get_db_connection()
	cur = conn.cursor()

	cur.execute('select nome, email, senha, telefone, tipo_usuario from usuarios where email = %s', (email,))
	usuario = cur.fetchone()

	cur.close()
	conn.close()

	if usuario:
		hash_salvo = usuario[2]
		if check_password_hash(hash_salvo, senha_digitada):
			return jsonify({
				"message": "Login realizado",
				"usuario": {
					"nome": usuario[0],
					"email": usuario[1],
					"telefone": usuario[3],
					"tipo_usuario": usuario[4]
				}
			}), 200
	
	return jsonify({"erro": "Email ou senha incorreto"}), 401

def validar_email(email):
	"""Funcao para validar email usando o regex."""
	padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
	return re.match(padrao, email)

def validar_senha(senha):
	"""
	Funcao para validar senha usando regex
	Deve ter no minimo 8 caracteres e pelo menos uma letra
	e um numero.
	"""
	if len(senha) < 8: # verifica o tamanho
		return False
	if not re.search(r"[a-z]", senha): # verifica se tem letra
		return False
	if not re.search(r"[0-9]", senha): # verfica se tem numero
		return False
	return True

if __name__ == '__main__':
    app.run(debug=True)

