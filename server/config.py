import os

class Config:
    SECRET_KEY = "miclaveultrasecreta123"        # 🔐 Necesaria para Flask
    JWT_SECRET_KEY = "miclaveultrasecreta123"    # 🔐 Clave usada para firmar/verificar tokens
    JWT_TOKEN_LOCATION = ["headers"]             # 🧠 Para usar Authorization: Bearer
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Micelular123@localhost/taximetro_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

