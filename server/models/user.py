from db import db
import bcrypt # type: ignore

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.LargeBinary(60), nullable=False)

    def set_password(self, plain_password):
        self.password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, plain_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.password)
