# Achados UFLA

Sistema web para cadastro e recuperação de objetos perdidos e encontrados no
ambiente universitário. Projeto acadêmico da disciplina GAC116 — Programação Web.

## Integrantes

- [Daniel Silva Ferraz Neto — Clofender](https://github.com/Clofender)
- [José Víctor Miranda de Oliveira — zector1](https://github.com/zector1)

## Status e funcionalidades

Em desenvolvimento — o portal público usa Django Templates, com autenticação
por sessão, perfis, catálogo de objetos, ocorrências e validação de devoluções.
A dashboard e todas as páginas do portal usam o mesmo tema e consultam o SQLite.
O Django Admin com Jazzmin continua disponível para a equipe.

Funcionalidades implementadas:

- cadastro, consulta, edição e exclusão de categorias, locais, objetos e ocorrências;
- objetos com status perdido, encontrado, devolvido ou arquivado;
- ocorrências de perda ou achado relacionadas a objeto, local e usuário responsável;
- buscas, filtros, navegação por datas e campos com autocomplete no Admin;
- validação de datas de ocorrências e das características de objetos devolvidos;
- dashboard com totais e registros recentes vindos do banco;
- cadastro, login, perfil e logout de usuários;
- catálogo com busca, filtros e paginação;
- cadastro e edição protegidos por proprietário;
- solicitações de devolução com aprovação transacional;
- comando para gerar dados fictícios de demonstração;
- página auxiliar Vite que encaminha para o portal Django principal.

O acesso ao Admin continua restrito a usuários com `is_staff` e permissões.

## Tecnologias

- Python 3.12 e Django 5.2;
- SQLite como banco de dados relacional;
- Jazzmin 3.0.5, com Bootstrap no ambiente administrativo;
- React 19 e Vite 8 como página auxiliar de redirecionamento;
- Git e GitHub.

## Requisitos

- Python 3.12 ou superior no PATH, compatível com Django 5.2;
- Node.js 20.19+ ou 22.12+ e npm; ambiente validado com Node.js 24;
- Git.

As instruções abaixo usam PowerShell no Windows e não exigem ativar o ambiente
virtual. No Linux/macOS, use `.venv/bin/python` no lugar de
`.\.venv\Scripts\python.exe` e `python3` para criar o ambiente.

## Instalação do backend

Clone o projeto, entre na pasta do repositório e selecione `develop`:

```powershell
git clone https://github.com/Clofender/achados-ufla.git
cd achados-ufla
git switch develop
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Se o comando `python` não estiver disponível, use `py -3.12` ou o caminho completo
do Python instalado para criar o ambiente virtual.

Na raiz do repositório, configure uma chave para a sessão e prepare o banco:

```powershell
$env:DJANGO_SECRET_KEY = & .\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
.\.venv\Scripts\python.exe backend/manage.py migrate
.\.venv\Scripts\python.exe backend/manage.py createsuperuser
```

Escolha usuário, e-mail e senha quando solicitado. Cada integrante deve criar
suas próprias credenciais locais. O SQLite é criado em `backend/db.sqlite3` e
está fora do versionamento.

`backend/.env.example` documenta a variável `DJANGO_SECRET_KEY`. Arquivos `.env`
não são carregados automaticamente: a configuração atual lê as variáveis do
ambiente. Sem a variável, há uma chave de fallback exclusiva para desenvolvimento.

## Execução e acesso ao Admin

A partir da raiz do repositório:

```powershell
.\.venv\Scripts\python.exe backend/manage.py runserver
```

Abra [http://127.0.0.1:8000/](http://127.0.0.1:8000/) para o portal ou
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) para a administração.

O superusuário pode administrar todos os modelos. Outros usuários precisam ter
`is_staff` habilitado e as permissões correspondentes, atribuídas no Admin.

### Dados de demonstração

O comando cria contas locais, categorias, locais, objetos e ocorrências:

```powershell
.\.venv\Scripts\python.exe backend/manage.py seed_demo
```

As contas `demo_aluno`, `demo_moderador` e `demo_admin` usam a senha local
`Demo12345!`. Para usar um usuário existente como proprietário, informe
`--username seu_usuario`. Nunca use as credenciais de demonstração em produção.

## Permissões, segurança e fluxo de demonstração

Cada usuário possui um `Profile` com telefone, matrícula e papel
(`student`, `moderator` ou `admin`). Usuários comuns só editam seus próprios
objetos e ocorrências. Moderadores e administradores validam ocorrências; a
aprovação de devolução atualiza a ocorrência e o objeto dentro de uma transação.
O proprietário de um objeto é atribuído no servidor, nunca pelo formulário.

Uploads são validados por extensão e tamanho (até 5 MB) e armazenados em
`MEDIA_ROOT`. Em produção, configure `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`,
HTTPS e um armazenamento de mídia apropriado.

Para ensaiar a apresentação: crie uma conta, cadastre um objeto encontrado,
registre uma solicitação de devolução e aprove-a com `demo_moderador`. O
dashboard mostrará o objeto como devolvido.

## Capturas de tela

As telas podem ser capturadas durante a execução local do portal em
`http://127.0.0.1:8000/`. A sequência recomendada é: dashboard, catálogo com
filtros, formulário de cadastro, detalhe da ocorrência e painel administrativo.

### Filtros e buscas disponíveis

| Listagem | Filtros | Busca |
| --- | --- | --- |
| Categorias | Ativa/inativa | Nome e descrição |
| Locais | — | Nome e descrição |
| Objetos | Status, categoria, local e data de criação | Título, descrição, características, categoria e local |
| Ocorrências | Tipo, local e data da ocorrência | Título do objeto, local, usuário responsável e observações |

Objetos e ocorrências também possuem navegação por ano, mês e dia. Os formulários
de objetos oferecem autocomplete de categoria e local; os de ocorrências, de
objeto, local e responsável.

## Acesso ao portal

O portal completo, incluindo dashboard, autenticação, catálogo e formulários,
é servido pelo Django e usa o banco SQLite. Inicie apenas o backend:

```powershell
.\.venv\Scripts\python.exe backend/manage.py runserver
```

Abra [http://127.0.0.1:8000/](http://127.0.0.1:8000/). O Vite em
`http://127.0.0.1:5173/` é opcional e apenas encaminha para o portal; não é uma
interface separada nem mantém dados próprios.

Para usar essa página auxiliar, instale e inicie o Vite em outro terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Se o PowerShell bloquear `npm.ps1`, use `npm.cmd` no lugar de `npm`.
O banco, login e operações de objetos continuam centralizados no Django.

Para validar a página auxiliar:

```powershell
npm run build
npm run preview
```

Os arquivos gerados ficam em `frontend/dist/`, ignorados pelo Git. O servidor de
preview é apenas para conferir o build localmente.

## Verificações do backend

Execute na raiz do repositório:

```powershell
.\.venv\Scripts\python.exe backend/manage.py check
.\.venv\Scripts\python.exe backend/manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe backend/manage.py test core occurrences
```

As migrations existentes são aplicadas por `migrate`; a verificação acima apenas
confirma se há alterações nos modelos sem migrations correspondentes.

## Modelagem e estrutura

O app `core` contém `Category`, `Location` e `Item`; `occurrences` contém
`Occurrence`. A autenticação utiliza o usuário padrão do Django. O local do objeto
é sua referência atual; o local da ocorrência registra onde aconteceu cada evento.

Categorias e locais utilizados são protegidos contra exclusão, assim como o usuário
responsável por uma ocorrência. Excluir um objeto também exclui suas ocorrências.
Consulte o [diagrama e as regras do modelo relacional](docs/modelo-er.md).

```text
achados-ufla/
├── backend/
│   ├── config/             # configurações, URLs e tema Jazzmin
│   ├── core/               # categorias, locais, objetos e seed_demo
│   ├── occurrences/        # registros de perda e achado
│   ├── .env.example        # referência de configuração
│   └── manage.py
├── frontend/
│   ├── src/                # página inicial React e estilos
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
├── docs/
│   └── modelo-er.md
├── .gitignore
├── requirements.txt
└── README.md
```

## Colaboração

As três entregas de finalização do Checkpoint 1 são feitas na branch `develop`.
`main` reúne a versão estável, e as branches `feature/...` preservam o histórico
das etapas de desenvolvimento.
