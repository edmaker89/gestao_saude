from app.ext.database import db
from app.models.dotacao.fonte import Fonte


class FonteService:
    @staticmethod
    def get_all():
        """Retorna todas as fontes de recursos"""
        return Fonte.query.all()
    
    @staticmethod
    def get_by_id(id):
        """Retorna uma fonte de recursos pelo id"""
        return Fonte.query.get(id)
    
    @staticmethod
    def get_by_codigo(codigo):
        """Retorna uma fonte de recursos pelo codigo"""
        return Fonte.query.filter_by(codigo=codigo).first()
    
    @staticmethod
    def create(codigo: str, descricao: str | None = None):
        """Cria uma nova fonte de recursos"""
        fonte = Fonte()
        fonte.codigo = codigo
        if descricao:
            fonte.descricao = descricao
        db.session.add(fonte)
        db.session.commit()
        return fonte
    
    @staticmethod
    def update(id_fonte: int, codigo: str | None = None, descricao: str | None = None):
        """Atualiza uma fonte de recursos pelo id"""
        fonte: Fonte | None = FonteService.get_by_id(id_fonte)
        if fonte is None:
            raise Exception("Fonte nao encontrada")
        if codigo is not None:
            fonte.codigo = codigo
        if descricao is not None:
            fonte.descricao = descricao
        db.session.commit()
        return True
    