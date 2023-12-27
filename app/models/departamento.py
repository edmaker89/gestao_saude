from app.ext.database import db

class Departamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False)

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
        
    def __repr__(self):
        return f"<Departamento {self.nome}>"