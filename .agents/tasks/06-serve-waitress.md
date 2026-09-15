# Task 6 — Entrypoint Waitress (serve.py)

## Objetivo
Criar um entrypoint para o serviço Windows usando Waitress (gunicorn não roda no Windows).

## Mudanças
Criar `serve.py` na raiz:
```python
import os
from waitress import serve
from app.app import create_app

def _env_int(nome, default):
    return int(os.getenv(nome, default))

app = create_app()
serve(
    app,
    host=os.getenv("APP_HOST", "127.0.0.1"),
    port=_env_int("APP_PORT", 5000),
    threads=_env_int("APP_THREADS", 8),
)
```
- Bind em `127.0.0.1` por padrão (não expõe a porta externamente; o nginx faz o proxy).

## Arquivos
- Criar: `serve.py`

## Critérios de aceite
- `python serve.py` sobe a app em `127.0.0.1:5000` (com `DATABASE_URL` e `SECRET_KEY` no ambiente).
- Não há uso de gunicorn no caminho Windows.

## Commit sugerido
`adicionar entrypoint serve.py com waitress`
