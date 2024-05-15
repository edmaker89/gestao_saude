from app.ext.database import db

class Pesquisa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('ativa', 'inativa', 'concluida'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('pesquisas', lazy=True))

    def __repr__(self):
        return f"Pesquisa('{self.titulo}', '{self.descricao}', '{self.data_criacao}', '{self.status}')"

class Pergunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pesquisa_id = db.Column(db.Integer, db.ForeignKey('pesquisa.id'), nullable=False)
    texto = db.Column(db.String(255), nullable=False)
    tipo_pergunta = db.Column(db.String(50), nullable=False)
    pesquisa = db.relationship('Pesquisa', backref=db.backref('perguntas', lazy=True))

    def __repr__(self):
        return f"Pergunta('{self.texto}', '{self.tipo_pergunta}')"

class OpcaoResposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pergunta_id = db.Column(db.Integer, db.ForeignKey('pergunta.id'), nullable=False)
    texto = db.Column(db.String(255), nullable=False)
    pergunta = db.relationship('Pergunta', backref=db.backref('opcoesresposta', lazy=True))

    def __repr__(self):
        return f"OpcaoResposta('{self.texto}')"

class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pesquisa_id = db.Column(db.Integer, db.ForeignKey('pesquisa.id'), nullable=False)
    pergunta_id = db.Column(db.Integer, db.ForeignKey('pergunta.id'), nullable=False)
    opcao_resposta_id = db.Column(db.Integer, db.ForeignKey('opcao_resposta.id'))
    texto_resposta = db.Column(db.Text)
    cpf = db.Column(db.String(11), nullable=False)
    data_hora_resposta = db.Column(db.DateTime, nullable=False)
    pesquisa = db.relationship('Pesquisa', backref=db.backref('respostas', lazy=True))
    pergunta = db.relationship('Pergunta', backref=db.backref('respostas', lazy=True))
    opcao_resposta = db.relationship('OpcaoResposta')

    def __repr__(self):
        return f"Resposta('{self.texto_resposta}', '{self.cpf}', '{self.data_hora_resposta}')"