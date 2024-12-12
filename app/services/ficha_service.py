from app.ext.database import db
from app.models.dotacao.ficha import Ficha

class FichaService:
    
    @staticmethod
    def get_all() -> list[Ficha]:
        """
        Retrieves all Ficha records from the database.
    
        Returns
        -------
        list[Ficha]
            A list containing all Ficha objects.
        """
        return Ficha.query.all()
    
    @staticmethod
    def get_by_id(id) -> Ficha | None:
        """Retrieves a Ficha by its id.
        
        Parameters
        ----------
        id : int
            The id of the Ficha to retrieve.
        
        Returns
        -------
        Ficha | None
            The Ficha with the given id, or None if no such Ficha exists.
        """
        return Ficha.query.get(id)
    
    @staticmethod
    def get_by_numero_ficha(numero_ficha) -> Ficha | None:
        """Retrieves a Ficha by its numero_ficha.
        
        Parameters
        ----------
        numero_ficha : str
            The numero_ficha of the Ficha to retrieve.
        
        Returns
        -------
        Ficha | None
            The Ficha with the given numero_ficha, or None if no such Ficha exists.
        """
        return Ficha.query.filter(Ficha.numero_ficha == numero_ficha).first()
        
    @staticmethod
    def get_by_aplicacao_and_elemento(aplicacao_programada_id, elemento_despesa_id) -> Ficha | None:
        """Retrieves a Ficha by its aplicacao_programada_id and elemento_despesa_id.
        
        Parameters
        ----------
        aplicacao_programada_id : int
            The id of the AplicacaoProgramada related to the Ficha.
        elemento_despesa_id : int
            The id of the ElementoDespesa related to the Ficha.
        
        Returns
        -------
        Ficha | None
            The Ficha with the given aplicacao_programada_id and elemento_despesa_id, or None if no such Ficha exists.
        """
        return Ficha.query.filter(
            Ficha.aplicacao_programada_id == aplicacao_programada_id,
            Ficha.elemento_despesa_id == elemento_despesa_id
        ).first()
    
    @staticmethod
    def create(numero_ficha: str, ano: int, aplicacao_programada_id: int, elemento_despesa_id: int, status: str = 'vigente') -> Ficha:
        """Creates a new Ficha with the given parameters.
        
        Parameters
        ----------
        numero_ficha : str
            The numero_ficha of the Ficha to create.
        ano : int
            The year of the Ficha to create.
        aplicacao_programada_id : int
            The id of the AplicacaoProgramada related to the Ficha.
        elemento_despesa_id : int
            The id of the ElementoDespesa related to the Ficha.
        status : str, optional
            The status of the Ficha, by default 'vigente'.
        
        Returns
        -------
        Ficha
            The created Ficha.
        
        Raises
        ------
        Exception
            If a Ficha with the given aplicacao_programada_id and elemento_despesa_id already exists.
        """
        exist_ficha = FichaService.get_by_aplicacao_and_elemento(aplicacao_programada_id, elemento_despesa_id)
        if exist_ficha:
            raise Exception("Ficha ja cadastrada")
        
        ficha = Ficha()
        ficha.numero_ficha=numero_ficha, 
        ficha.ano=ano, 
        ficha.status=status, 
        ficha.aplicacao_programada_id=aplicacao_programada_id, 
        ficha.elemento_despesa_id=elemento_despesa_id
        
        db.session.add(ficha)
        db.session.commit()
        return ficha
    
    @staticmethod
    def update(id: int, numero_ficha: str | None = None, ano: int | None = None, status: str | None = None, aplicacao_programada_id: int | None = None, elemento_despesa_id: int | None = None) -> Ficha:
        """Updates a Ficha with the given parameters.
        
        Parameters
        ----------
        id : int
            The id of the Ficha to update.
        numero_ficha : str | None, optional
            The new numero_ficha of the Ficha. If None, the current value is kept.
        ano : int | None, optional
            The new year of the Ficha. If None, the current value is kept.
        status : str | None, optional
            The new status of the Ficha. If None, the current value is kept.
        aplicacao_programada_id : int | None, optional
            The new id of the AplicacaoProgramada related to the Ficha. If None, the current value is kept.
        elemento_despesa_id : int | None, optional
            The new id of the ElementoDespesa related to the Ficha. If None, the current value is kept.
        
        Returns
        -------
        Ficha
            The updated Ficha.
        
        Raises
        ------
        Exception
            If a Ficha with the given id is not found.
        """
        ficha: Ficha | None = FichaService.get_by_id(id)
        if ficha is None:
            raise Exception("Ficha nao encontrada")
        if numero_ficha is not None:
            ficha.numero_ficha = numero_ficha
        if ano is not None:
            ficha.ano = ano
        if status is not None:
            ficha.status = status
        if aplicacao_programada_id is not None:
            ficha.aplicacao_programada_id = aplicacao_programada_id
        if elemento_despesa_id is not None:
            ficha.elemento_despesa_id = elemento_despesa_id
        db.session.commit()
        return ficha
    
    @staticmethod
    def change_status(id: int, status: str) -> Ficha:
        """
        Muda o status de uma Ficha existente.
        
        Args:
            id (int): O id da Ficha a ser atualizada.
            status (str): O novo status a ser definido na Ficha.
        
        Returns:
            Ficha: A Ficha com o status atualizado.
        
        Raises:
            Exception: Se a Ficha com o id fornecido não for encontrada.
        """

        ficha: Ficha | None = FichaService.get_by_id(id)
        if ficha is None:
            raise Exception("Ficha nao encontrada")
        ficha.status = status
        db.session.commit()
        return ficha