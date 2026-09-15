# Task 4 — Remover prints e trocar por logging

## Objetivo
Eliminar `print()` de debug em produção, trocando por `app.logger`/`logging` quando útil.

## Mudanças (arquivos e linhas atuais)
- `app/utils/context_processors.py:11` — `print(permissions)` → remover.
- `app/models/token.py:27-31` — prints de token/datetime → `app.logger.debug(...)` ou remover.
- `app/blueprints/views.py` — `print(solicitacao)` (51) e blocos `print(...)` das rotas de redefinição de senha (70-122) → `app.logger.debug(...)` ou remover.
- `app/blueprints/admin.py` — `print('id_role'...)` (23), `print(role)` (89), `print(role_permissions)` (90), `print(permission_linked)` (96), `print(e)` (202) → `app.logger`.
- `app/blueprints/departmento.py:34-47` — prints de fluxo → remover/logger.
- `app/blueprints/mail.py:33,46,84,191` — prints → remover; `print(e)` em `except` → `app.logger.exception`.
- `app/services/usuario_service.py:141` — `print(user)` → remover.
- `app/services/correspondencia_service.py:186,189,193` — prints → remover/logger.
- `app/models/departamento.py:30` — `print(e)` → `app.logger.exception`.
- `app/utils/filters.py:47` — `print(e)` → `app.logger.exception`.
- `app/utils/comunications/email.py:81,118` — `print(e)` → `app.logger.exception`.

## Padrão
- Dentro de `except`: `app.logger.exception("mensagem")` (ou `logging.getLogger(__name__)` onde não houver `app` acessível).
- Demais: remover ou `app.logger.debug(...)`.

## Arquivos
- Editar: os 9 arquivos listados acima.

## Critérios de aceite
- `grep -rn "print(" app/` não retorna nenhum `print` de debug restante (exceto se houver `print` intencional fora do escopo — não deve haver).

## Commit sugerido
`substituir prints por logging`
