from flask_login import current_user
from app.models.role_permissions import Permission, RolePermissions
from functools import wraps
from flask import abort, redirect, url_for

def verify_permission(permission):
    # Verifica se o usuário está autenticado
    if current_user.is_authenticated:
        # Obtém o ID do papel (role) do usuário
        role_id = current_user.role
        # Consulta a tabela role_permissions para verificar se há uma correspondência
        # entre o ID do papel, a ID da permissão e o nome da permissão
        result = RolePermissions.query.join(Permission).filter(
            RolePermissions.role_id == role_id,
            Permission.nome == permission
        ).first()

        if result:
            return True

    return False


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Verifica se o usuário tem a permissão
            if not verify_permission(permission):
                # Se não tiver, redireciona para uma página de acesso negado
                # ou realiza outra ação apropriada (por exemplo, abort(403))
                return redirect(abort(403))  # Substitua 'acesso_negado' pela rota apropriada

            # Se tiver a permissão, continua com a execução da função
            return func(*args, **kwargs)

        return wrapper

    return decorator

