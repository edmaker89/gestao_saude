from time import strftime
from app.models.correspondencias import Correspondencias
from datetime import date
from app.ext.database import db


class CorrespondenciaController:
    
    @staticmethod
    def obter_novo_numero(tipo_id):
        data = date.today().year
        ultima_correspondencia = Correspondencias.query.filter(Correspondencias.tipo==tipo_id).first()
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