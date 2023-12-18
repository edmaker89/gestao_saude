from time import strftime

from flask import jsonify
from app.models.correspondencias import Correspondencias
from datetime import date
from app.ext.database import db
from app.models.tipo_correspondencias import TipoCorrespondencias
from app.models.users import Usuario


class CorrespondenciaController:
    
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

        print('ultima correspondencia', ultima_correspondencia)
        if ultima_correspondencia:
            print(ultima_correspondencia.assunto)
            if int(ultima_correspondencia.ano) != data:
                print('é diferente')
                numero = 1
                print(ultima_correspondencia.ano)
                return numero
            else:
                print('é igual')
                numero = ultima_correspondencia.numero + 1
                return numero
        else:
            return 1
        
    @staticmethod
    def nova_correspondencia(tipo_id, assunto, usuario_id):
        numero = CorrespondenciaController.obter_novo_numero(tipo_id)
        print('numero gerado', numero)
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
    def get_last_correspondencias_by_user(user_id):
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
        ).limit(20).all()
    
        return mails
    
    @staticmethod
    def mail_edit_assunto(mail_id, mail_assunto):
        mail = CorrespondenciaController.get_correspondencia_by_id_unique(mail_id)

        mail.assunto = mail_assunto

        db.session.commit()

        return mail


