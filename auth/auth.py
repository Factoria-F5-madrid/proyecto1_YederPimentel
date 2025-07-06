import os
import json
import bcrypt # type: ignore
import jwt    # type: ignore
from datetime import datetime, timedelta

# --- Configurar ruta absoluta para users.json en la carpeta auth de la raíz del proyecto ---

# Ruta absoluta del directorio donde está este archivo (auth.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Subimos un nivel para llegar a la raíz del proyecto
ROOT_DIR = os.path.dirname(BASE_DIR)

# Ruta completa a users.json en la carpeta auth
USERS_FILE = os.path.join(ROOT_DIR, "auth", "users.json")

# Asegurar que la carpeta 'auth' existe (por si no está creada)
os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)

# --- Funciones para manejar usuarios ---

def load_users():
    if not os.path.isfile(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def register(username, password):
    users = load_users()
    if username in users:
        return False, "Usuario ya existe."
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = {"password": hashed}
    save_users(users)
    return True, "Usuario registrado correctamente."

def login(username, password):
    users = load_users()
    if username not in users:
        return False, "Usuario no encontrado."
    hashed = users[username]["password"].encode()
    if bcrypt.checkpw(password.encode(), hashed):
        token = create_token(username)
        return True, token
    else:
        return False, "Contraseña incorrecta."

# --- JWT ---

SECRET_KEY = "tu_clave_secreta_aqui"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

def create_token(username):
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True, payload["sub"]
    except jwt.ExpiredSignatureError:
        return False, "Token expirado."
    except jwt.InvalidTokenError:
        return False, "Token inválido."
