import psycopg2
from controllers.config import load_config

"""Este arquivo cria as tabelas necessárias no banco de dados PostgreSQL."""


def create_tables():
    commands = (
        """
	        CREATE TABLE IF NOT EXISTS rotas (
		        id SERIAL PRIMARY KEY,
		        origem VARCHAR(15) NOT NULL,
				destino VARCHAR(15) NOT NULL,
				horario VARCHAR(6) NOT NULL,
				duracao VARCHAR(5),
				preco REAL NOT NULL,
				motorista VARCHAR(30) NOT NULL,
				ponto_embarque VARCHAR(50) NOT NULL,
				ponto_desembarque VARCHAR(50) NOT NULL,
				paradas VARCHAR(255),
				dias_disponiveis VARCHAR(100)
		)""",
        """
			CREATE TABLE IF NOT EXISTS usuarios (
			    id SERIAL PRIMARY KEY,
				nome VARCHAR(40) NOT NULL,
				email VARCHAR(40) NOT NULL,
				senha VARCHAR(255) NOT NULL,
				telefone VARCHAR(15) NOT NULL,
				tipo_usuario VARCHAR(15)
		)""",
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
                print("Tabelas verificadas/criadas com sucesso.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Erro ao criar tabelas: {error}")


if __name__ == "__main__":
    create_tables()
