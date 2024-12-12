from app.ext.database import db
from app.models.dotacao import elemento_despesa
from app.models.dotacao.elemento_despesa import ElementoDespesa


class ElementoDespesaService:
    
    @staticmethod
    def get_all() -> list[ElementoDespesa]:
        """
        Recupera todos os elementos de despesa cadastrados.
        
        Returns
        -------
        list[ElementoDespesa]
            Lista de elementos de despesa cadastrados.
        """
        return ElementoDespesa.query.all()
    
    @staticmethod
    def get_by_id(id_elemento_despesa: int) -> ElementoDespesa:
        """
        Recupera um elemento de despesa pelo seu id.
        
        Parameters
        ----------
        id_elemento_despesa : int
            Id do elemento de despesa a ser recuperado.
        
        Returns
        -------
        ElementoDespesa
            Elemento de despesa recuperado.
        
        Raises
        ------
        Exception
            Caso o elemento de despesa nao seja encontrado.
        """
        elemento_despesa = ElementoDespesa.query.filter(ElementoDespesa.id == id_elemento_despesa).first()
        if not elemento_despesa:
            raise Exception("Elemento de despesa nao encontrado, tente novamente.")
        return elemento_despesa
    
    @staticmethod
    def create(codigo: str, descricao: str) -> ElementoDespesa:
        """
        Cria um novo elemento de despesa.
        
        Parameters
        ----------
        codigo : str
            Codigo do elemento de despesa.
        descricao : str
            Descricao do elemento de despesa.
        
        Returns
        -------
        ElementoDespesa
            Elemento de despesa criado.
        """
        elemento_despesa = ElementoDespesa()
        elemento_despesa.codigo = codigo
        elemento_despesa.descricao = descricao
        db.session.add(elemento_despesa)
        db.session.commit()
        return elemento_despesa
    
    @staticmethod
    def update(id_elemento_despesa: int, codigo: str | None = None, descricao: str | None = None) -> ElementoDespesa:
        """
        Atualiza um elemento de despesa existente com os valores fornecidos.

        Parameters
        ----------
        id_elemento_despesa : int
            Id do elemento de despesa a ser atualizado.
        codigo : str | None, optional
            Novo código do elemento de despesa. Se None, o código não será alterado.
        descricao : str | None, optional
            Nova descrição do elemento de despesa. Se None, a descrição não será alterada.

        Returns
        -------
        ElementoDespesa
            Elemento de despesa atualizado.

        Raises
        ------
        Exception
            Se nenhum dos campos `codigo` ou `descricao` for alterado.
        """
        if codigo is None and descricao is None:
            raise Exception("Nenhum campo foi alterado")
        elemento_despesa = ElementoDespesaService.get_by_id(id_elemento_despesa)
        if codigo is not None:
            elemento_despesa.codigo = codigo
        if descricao is not None:
            elemento_despesa.descricao = descricao
        db.session.commit()
        return elemento_despesa
    