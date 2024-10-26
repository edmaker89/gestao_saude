from app.models import *
from app.models.departamento import Departamento
from app.models.organizacao import Organizacao
from app.models.estabelecimento import Estabelecimento
from app.ext.database import db

Organizacao.estabelecimentos = db.relationship('Estabelecimento', backref='organizacao', cascade="all, delete-orphan")