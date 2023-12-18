from app.ext.database import db

class TipoCorrespondencias(db.Model):
    __tablename__ = 'tipo_correspondencias'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)

    def __repr__(self):
        return f"<TipoCorrespondencia {self.tipo}>"