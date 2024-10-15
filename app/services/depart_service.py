from app.ext.database import db
from app.models.departamento import Departamento


class DepartmentService:

    @staticmethod
    def get_departs_by_filters(departamento=None, ordem='asc', page=1, per_page=20): 
        query = db.session.query(
            Departamento
        )

        if departamento:
            query = query.filter(Departamento.nome.like(f"%{departamento}%"))
        if ordem == 'asc':
            query = query.order_by(Departamento.nome.asc())
        else:
            query = query.order_by(Departamento.nome.desc())

        departamentos = query.paginate(page=page, per_page=per_page) # type: ignore

        return departamentos
