# Tasks — migração Linux → Windows (ajustes mínimos)

Ordem de execução. Uma task = uma entrega consistente + um commit.

1. [01-externalizar-segredos.md](01-externalizar-segredos.md) — tirar `.env` real do repo, criar `.env.example`, atualizar `.gitignore`, remover `.pem`
2. [02-config-env-cookies.md](02-config-env-cookies.md) — `settings.toml` sem `SECRET_KEY`; `app.py` lê env, cookies seguros e `ProxyFix`
3. [03-requirements-waitress.md](03-requirements-waitress.md) — regravar `requirements.txt` em UTF-8 sem BOM e adicionar `waitress`
4. [04-remover-prints.md](04-remover-prints.md) — substituir `print()` por `app.logger`
5. [05-bootstrap-seed.md](05-bootstrap-seed.md) — `app/utils/bootstrap.py`: importar models, `db.create_all()`, seed se banco vazio
6. [06-serve-waitress.md](06-serve-waitress.md) — criar `serve.py` (Waitress)
7. [07-docker-dockerignore.md](07-docker-dockerignore.md) — `docker-compose.yml` com `${VAR}` e criar `.dockerignore`
8. [08-deploy-windows.md](08-deploy-windows.md) — `deploy/windows/*` (NSSM + nginx)
9. [09-verificacao.md](09-verificacao.md) — validação final + runbook

## Convenções
- Executar na ordem; commit ao final de cada task.
- Mensagens de commit em PT-BR, no imperativo (ex.: `remover .env real do repositório`).
- Não expandir escopo: sem SQLAlchemy 2.0, Flask-Migrate/Alembic, Portainer/Adminer, testes ou refactor de services.
