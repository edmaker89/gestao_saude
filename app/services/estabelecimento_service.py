from app.ext.database import db
from app.models import estabelecimento
from app.models.estabelecimento import Estabelecimento


class EstabelecimentoService:

    @staticmethod
    def list_all(orgao_id: int):
        """Lista todas os estabelecimentos"""
        return Estabelecimento.query.filter_by(orgao_id=orgao_id).order_by(Estabelecimento.nome).all()

    @staticmethod
    def get_by_nome(orgao_id: int, nome: str):
        """Busca uma organização pelo nome"""
        return Estabelecimento.query.filter_by(orgao_id=orgao_id, nome=nome).first()
    
    @staticmethod
    def get_by_id(id: int):
        """Busca uma organização pelo id"""
        return Estabelecimento.query.filter_by(id=id).first()

    @staticmethod
    def create(orgao_id: int, nome: str, id_responsavel: int | None = None):
        """Cria uma nova organização"""
        # Verifica se já existe uma organização com o nome ou sigla fornecidos
        if EstabelecimentoService.get_by_nome(orgao_id, nome):
            raise ValueError("Um estabelecimento nessa organização com esse nome já existe.")
        
        new_estabelecimento = Estabelecimento(
            orgao_id=orgao_id, # type: ignore
            nome=nome,  # type: ignore
            id_responsavel=id_responsavel # type: ignore
        )
        
        try:
            db.session.add(new_estabelecimento)
            db.session.commit()
            return new_estabelecimento
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao criar estabelecimento: {e}")
        
    @staticmethod
    def update(id: int, nome: str, orgao_id: int | None = None, id_responsavel: int | None = None):
        """Atualiza uma estabelecimento"""
        if len(Estabelecimento.query.filter_by(orgao_id=orgao_id, nome=nome).all()) > 1:
            raise ValueError("Um estabelecimento nessa organização com esse nome já existe.")
        
        estabelecimento: Estabelecimento = EstabelecimentoService.get_by_id(id) # type: ignore
        estabelecimento.nome = nome
        if orgao_id:
            estabelecimento.orgao_id = orgao_id
        
        
        estabelecimento.id_responsavel = id_responsavel
        
        try:
            db.session.commit()
            return estabelecimento
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao atualizar um estabelecimento: {e}")

    @staticmethod
    def inativar(id):
        """Inativa um estabelecimento pelo ID"""
        estabelecimento = Estabelecimento.query.get(id)
        if estabelecimento:
            try:
                estabelecimento.ativo = False
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(f"Erro ao inativar Estabelecimento: {e}")
        else:
            raise ValueError(f"Estabelecimento com ID {id} não encontrada.")
        
    @staticmethod
    def ativar(id):
        """Ativa uma Estabelecimento pelo ID"""
        estabelecimento = Estabelecimento.query.get(id)
        if estabelecimento:
            try:
                estabelecimento.ativo = True
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(f"Erro ao ativar Estabelecimento: {e}")
        else:
            raise ValueError(f"Estabelecimento com ID {id} não encontrada.")
        
    @staticmethod
    def e_responsavel(user_id, estabelecimento_id):
        estabelecimento = Estabelecimento.query.filter(Estabelecimento.id == estabelecimento_id, Estabelecimento.id_responsavel == user_id).first()
        if estabelecimento:
            return True
        return False
