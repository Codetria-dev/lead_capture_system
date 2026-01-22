from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instância do SQLAlchemy (será inicializada no app.py)
db = SQLAlchemy()


class Lead(db.Model):
    """Modelo para armazenar os leads capturados"""
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    empresa = db.Column(db.String(100))
    mensagem = db.Column(db.Text)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Lead {self.nome}>'
    
    def to_dict(self):
        """Converte o lead para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'empresa': self.empresa,
            'mensagem': self.mensagem,
            'data_cadastro': self.data_cadastro.strftime('%d/%m/%Y %H:%M:%S')
        }
