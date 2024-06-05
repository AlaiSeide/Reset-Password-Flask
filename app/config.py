import os

class Config:
    SECRET_KEY = os.urandom(24)  # Chave secreta para proteger o aplicativo
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Banco de dados SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desativa o rastreamento de modificações
    MAIL_SERVER = 'smtp.googlemail.com'  # Servidor de email
    MAIL_PORT = 587  # Porta do servidor de email
    MAIL_USE_TLS = True  # Usar TLS para segurança
    MAIL_USERNAME = os.getenv('EMAIL_USER')  # Nome de usuário do email
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')  # Senha do email
