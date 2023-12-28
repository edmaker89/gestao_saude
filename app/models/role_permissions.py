from app.ext.database import db

class Perfil(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    
    # Adicione uma relação para associar usuários aos perfis
    # usuarios = db.relationship('Usuario', backref='perfil', lazy=True)

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    descricao = db.Column(db.String(255))

    def __repr__(self):
        return f"<Permission {self.nome}>"
    
class RolePermission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), nullable=False)

    # role = db.relationship('Role', backref='role_permissions', lazy=True)
    # permission = db.relationship('Permission', backref='role_permissions', lazy=True)

    def __repr__(self):
        return f"<RolePermission {self.id}>"
