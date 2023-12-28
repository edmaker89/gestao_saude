from flask import g
from flask_login import current_user
from app.models.role_permissions import RolePermission

def permission_processor():
    permissions = set()

    if current_user.is_authenticated:
        role_id = current_user.role.id
        role_permissions = RolePermission.query.filter_by(role_id=role_id).all()
        permissions = {rp.permission.nome for rp in role_permissions}

    return {'user_permissions': permissions}

def inject_permissions():
    return permission_processor()

