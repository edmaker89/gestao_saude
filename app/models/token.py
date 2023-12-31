from app.ext.database import db
from datetime import datetime, timedelta


class Token(db.Model):
    __tablename__= 'Token'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), nullable=False, unique=True)
    expiration_date = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=30))

    @classmethod
    def salvar_token_no_banco(cls, user_id, token):
        # Crie uma nova instância de Token
        novo_token = cls(user_id=user_id, token=token)

        # Adicione ao banco de dados
        db.session.add(novo_token)
        db.session.commit()

    @classmethod
    def token_valido(cls, token):
        """
        Verifica se um token é válido, ou seja, se existe na base de dados
        e se ainda não expirou.
        """
        print(token)
        print(datetime.utcnow())
        token_validado = cls.query.filter(cls.token == token).first()
        print(token_validado.user_id)
        print(token_validado)
        return token_validado