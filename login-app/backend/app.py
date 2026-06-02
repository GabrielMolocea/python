from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import hashlib

app = Flask(__name__)
CORS(app)


SECRET_KEY = "super-secret-dev-key-change-in-production"
TOKEN_EXPIRY_SECONDS = 60  # 1 minute

# Mock user database (password is sha256 of the plain text)
USERS = {
    "alice": hashlib.sha256("password123".encode()).hexdigest(),
    "bob":   hashlib.sha256("hunter2".encode()).hexdigest(),
}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token(username: str) -> str:
    payload = {
        "sub": username,
        "iat": datetime.now().isoformat(),
        "exp": datetime.now().isoformat() + datetime.timedelta(seconds=TOKEN_EXPIRY_SECONDS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def 
