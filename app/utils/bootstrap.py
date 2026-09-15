import logging
import os

from app.ext.database import db

logger = logging.getLogger(__name__)

SEED_ADMIN_NOME = "Administrador do Sistema"
SEED_ADMIN_USERNAME = "admin"
SEED_ADMIN_EMAIL = "admin@example.com"
SEED_ADMIN_PASSWORD = "Mudar@123"

PERMISSIONS = [
    ("gerenciamento master", "Acesso irrestrito ao sistema"),
    ("acesso restrito", "Acesso administrativo"),
    ("todas correspondencias", "Visualizar todas as correspondências"),
    ("regulacao", "Módulo de regulação"),
    ("pesquisa", "Módulo de pesquisa"),
    ("gestao de avisos", "Gerenciar avisos"),
    ("gerenciar permissão", "Gerenciar permissões de perfis"),
]

TIPOS_CORRESPONDENCIA = [
    ("Memorando", "Correspondência interna"),
    ("Ofício", "Comunicação oficial entre órgãos"),
    ("Despacho", "Decisão ou encaminhamento"),
    ("Portaria", "Ato normativo"),
]

MODEL_MODULES = [
    "app.models.users",
    "app.models.role_permissions",
    "app.models.departamento",
    "app.models.estabelecimento",
    "app.models.organizacao",
    "app.models.tipo_correspondencias",
    "app.models.correspondencias",
    "app.models.avisos",
    "app.models.token",
    "app.models.item",
    "app.models.contrato.base_contrato",
    "app.models.contrato.contrato",
    "app.models.contrato.contrato_item",
    "app.models.contrato.fornecedor",
    "app.models.contrato.lotacao_contrato",
    "app.models.contrato.solicitacao_contrato",
    "app.models.contrato.tipo_contrato",
    "app.models.dotacao.aplicacao_programada",
    "app.models.dotacao.conta",
    "app.models.dotacao.elemento_despesa",
    "app.models.dotacao.ficha",
    "app.models.dotacao.ficha_fonte",
    "app.models.dotacao.fonte",
    "app.models.dotacao.rubrica_orcamentaria",
    "app.models.edital.edital",
]


def _env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


def _import_models():
    import importlib

    for module in MODEL_MODULES:
        importlib.import_module(module)


def _seed():
    from app.models.users import Usuario
    from app.models.role_permissions import Role, Permission, RolePermissions
    from app.models.departamento import Departamento
    from app.models.estabelecimento import Estabelecimento
    from app.models.organizacao import Organizacao
    from app.models.tipo_correspondencias import TipoCorrespondencias
    from app.models.avisos import Avisos
    from werkzeug.security import generate_password_hash

    permissions = {}
    for nome, descricao in PERMISSIONS:
        permission = Permission(nome=nome, descricao=descricao)
        db.session.add(permission)
        permissions[nome] = permission
    db.session.flush()

    role = Role(nome="Master", descricao="Perfil administrador com acesso total")
    db.session.add(role)
    db.session.flush()

    for permission in permissions.values():
        db.session.add(RolePermissions(role_id=role.id, permission_id=permission.id))

    admin = Usuario(
        nome_completo=SEED_ADMIN_NOME,
        username=SEED_ADMIN_USERNAME,
        email=SEED_ADMIN_EMAIL,
        senha=generate_password_hash(SEED_ADMIN_PASSWORD),
        role=role.id,
        tentativas_login=0,
        bloqueado=False,
        ativo=True,
    )
    db.session.add(admin)
    db.session.flush()

    organizacao = Organizacao(
        nome="Secretaria Municipal de Saúde (exemplo)",
        sigla="SMS",
        id_responsavel=admin.id,
        ativo=True,
    )
    db.session.add(organizacao)
    db.session.flush()

    estabelecimento = Estabelecimento(
        nome="Sede (exemplo)",
        orgao_id=organizacao.id,
        id_responsavel=admin.id,
        ativo=True,
    )
    db.session.add(estabelecimento)
    db.session.flush()

    departamento = Departamento(
        nome="Administração (exemplo)",
        estabelecimento_id=estabelecimento.id,
        responsavel_id=admin.id,
        ativo=True,
    )
    db.session.add(departamento)
    db.session.flush()

    admin.departamento_id = departamento.id

    for tipo, descricao in TIPOS_CORRESPONDENCIA:
        db.session.add(TipoCorrespondencias(tipo=tipo, descricao=descricao))

    db.session.add(
        Avisos(
            titulo="Bem-vindo ao sistema",
            descricao="Utilize este espaço para se manter informado sobre avisos internos da Secretaria Municipal de Saúde.",
            autor=admin.id,
        )
    )

    db.session.commit()


def bootstrap(app):
    if not _env_bool("SEED_ON_EMPTY", True):
        return

    try:
        with app.app_context():
            _import_models()
            db.create_all()

            from app.models.users import Usuario

            if Usuario.query.first() is not None:
                logger.info("Banco já possui dados; bootstrap ignorado.")
                return

            try:
                _seed()
                logger.info("Dados mínimos criados com sucesso.")
            except Exception as exc:
                db.session.rollback()
                logger.warning("Falha ao criar dados mínimos: %s", exc)
    except Exception as exc:
        logger.warning("Falha no bootstrap de dados mínimos: %s", exc)
