from typing import List
from app.ext.database import db
from app.models.organizacao import Organizacao


class OrganizacaoService:

    @staticmethod
    def list_all():
        """Lista todas as organizações"""
        return Organizacao.query.order_by(Organizacao.nome).all()

    @staticmethod
    def get_by_nome(nome: str):
        """Busca uma organização pelo nome"""
        return Organizacao.query.filter_by(nome=nome).first()
    
    @staticmethod
    def get_by_sigla(sigla: str):
        """Busca uma organização pela sigla"""
        return Organizacao.query.filter_by(sigla=sigla).first()
    
    @staticmethod
    def get_by_id(id: int):
        """Busca uma organização pelo id"""
        return Organizacao.query.filter_by(id=id).first()

    @staticmethod
    def create(nome: str, sigla: str, id_responsavel: int | None = None):
        """Cria uma nova organização"""
        # Verifica se já existe uma organização com o nome ou sigla fornecidos
        if OrganizacaoService.get_by_nome(nome):
            raise ValueError("Uma organização com esse nome já existe.")
        
        if OrganizacaoService.get_by_sigla(sigla):
            raise ValueError("Essa sigla já foi cadastrada para outra organização.")
        
        # Criação da nova organização
        new_org = Organizacao(
            nome=nome,  # type: ignore
            sigla=sigla, # type: ignore
            id_responsavel=id_responsavel # type: ignore
        )
        
        try:
            db.session.add(new_org)
            db.session.commit()
            return new_org
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao criar organização: {e}")
        
    @staticmethod
    def update(id: int, nome: str, sigla: str, id_responsavel: int | None = None):
        """Atualiza uma organização"""
        if len(Organizacao.query.filter_by(nome=nome).all()) > 1:
            raise ValueError("Uma organização com esse nome já existe.")
        
        if len(Organizacao.query.filter_by(sigla=sigla).all()) > 1:
            raise ValueError("Essa sigla já foi cadastrada para outra organização.")
        
        org: Organizacao = OrganizacaoService.get_by_id(id) # type: ignore
        org.nome = nome
        org.sigla= sigla
        if id_responsavel:
            org.id_responsavel = id_responsavel
        
        try:
            db.session.commit()
            return org
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao atualizar uma organização: {e}")

    @staticmethod
    def inativar(id):
        """Inativa uma organização pelo ID"""
        org = Organizacao.query.get(id)
        if org:
            try:
                org.ativo = False
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(f"Erro ao inativar organização: {e}")
        else:
            raise ValueError(f"Organização com ID {id} não encontrada.")
        
    @staticmethod
    def ativar(id):
        """Ativa uma organização pelo ID"""
        org = Organizacao.query.get(id)
        if org:
            try:
                org.ativo = True
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(f"Erro ao ativar organização: {e}")
        else:
            raise ValueError(f"Organização com ID {id} não encontrada.")

    @staticmethod
    def e_responsavel(user_id, organizacao_id):
        org = Organizacao.query.filter(Organizacao.id == organizacao_id ,Organizacao.id_responsavel == user_id).first()
        if org:
            return True
        return False