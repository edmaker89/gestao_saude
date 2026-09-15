# Task 2 — Config: env + cookies seguros + ProxyFix

## Objetivo
Ler `SECRET_KEY` do ambiente (sem ficar em `settings.toml`) e aplicar configuração de segurança de sessão para operar atrás do nginx.

## Mudanças
1. `settings.toml`: remover a linha `SECRET_KEY="..."`; manter apenas `[default] EXTENSIONS=[...]`.
2. `app/app.py` (em `minimal_app`):
   - Ler `DATABASE_URL` (já existe) e `SECRET_KEY` de `os.getenv`, com fail-fast (`raise ValueError`) se ausentes.
   - **Depois** de `configuration.init_app(app)`, aplicar:
     - `app.config['SECRET_KEY'] = SECRET_KEY`
     - `app.config['SESSION_COOKIE_SECURE'] = _env_bool('SESSION_COOKIE_SECURE', True)`
     - `app.config['SESSION_COOKIE_HTTPONLY'] = True`
     - `app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'`
   - Aplicar `ProxyFix` no WSGI: `from werkzeug.middleware.proxy_fix import ProxyFix` e `app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)`.
   - Forçar `app.debug = False`.
   - Criar helper local `_env_bool(nome, default)` (aceita `true/1/yes`).

## Detalhe importante
- Dynaconf (`FlaskDynaconf`) usa `ENVVAR_PREFIX="FLASK"` e `LOAD_DOTENV=True`. Por isso `SECRET_KEY` precisa ser lida explicitamente de `os.environ` e setada **após** `init_app` (o `__setitem__` do `DynaconfConfig` grava no settings e tem precedência).

## Arquivos
- Editar: `settings.toml`, `app/app.py`

## Critérios de aceite
- `create_app()` funciona com `DATABASE_URL` e `SECRET_KEY` no ambiente.
- Sem as variáveis, `create_app()` levanta erro claro (fail-fast).
- `settings.toml` não contém mais segredos.

## Commit sugerido
`ler SECRET_KEY do ambiente e endurecer cookies de sessão`
