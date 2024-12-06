from app.ext.database import db

class ContratoItem(db.Model):
    __tablename__ = 'contrato_item'
    id = db.Column(db.Integer, primary_key=True)
    contrato_id = db.Column(db.String(255), db.ForeignKey('contrato.id'), nullable=False)
    item_id = db.Column(db.String(255), db.ForeignKey('item.id'), nullable=False)
    
    def __repr__(self):
        return f"ContratoItem (id={self.id}, contrato={self.contrato_id}"