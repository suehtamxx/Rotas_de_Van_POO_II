import psycopg2
from controllers.config import load_config

"""Este arquivo gerencia a conexão com o banco de dados PostgreSQL."""


def connect(config):
    """Estabelece a conexão com o banco de dados PostgreSQL."""
    try:
        with psycopg2.connect(**config) as conn:
            print("Connected to the PostgreSQL server.")
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == "__main__":
    config = load_config()
    connect(config)
