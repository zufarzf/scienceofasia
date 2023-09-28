db_uri = {
    "sqlite": 'sqlite:///database.db',
    "postgresql": 'postgresql://postgres:##m+k6pXA8*MWh#^@localhost/casia',
}

class Config:
    SECRET_KEY = 'f209c0161f57da595219d0980851945efde1cc0cbd2eff1a368bbb58efd5'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ON_TEARDOWN = True


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = db_uri.get('postgresql')


class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = db_uri.get('postgresql')


config = {
    'default': DevConfig,

    'dev': DevConfig,
    'prod': ProdConfig
}
