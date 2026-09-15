# Task 5 — Bootstrap de dados mínimos (create_all + seed)

## Objetivo
Criar `app/utils/bootstrap.py` que, no startup, garante o schema (fallback) e insere um dataset mínimo fictício **somente se o banco estiver vazio**. Chamar em `create_app()`.

## Regras
- Só roda se `SEED_ON_EMPTY` for verdadeiro (default `true`).
- Envolver em `try/except` com `app.app_context()`: se o banco não conectar ou faltar algo, logar aviso e **não derrubar o app**.

## Mudanças
1. `app/utils/bootstrap.py` (novo):
   - Importar **todos** os módulos de models antes do `create_all`, para o metadata ficar completo:
     `users, role_permissions, departamento, estabelecimento, organizacao, tipo_correspondencias, correspondencias, avisos, token, item`,
     `contrato.base_contrato, contrato.contrato, contrato.contrato_item, contrato.fornecedor, contrato.lotacao_contrato, contrato.solicitacao_contrato, contrato.tipo_contrato`,
     `dotacao.aplicacao_programada, dotacao.conta, dotacao.elemento_despesa, dotacao.ficha, dotacao.ficha_fonte, dotacao.fonte, dotacao.rubrica_orcamentaria`,
     `edital.edital`.
   - `db.create_all()` (fallback para banco novo; não altera tabelas existentes).
   - Se `Usuario.query.first()` existir → retorna (não faz seed).
   - Senão, inserir dataset fictício:
     1. 7 `Permission`: `gerenciamento master`, `acesso restrito`, `todas correspondencias`, `regulacao`, `pesquisa`, `gestao de avisos`, `gerenciar permissão`.
     2. `Role id=1` "Master" + `RolePermissions` ligando a todas.
     3. `Usuario` admin (constantes fictícias): username `admin`, email `admin@example.com`, senha `Mudar@123` via `generate_password_hash`, `role='1'`, `ativo=True`.
     4. 1 `Organizacao` → 1 `Estabelecimento` → 1 `Departamento` (responsavel = admin); depois setar `admin.departamento_id`.
     5. 4 `TipoCorrespondencias`: Memorando, Ofício, Despacho, Portaria.
     6. 1 `Aviso` de boas-vindas (autor = admin).
     - `db.session.commit()` no fim; `rollback()` em caso de erro.
2. `app/app.py` (`create_app`): chamar `bootstrap(app)` **após** `configuration.load_extensions(app)`.

## Detalhe
- FK circular (`Usuario.departamento_id` ↔ `Departamento.responsavel_id`) → criar em 2 passos (user primeiro, depois departamento, depois atualizar user).

## Arquivos
- Criar: `app/utils/bootstrap.py`
- Editar: `app/app.py`

## Critérios de aceite
- Banco vazio → schema completo criado e dataset presente (login `admin`/`Mudar@123` funciona).
- Banco já populado → seed não roda (nenhum dado duplicado).
- `SEED_ON_EMPTY=false` → bootstrap não faz nada.
- Falha de conexão não derruba a app.

## Commit sugerido
`adicionar bootstrap com create_all e seed de dados mínimos`
