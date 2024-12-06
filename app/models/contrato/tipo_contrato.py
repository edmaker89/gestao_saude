from app.ext.database import db

class TipoContrato(db.Model):
    __tablename__ = 'tipo_contrato'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"Tipo Contrato (id={self.id}, tipo={self.tipo}"