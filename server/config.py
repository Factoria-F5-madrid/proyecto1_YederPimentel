import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:Micelular123@localhost/taximetro_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "tu_clave_secreta"  # para JWT si la usas
