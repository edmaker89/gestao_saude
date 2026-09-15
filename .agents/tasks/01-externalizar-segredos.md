# Task 1 — Externalizar segredos para variáveis de ambiente

## Objetivo
Tirar do repositório todos os valores sensíveis reais e preparar o padrão de variáveis de ambiente.

## Mudanças
1. Remover o arquivo `.env` do controle de versão (`git rm --cached .env` e apagar o arquivo).
2. Criar `.env.example` (sem valores reais) com as variáveis canônicas:
   ```
   DATABASE_URL=mysql+pymysql://USER:SENHA@127.0.0.1:3306/gestao_saude_db
   SECRET_KEY=CHANGE_ME
   SESSION_COOKIE_SECURE=true
   EMAIL_USER=noreplay@example.com
   EMAIL_PASSWORD=CHANGE_ME
   EMAIL_SMTP_SERVER=smtp.gmail.com
   EMAIL_SMTP_PORT=587
   APP_HOST=127.0.0.1
   APP_PORT=5000
   APP_THREADS=8
   SEED_ON_EMPTY=true
   ```
3. Atualizar `.gitignore` para ignorar `.env` e `*.pem`.
4. Remover os certificados/chaves do versionamento:
   - `cert.pem` (raiz)
   - `privkey.pem` (raiz)
   - `app/cert.pem`
   - `app/privkey.pem`

## Arquivos
- Criar: `.env.example`
- Editar: `.gitignore`
- Remover: `.env`, `cert.pem`, `privkey.pem`, `app/cert.pem`, `app/privkey.pem`

## Critérios de aceite
- `git status` não lista mais `.env` nem `*.pem`.
- `.env.example` existe e documenta todas as variáveis usadas pelo app.

## Commit sugerido
`remover segredos do repositório e criar .env.example`
