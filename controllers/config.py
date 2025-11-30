from configparser import ConfigParser

"""Este arquivo lê o arquivo de configuração .ini para obter parâmetros do banco de dados."""


def load_config(filename="database.ini", section="postgresql"):
    """
    Lê o arquivo .ini e retorna um dicionário com os parâmetros de conexão do banco de dados.
    """
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]

    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return config


if __name__ == "__main__":
    config = load_config()
    print(config)
