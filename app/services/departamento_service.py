from app.ext.database import db
from app.models.departamento import Departamento


class DepartamentoService:

    @staticmethod
    def list_all_by_estab(estabelecimento_id: int):
        """Lista todos os departamentos"""
        return Departamento.query.filter_by(estabelecimento_id=estabelecimento_id).order_by(Departamento.nome).all()

    @staticmethod
    def get_by_nome_by_estab(estabelecimento_id: int, nome: str):
        """Busca um departamento pelo nome"""
        return Departamento.query.filter_by(estabelecimento_id=estabelecimento_id, nome=nome).first()
    
    @staticmethod
    def get_by_id(id: int):
        """Busca um departamento pelo id"""
        return Departamento.query.filter_by(id=id).first()

    @staticmethod
    def create(estabelecimento_id: int, nome: str, id_responsavel: int | None = None):
        """Cria um novo departamento"""
        # Verifica se já existe uma organização com o nome ou sigla fornecidos
        if DepartamentoService.get_by_nome_by_estab(estabelecimento_id, nome):
            raise ValueError("Um Departamento nesse estabelecimento com esse nome já existe.")
        
        new_departamento = Departamento(
            estabelecimento_id = estabelecimento_id, # type: ignore
            nome=nome,  # type: ignore
            responsavel_id=id_responsavel # type: ignore
        )
        
        try:
            db.session.add(new_departamento)
            db.session.commit()
            return new_departamento
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao criar departamento: {e}")
        
    @staticmethod
    def update(id: int, nome: str, estabelecimento_id: int | None = None, id_responsavel: int | None = None):
        """Atualiza um departamento"""
        if len(Departamento.query.filter_by(estabelecimento_id=estabelecimento_id, nome=nome).all()) > 1:
            raise ValueError("Um departamento nesse estabecimento com esse nome já existe.")
        
        estabelecimento: Departamento = DepartamentoService.get_by_id(id) # type: ignore
        estabelecimento.nome = nome
        
        if estabelecimento_id:
            estabelecimento.estabelecimento_id = estabelecimento_id
            
        if id_responsavel:
            estabelecimento.responsavel_id = id_responsavel
        
        try:
            db.session.commit()
            return estabelecimento
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao atualizar um departamento: {e}")

    @staticmethod
    def inativar(id):
        """Inativa um departamento pelo ID"""
        estabelecimento = Departamento.query.get(id)
        if estabelecimento:
            try:
                estabelecimento.ativo = False
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(f"Erro ao inativar um departamento: {e}")
        else:
            raise ValueError(f"Departamento com ID {id} não encontrada.")
        
    @staticmethod
    def ativar(id):
        """Ativa um Departamento pelo ID"""
        estabelecimento = Departamento.query.get(id)
        if estabelecimento:
            try:
                estabelecimento.ativo = True
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(f"Erro ao ativar departamento: {e}")
        else:
            raise ValueError(f"Departamento com ID {id} não encontrada.")
