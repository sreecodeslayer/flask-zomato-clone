import os


class Development:
    DEBUG = True
    SECRET_KEY = "changeme"
    HOST = os.getenv('MONGO_HOST', 'localhost')
    PORT = os.getenv('MONGO_PORT', 27017)
    DB = os.getenv('MONGO_DB', 'FOOGG')

    MONGODB_SETTINGS = [{
        'db': DB,
        'host': HOST,
        'port': PORT
    }]


class Production(Development):
    DEBUG = False
    SECRET_KEY = "sup3rs3cr3tk3yf0rPr0duct10N"
    HOST = os.getenv('MONGO_HOST', 'localhost')
    PORT = os.getenv('MONGO_PORT', 27017)
    DB = os.getenv('MONGO_DB', 'FOOGG')

    MONGODB_SETTINGS = [{
        'db': DB,
        'host': HOST,
        'port': PORT
    }]


configuration = {
    'dev': Development,
    'production': Production
}
