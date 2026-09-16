# Deploy no Windows Server

Guia para rodar a aplicação como serviço no Windows, atrás do nginx como proxy reverso (TLS).

## Arquitetura

```
LAN/Internet -> nginx (serviço Windows, :80/:443, TLS)
             -> 127.0.0.1:5000 (não exposto externamente)
             -> Waitress (serviço Windows "GestaoSaudeApp")
             -> MariaDB (serviço local, :3306)
```

## Pré-requisitos

- Windows Server (2016+).
- [Python 3.14](https://www.python.org/downloads/).
- [MariaDB](https://mariadb.org/download/) instalado como serviço local.
- [NSSM](https://nssm.cc/download) (extrair para `C:\nssm`).
- [nginx para Windows](https://nginx.org/en/download.html) (extrair para `C:\nginx`).

## Passo a passo

### 1. Código e dependências

```powershell
mkdir C:\apps\gestao_saude
# copie o repositório para C:\apps\gestao_saude
cd C:\apps\gestao_saude
python -m venv venv
.\venv\Scripts\python -m pip install --upgrade pip
.\venv\Scripts\python -m pip install -r requirements.txt
```

### 2. Banco de dados

1. Instale o MariaDB como serviço e crie o banco/usuário:
   ```sql
   CREATE DATABASE gestao_saude_db;
   CREATE USER 'gestao_saude_user'@'localhost' IDENTIFIED BY 'SENHA_FORTE';
   GRANT ALL PRIVILEGES ON gestao_saude_db.* TO 'gestao_saude_user'@'localhost';
   ```
2. O schema é criado automaticamente pelo bootstrap (`db.create_all()`) caso o banco
   esteja vazio. Para manter um schema já existente, restaure o dump do Linux
   **sem** os dados (só estrutura); o bootstrap insere os dados mínimos.

### 3. Variáveis de ambiente

1. Edite `set-env.ps1` com os valores reais.
2. Rode em um PowerShell **Administrador**:
   ```powershell
   .\deploy\windows\set-env.ps1
   ```

### 4. Serviço da aplicação

```powershell
# criar o diretório de logs
mkdir C:\apps\gestao_saude\logs

# instalar e iniciar o serviço (PowerShell Administrador)
.\deploy\windows\install-app-service.ps1
```

Para remover: `.\deploy\windows\uninstall-app-service.ps1`.

### 5. nginx (proxy reverso + TLS)

#### 5.1 Obter o certificado TLS

O nginx espera os arquivos em `C:\nginx\ssl\cert.pem` e `C:\nginx\ssl\privkey.pem`.
Gere com uma das opções abaixo, substituindo `aplicacao.example.com` pelo domínio real.

**Opção 1 — win-acme (Let's Encrypt), recomendada para domínio público**

1. Baixe o win-acme em https://github.com/win-acme/win-acme/releases e extraia
   (ex.: `C:\win-acme`).
2. Rode o assistente em um PowerShell **Administrador**:
   ```powershell
   cd C:\win-acme
   .\wacs.exe
   ```
3. No assistente:
   - `N` (criar novo certificado);
   - `M` (instalar manualmente) e indique `aplicacao.example.com`;
   - validação `http-01` (porta 80 acessível publicamente) ou `dns-01`
     (via subdomínio DuckDNS, se não tiver porta 80);
   - como destino da instalação, aponte para `C:\nginx\ssl\`.
4. A renovação fica agendada automaticamente (Agendador de Tarefas do Windows).

> Exige um domínio registrado (ou um subdomínio grátis, ex.: `*.duckdns.org`).

**Opção 2 — OpenSSL autoassinado, para teste/uso interno**

O OpenSSL já vem com o Git for Windows (`C:\Program Files\Git\usr\bin\openssl.exe`).

```powershell
New-Item -ItemType Directory -Force C:\nginx\ssl
& "C:\Program Files\Git\usr\bin\openssl.exe" req -x509 -nodes -newkey rsa:2048 `
  -days 365 `
  -keyout C:\nginx\ssl\privkey.pem `
  -out    C:\nginx\ssl\cert.pem `
  -subj "/CN=aplicacao.example.com"
```

> `-nodes` gera a chave **sem senha** (obrigatório: o nginx como serviço não consegue
> pedir passphrase). Esse certificado não é confiável — os navegadores exibem aviso.

Após gerar, restrinja o acesso à chave privada:

```powershell
icacls C:\nginx\ssl\privkey.pem /inheritance:r /grant:r "SYSTEM:(R)" "Administrators:(F)"
```

#### 5.2 Instalar o nginx

1. Copie `deploy\windows\nginx.conf` para `C:\nginx\conf\nginx.conf` e ajuste o
   `server_name` para `aplicacao.example.com`.
2. Confirme que os arquivos do certificado estão em `C:\nginx\ssl\cert.pem` e
   `C:\nginx\ssl\privkey.pem` (nunca no repositório).
3. Instale como serviço:
   ```powershell
   .\deploy\windows\install-nginx-service.ps1
   ```

### 6. Firewall

Abrir apenas `80` e `443`. A aplicação roda em loopback (`127.0.0.1:5000`) e não deve
ser exposta.

## Credenciais iniciais (seed)

O bootstrap cria um usuário administrador fictício quando o banco está vazio:

- Usuário: `admin`
- E-mail: `admin@example.com`
- Senha: `Mudar@123`

**Troque a senha no primeiro acesso.**

## Variáveis de ambiente

| Variável | Obrigatória | Padrão | Descrição |
|---|---|---|---|
| `DATABASE_URL` | sim | — | URL do MySQL/MariaDB |
| `SECRET_KEY` | sim | — | Chave secreta do Flask |
| `SESSION_COOKIE_SECURE` | não | `true` | Cookie de sessão apenas via HTTPS. Desligue (`false`) somente se a app for acessada por HTTP sem o nginx/TLS na frente |
| `EMAIL_USER`/`EMAIL_PASSWORD`/`EMAIL_SMTP_SERVER`/`EMAIL_SMTP_PORT` | não | — | Configuração SMTP |
| `APP_HOST`/`APP_PORT`/`APP_THREADS` | não | `127.0.0.1`/`5000`/`8` | Configuração do Waitress |
| `SEED_ON_EMPTY` | não | `true` | Habilita bootstrap de dados mínimos |
