from sqlalchemy import and_, asc, desc, and_
from app.ext.database import db

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    descricao = db.Column(db.String(255))

    @classmethod
    def get_perfil(cls, id):
        perfil_existente = cls.query.filter_by(id=id).first()
        return perfil_existente

    @classmethod
    def novo_perfil(cls, nome, descricao=None):
        perfil = cls(nome=nome, descricao=descricao)
        db.session.add(perfil)
        db.session.commit()
        return perfil
    
    @classmethod
    def update_perfil(cls, id_perfil, nome=None, descricao=None):
        perfil = cls.get_perfil(id_perfil)
        try:
            if nome is not None:
                perfil.nome = nome
            if descricao is not None:
                perfil.descricao = descricao
            db.session.commit()
            return True
        except Exception as e:
            return False

    def delete_perfil(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False
    @classmethod
    def list_perfis(cls, ordem='asc', page=1, per_page=20):
        query = cls.query

        if ordem.lower() == 'asc':
            query = query.order_by(asc(cls.nome))
        elif ordem.lower() == 'desc':
            query = query.order_by(desc(cls.nome))
        
        perfis = query.paginate(page=page, per_page=per_page, error_out=False)

        return perfis
    


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    descricao = db.Column(db.String(255))

    @classmethod
    def get_permission(cls, id):
        permission_existente = cls.query.filter_by(id=id).first()
        return permission_existente

    @classmethod
    def new_permission(cls, nome, descricao=None):
        permission = cls(nome=nome, descricao=descricao)
        db.session.add(permission)
        db.session.commit()
        return permission
    
    def update_permission(self, nome=None, descricao=None):
        try:
            if nome is not None:
                self.nome = nome
            if descricao is not None:
                self.descricao = descricao
            db.session.commit()
            return True
        except Exception as e:
            return False

    def delete_permission(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False

    def __repr__(self):
        return f"<Permission {self.nome}>"
    
class RolePermissions(db.Model):
    __tablename__ = 'role_permissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)

    role = db.relationship('Role', backref='role_permissions', lazy=True)
    permission = db.relationship('Permission', backref='role_permissions', lazy=True)

    @classmethod
    def add_permission(cls, role_id, permission_id):

        add = cls(
            role_id=role_id,
            permission_id=permission_id
        )

        db.session.add(add)
        db.session.commit()

        return add
    
    @classmethod
    def remove_permission(cls, role_id, permission_id):

        remove = cls.query.filter(and_(cls.role_id==role_id, cls.permission_id==permission_id)).first()

        db.session.delete(remove)
        db.session.commit()

    def __repr__(self):
        return f"<RolePermission {self.id}>"
