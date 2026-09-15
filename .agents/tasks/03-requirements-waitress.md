# Task 3 — Corrigir requirements.txt (UTF-8) e adicionar Waitress

## Objetivo
O `requirements.txt` está em UTF-16LE com BOM (bytes iniciais `ff fe`), o que quebra `pip install -r`. Regravar em UTF-8 sem BOM e adicionar o servidor WSGI para Windows.

## Mudanças
1. Regravar `requirements.txt` em **UTF-8 sem BOM**, preservando todas as versões atuais.
2. Adicionar `waitress==3.0.2` (servidor WSGI para Windows; gunicorn permanece para o caminho Linux/Docker).

## Arquivos
- Editar: `requirements.txt`

## Critérios de aceite
- `xxd requirements.txt | head -1` NÃO começa com `ff fe`.
- `python -c "import sys; open('requirements.txt', encoding='utf-8').read()"` lê sem erro.
- `waitress` presente no arquivo.

## Commit sugerido
`corrigir encoding do requirements.txt e adicionar waitress`
