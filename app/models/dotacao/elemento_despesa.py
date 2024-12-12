from app.ext.database import db

class ElementoDespesa(db.Model):
    __tablename__ = 'elemento_despesa'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return '<ElementoDespesa %r>' % self.id