from flask import Flask, jsonify, request
import psycopg2
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

if __name__ == '__main__':
    app.run(debug=True)

