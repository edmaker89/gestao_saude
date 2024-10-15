from app.models.correspondencias import Correspondencias
from datetime import date
from app.ext.database import db
from app.models.tipo_correspondencias import TipoCorrespondencias
from app.models.users import Usuario

class CorrespondenciaService:
    
    @staticmethod
    def obter_novo_numero(tipo_id: int):
        """sumary_line
        
        Keyword arguments:
        argument -- recebe um tipo da correspondencia em id -> tipo_id
        Return: retorna um novo numero de correspondencia baseado na consulta
        ao banco de dados, se ele encontrar do mesmo tipo e mesmo ano ele soma
        + 1 no numero, se não, retorna 1
        """
        

        data = date.today().year
        ultima_correspondencia = Correspondencias.query.filter(Correspondencias.tipo == tipo_id).\
            order_by(Correspondencias.id.desc()).first()

        if ultima_correspondencia:
            if int(ultima_correspondencia.ano) != data:
                numero = 1
                return numero
            else:
                numero = ultima_correspondencia.numero + 1
                return numero
        else:
            return 1
        
    @staticmethod
    def nova_correspondencia(tipo_id, assunto, usuario_id):
        numero = CorrespondenciaService.obter_novo_numero(tipo_id)
        nova = Correspondencias()
        nova.tipo = tipo_id
        nova.assunto = assunto
        nova.usuario = usuario_id
        nova.data = date.today()
        nova.numero = numero
        nova.ano = date.today().year
        nova.numero_ano = str(numero)+'/'+str(date.today().year)
        
        db.session.add(nova)
        db.session.commit()

        return nova
    
    @staticmethod
    def get_correspondencia_by_id(correspondencia_id):
        mail = db.session.query(
            Correspondencias,
            TipoCorrespondencias,
            Usuario
        ).join(
            TipoCorrespondencias,
            Correspondencias.tipo == TipoCorrespondencias.id
        ).join(
            Usuario,
            Correspondencias.usuario == Usuario.id
        ).filter(
            Correspondencias.id == correspondencia_id
        ).first()

        return mail
    
    @staticmethod
    def get_correspondencia_by_id_unique(correspondencia_id):
        mail = Correspondencias.query.filter(Correspondencias.id == correspondencia_id).first()

        return mail
    
    @staticmethod
    def get_correspondencias_by_user(user_id):
        mails = db.session.query(
            Usuario,
            Correspondencias,
            TipoCorrespondencias,
        ).join(
            Correspondencias,
            Usuario.id == Correspondencias.usuario
        ).join(
            TipoCorrespondencias,
            Correspondencias.tipo == TipoCorrespondencias.id
        ).filter(
            Usuario.id == user_id
        ).all()
        
        return mails
    
    @staticmethod
    def get_last_correspondencias_by_user(user_id, page=1, per_page=10):
        mails = db.session.query(
            Usuario,
            Correspondencias,
            TipoCorrespondencias,
        ).join(
            Correspondencias,
            Usuario.id == Correspondencias.usuario
        ).join(
            TipoCorrespondencias,
            Correspondencias.tipo == TipoCorrespondencias.id
        ).filter(
            Usuario.id == user_id
        ).order_by(
            Correspondencias.id.desc()  # Substitua por seu campo de data, se necessário
        ).paginate(page=page, per_page=per_page)
    
        return mails
    
    @staticmethod
    def mail_edit_assunto(mail_id, mail_assunto):
        mail = CorrespondenciaService.get_correspondencia_by_id_unique(mail_id)

        mail.assunto = mail_assunto

        db.session.commit()

        return mail

    @staticmethod
    def get_correspondencias_by_user_with_filters(user_id=None, numero=None, data=None, assunto=None, page=1, per_page=10, tipo=None, ordem='desc'):
        query = db.session.query(
            Usuario,
            Correspondencias,
            TipoCorrespondencias,
        ).join(
            Correspondencias,
            Usuario.id == Correspondencias.usuario
        ).join(
            TipoCorrespondencias,
            Correspondencias.tipo == TipoCorrespondencias.id
        )

        if user_id:
            query = query.filter(Correspondencias.usuario == user_id)
        if numero:
            query = query.filter(Correspondencias.numero_ano.like(f"%{numero}%"))
        if data:
            query = query.filter(Correspondencias.data == data)
        if assunto:
            query = query.filter(Correspondencias.assunto.like(f"%{assunto}%"))
        if tipo:
            query = query.filter(Correspondencias.tipo == tipo)

        # Adicione a ordenação pela data ou outro campo apropriado
        if ordem == 'asc':
            query = query.order_by(Correspondencias.id.asc())
        else:
            query = query.order_by(Correspondencias.id.desc())
        

        mails = query.paginate(page=page, per_page=per_page) # type: ignore

        return mails