from datetime import UTC, datetime
from app.ext.database import db

class Cidadaos(db.Model):
    __tablename__ = 'cidadaos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    mae = db.Column(db.String(255))
    cpf = db.Column(db.String(15))
    cns = db.Column(db.String(11))
    rg = db.Column(db.String(20))
    orgao_expedidor = db.Column(db.String(50))
    data_de_nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(15), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    logradouro = db.Column(db.String(255))
    numero = db.Column(db.String(20))
    complemento = db.Column(db.String(255))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    ocupacao = db.Column(db.String(100))
    data_criacao = db.Column(db.Date, default=datetime.now(UTC))
    data_atualizacao = db.Column(db.Date, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    telefone = db.relationship('TelefoneCidadao', backref='cidadao', lazy=True)
    
    def verificar_existencia_cpf_cns(self):
        if self.cpf or self.cns:
            # Verificar no banco de dados se já existe um registro com o mesmo CPF ou CNS
            existing_cidadao = Cidadaos.query.filter((Cidadaos.cpf == self.cpf) | (Cidadaos.cns == self.cns)).first()
            if existing_cidadao:
                return False  # Já existe um cidadão com o mesmo CPF ou CNS
        return True  # Não existe nenhum cidadão com o mesmo CPF ou CNS
    
    def save(self):
        print(self.id)
        if self.id == None:
            print('esse é um novo cidadao')
            if self.verificar_existencia_cpf_cns():
                print('verificando se ja existe cpf ou cartão sus')
                db.session.add(self)
                db.session.commit()
                
                #cadastrar os Telefones
                return True
            else:
                return False
        else:
            print('estamos atualizando o cidadao')
            db.session.commit()
            return True

    def __repr__(self):
        return self.nome
    
class TelefoneCidadao(db.Model):
    __tablename__ = 'telefone_cidadao'
    id = db.Column(db.Integer, primary_key=True)
    ddd = db.Column(db.String(2), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(20))  # Você pode adicionar um campo para o tipo de telefone se necessário
    cidadao_id = db.Column(db.Integer, db.ForeignKey('cidadaos.id'), nullable=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def __repr__(self):
        return f'TelefoneCidadao {self.numero}'