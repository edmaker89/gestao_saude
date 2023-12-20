# Gestão Saúde

# Sistema de Controle de Correspondências para a Secretaria Municipal de Saúde de Itaberaí

Este projeto foi desenvolvido para atender às necessidades da Secretaria Municipal de Saúde de Itaberaí, proporcionando uma transição eficiente e profissional do controle de correspondências tradicional, baseado em papéis afixados nas paredes, para um sistema informatizado.

## Descrição

O Sistema de Controle de Correspondências oferece uma abordagem moderna e eficaz para gerenciar o fluxo de informações dentro da Secretaria Municipal de Saúde. Ao substituir os métodos antiquados por um sistema informatizado, o secretário e a equipe terão acesso a uma plataforma centralizada para registrar, monitorar e arquivar todas as correspondências.

## Funcionalidades Principais

- **Geração Automática de Números**: O sistema gera automaticamente números de correspondências, eliminando a necessidade de métodos manuais e proporcionando um rastreamento mais eficiente.

- **Controle de Tipos de Correspondências**: Categorização inteligente com base nos tipos de correspondências, como memorandos, ofícios, despachos e portarias.

- **Registro e Consulta Rápida**: Facilidade em registrar novas correspondências e acessar rapidamente os registros existentes.

- **Notificações Automáticas**: O sistema pode enviar notificações automáticas para alertar sobre novas correspondências ou ações pendentes.

## Benefícios

- **Redução do Uso de Papel**: Eliminação do método tradicional de controle manual em papel, contribuindo para a sustentabilidade ambiental.

- **Eficiência no Rastreamento**: Facilita o rastreamento e a localização rápida de correspondências, otimizando o tempo da equipe.

- **Segurança e Privacidade**: Garante a segurança e a privacidade das informações, evitando perdas e extravios.

- **Profissionalismo e Modernização**: Transição para um sistema informatizado, refletindo um ambiente mais profissional e modernizado.

## Como Contribuir

Se você deseja contribuir para o aprimoramento deste projeto, siga as instruções fornecidas no [guia de contribuição](CONTRIBUTING.md).

## Licença

Este projeto é licenciado sob a [edmaker.dev.br](LICENSE).


## Pré-requisitos

- Python (versão 3.12)
- Flask (versão 3.0.0)
- Gunicorn (versão 21.2.0)
- Docker
- Outras dependências... vide arquivo requirements.txt

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/seu-projeto.git
2. Acesse o diretório do projeto:
   ```bash
   cd seu-projeto

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt

## Configuração

1. Crie um arquivo .env na raiz do projeto e configure as variáveis de ambiente:
    ```bash
    FLASK_APP=nome_do_app.py
    FLASK_ENV=development
    SECRET_KEY=sua_chave_secreta
    DATABASE_URL=URL_do_banco_de_dados

## Uso

1. Inicie o servidor flask:
     ```bash
     flask run
2. Acesso o aplicativo pelo navegador [http://localhost:5000](http://localhost:5000)

## Como Contribuir

Agradecemos por considerar contribuir para o projeto. Siga estas etapas para participar:

1. **Faça um Fork do projeto.**
2. **Crie uma nova branch para a sua contribuição:**
   ```bash
   git checkout -b feature/sua-contribuicao

3. Faça as alterações necessárias e adicione testes, se aplicável.

  4 .Certifique-se de que os testes passam.

5. Faça commit das suas alterações:
    ```bash
    git commit -m 'Adicione sua contribuição'

7. Faça push da sua branch:
   ```bash
   git push origin feature/sua-contribuicao

9. Envie um Pull Request
    Nós revisaremos as suas alterações o mais rapido possivel. Agradecemos por suas contribuições!
