from operator import or_
import stat
from app.ext.database import db
from app.models.dotacao import aplicacao_programada
from app.models.dotacao.aplicacao_programada import AplicacaoProgramada

class AplicacaoProgramadaService():
    
    @staticmethod
    def get_all() -> list[AplicacaoProgramada]:
        """
        Retorna todas as AplicacoesProgramadas cadastradas.

        Returns:
            list[AplicacaoProgramada]: Uma lista de AplicacoesProgramadas.
        """
        return AplicacaoProgramada.query.all()
    
    @staticmethod
    def get_by_numero(numero: str) -> AplicacaoProgramada | None:
        """
        Retorna uma AplicacaoProgramada pelo seu numero.

        Args:
            numero (str): O numero da AplicacaoProgramada.

        Returns:
            AplicacaoProgramada | None: A AplicacaoProgramada com o numero especificado ou None caso nao seja encontrada.
        """
        return AplicacaoProgramada.query.filter(AplicacaoProgramada.numero == numero).first()
    
    @staticmethod
    def get_by_id(id: int) -> AplicacaoProgramada | None:
        """
        Retorna uma AplicacaoProgramada pelo seu id.

        Args:
            id (int): O id da AplicacaoProgramada.

        Returns:
            AplicacaoProgramada | None: A AplicacaoProgramada com o id especificado ou None caso nao seja encontrada.
        """
        return AplicacaoProgramada.query.filter(AplicacaoProgramada.id == id).first()
    
    @staticmethod
    def create(numero: str, ano: int, status: str = 'vigente', descricao: str | None = None) -> AplicacaoProgramada:
        """
        Cria uma nova AplicacaoProgramada com os valores fornecidos.

        Args:
            numero (str): O numero da AplicacaoProgramada.
            ano (int): O ano da AplicacaoProgramada.
            status (str, optional): O status da AplicacaoProgramada. Defaults to 'vigente'.
            descricao (str | None, optional): A descricao da AplicacaoProgramada. Defaults to None.

        Returns:
            AplicacaoProgramada: A AplicacaoProgramada criada.
        """
        aplicacao_programada = AplicacaoProgramada()
        aplicacao_programada.descricao = descricao
        aplicacao_programada.ano = ano
        aplicacao_programada.status = status
        aplicacao_programada.numero = numero

        db.session.add(aplicacao_programada)
        db.session.commit()

        return aplicacao_programada
    
    @staticmethod
    def update(id: int, numero: str | None = None, ano: int | None = None, status: str | None = None, descricao: str | None = None) -> AplicacaoProgramada:
        """
        Atualiza uma AplicacaoProgramada existente com os valores fornecidos.
    
        Args:
            id (int): O id da AplicacaoProgramada a ser atualizada.
            numero (str | None): O novo numero da AplicacaoProgramada. Se None, não será alterado.
            ano (int | None): O novo ano da AplicacaoProgramada. Se None, não será alterado.
            status (str | None): O novo status da AplicacaoProgramada. Se None, não será alterado.
            descricao (str | None): A nova descricao da AplicacaoProgramada. Se None, não será alterado.
    
        Returns:
            AplicacaoProgramada: A AplicacaoProgramada atualizada.
    
        Raises:
            Exception: Se a AplicacaoProgramada com o id fornecido não for encontrada.
        """
        aplicacao_programada: AplicacaoProgramada | None = AplicacaoProgramadaService.get_by_id(id)
        if not aplicacao_programada:
            raise Exception("AplicacaoProgramada nao encontrada")

        updates = {k: v for k, v in {'numero': numero, 'descricao': descricao, 'ano': ano, 'status': status}.items() if v is not None}
        for attr, value in updates.items():
            setattr(aplicacao_programada, attr, value)

        db.session.commit()
        return aplicacao_programada
    
    @staticmethod
    def change_status(id: int, status: str) -> AplicacaoProgramada:
        """
        Muda o status de uma AplicacaoProgramada existente.
        Status possiveis: 'vigente', 'arquivida'

        Args:
            id (int): O id da AplicacaoProgramada a ser atualizada.
            status (str): O novo status a ser definido na AplicacaoProgramada.

        Returns:
            AplicacaoProgramada: A AplicacaoProgramada com o status atualizado.

        Raises:
            Exception: Se a AplicacaoProgramada com o id fornecido não for encontrada.
        """
        if status not in ['vigente', 'arquivada']:
            raise Exception("Situacao da aplicação programada invalida")
        
        aplicacao_programada: AplicacaoProgramada | None = AplicacaoProgramadaService.get_by_id(id)
        if not aplicacao_programada:
            raise Exception("AplicacaoProgramada nao encontrada")

        aplicacao_programada.status = status
        db.session.commit()
        return aplicacao_programada
