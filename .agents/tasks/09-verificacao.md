# Task 9 — Verificação final

## Objetivo
Garantir que tudo compila e que a app sobe sem quebrar, e fechar a documentação.

## Passos de verificação
1. `python -m compileall app serve.py` (sem erros de sintaxe).
2. `python -c "import app.app"` (importa sem erro).
3. Com `DATABASE_URL` e `SECRET_KEY` no ambiente, instanciar `create_app()` e verificar que não lança exceção (bootstrap tolera banco indisponível).
4. `xxd requirements.txt | head -1` → sem BOM.
5. `grep -rn "print(" app/` → sem prints de debug.
6. `git status` → sem `.env`/`*.pem` rastreados; `.env.example` e `deploy/windows/` presentes.
7. Smoke test (se houver MariaDB disponível):
   - `python serve.py`, acessar `http://127.0.0.1:5000`, login `admin`/`Mudar@123`, trocar senha.
   - Testar envio de e-mail (se `EMAIL_*` configurado).
   - Validar proxy: nginx em `443 → 127.0.0.1:5000`.

## Arquivos
- Nenhum obrigatório; atualizar `README.md` raiz se necessário (link para `deploy/windows/README.md`).

## Critérios de aceite
- Nenhum erro de import/compile.
- Checklist acima todo verde.

## Commit sugerido
`verificação final e documentação do deploy windows`
