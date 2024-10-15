from datetime import datetime
from app.ext.database import db

class Departamento(db.Model):
    __tablename__ = 'departamento'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    estabelecimento_id = db.Column(db.Integer, db.ForeignKey('estabelecimento.id'), nullable=False)
    responsavel_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    responsavel = db.relationship('Usuario', backref='departamentos_responsavel', foreign_keys=[responsavel_id])
    # users = db.relationship('Usuario', backref='departamento', foreign_keys='Usuario.departamento_id') #qualquer coisa tira

    @classmethod
    def new_depart(cls, departamento):
        try:
            novo_departamento = cls()
            novo_departamento.nome = departamento
            novo_departamento.ativo = True

            db.session.add(novo_departamento)
            db.session.commit()

            return novo_departamento
        except Exception as e:
            print(e)
            return False
    
    @classmethod
    def update(cls, departamento_id, departamento_nome):

        try:
            departamento = cls.query.filter(cls.id == departamento_id).first()
            departamento.nome = departamento_nome #type: ignore
            db.session.commit()

            return departamento
        except Exception as e:
            return False

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_departamento(cls, id_depart):
        departamento = cls.query.filter(cls.id==id_depart).first()
        return departamento
        
    def __repr__(self):
        return f"<Departamento {self.nome}>"