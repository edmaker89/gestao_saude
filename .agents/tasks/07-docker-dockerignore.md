# Task 7 — Docker: parametrizar secrets e .dockerignore

## Objetivo
Manter o caminho Linux/Docker, mas sem segredos em texto puro e sem copiar `.env`/chaves para a imagem.

## Mudanças
1. `docker-compose.yml`:
   - Substituir literais por variáveis:
     - `MARIADB_ROOT_PASSWORD: ${MARIADB_ROOT_PASSWORD}`
     - `MARIADB_PASSWORD: ${MARIADB_PASSWORD}`
     - `DATABASE_URL: ${DATABASE_URL:-mysql+pymysql://gestao_saude_user:${MARIADB_PASSWORD}@db:3306/gestao_saude_db}`
   - Não publicar `3306` (db) e `8080` (adminer) externamente; se mantiver adminer/portainer, ligar em `127.0.0.1`.
2. Criar `.dockerignore`:
   ```
   .env
   *.pem
   .git
   __pycache__
   **/__pycache__
   .venv
   venv
   .agents
   ```

## Arquivos
- Editar: `docker-compose.yml`
- Criar: `.dockerignore`

## Critérios de aceite
- Nenhum segredo literal em `docker-compose.yml`.
- `docker build` não inclui `.env`/`*.pem` na imagem.

## Commit sugerido
`parametrizar segredos no docker-compose e adicionar .dockerignore`
