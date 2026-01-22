# Lead Capture System

Sistema web para captação e gerenciamento de leads através de uma landing page e painel administrativo.

## Funcionalidades

- **Captação de Leads**: Formulário completo em landing page
- **Validação de Dados**: Validação de campos obrigatórios e e-mail único
- **Login Administrativo**: Sistema de autenticação simples para proteger área administrativa
- **Dashboard**: Lista organizada de todos os leads cadastrados
- **Paginação**: Navegação entre páginas de leads (10 por página)
- **Detalhes do Lead**: Visualização completa das informações
- **Exclusão**: Remoção de leads com confirmação
- **Página de Sucesso**: Confirmação após cadastro

## Tecnologias

- **Python 3.8+**
- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados
- **Jinja2** - Template engine
- **HTML5, CSS3, JavaScript** - Frontend

## Instalação

### 1. Clone o repositório ou navegue até a pasta do projeto

```bash
cd lead_capture_system
```

### 2. Crie um ambiente virtual (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## Como Usar

### 1. Execute a aplicação

```bash
python app.py
```

### 2. Acesse no navegador

- **Landing Page**: http://localhost:5000
- **Login Administrativo**: http://localhost:5000/login
- **Dashboard**: http://localhost:5000/dashboard (requer login)

### 3. Credenciais de Demonstração

Para acessar a área administrativa, use as credenciais:

- **Usuário**: `admin`
- **Senha**: `admin123`

**Nota**: Estas são credenciais hardcoded para demonstração. Em produção, implemente um sistema de autenticação adequado.

## Estrutura do Projeto

```
lead_capture_system/
│
├── app.py                 # Aplicação Flask principal
├── models.py             # Modelos SQLAlchemy
├── requirements.txt      # Dependências Python
├── README.md            # Este arquivo
│
├── templates/           # Templates HTML
│   ├── base.html        # Template base
│   ├── index.html       # Landing page
│   ├── login.html       # Página de login administrativo
│   ├── sucesso.html     # Página de sucesso
│   ├── dashboard.html   # Dashboard de leads
│   └── detalhes.html    # Detalhes do lead
│
└── static/              # Arquivos estáticos
    ├── css/
    │   └── style.css    # Estilos CSS
    └── js/
        └── main.js      # JavaScript
```

## Campos do Formulário

- **Nome** (obrigatório)
- **E-mail** (obrigatório, único)
- **Telefone** (obrigatório)
- **Empresa** (opcional)
- **Mensagem** (opcional)

## Segurança

### Login Administrativo

O sistema possui um login administrativo simples com credenciais hardcoded para demonstração:

- **Usuário**: `admin`
- **Senha**: `admin123`

As seguintes rotas são protegidas e requerem autenticação:
- `/dashboard` - Lista de leads
- `/lead/<id>` - Detalhes do lead
- `/lead/<id>/excluir` - Exclusão de lead

O sistema utiliza Flask sessions para manter a autenticação durante a navegação.

**Importante para Produção**: 
- Antes de colocar em produção, altere a `SECRET_KEY` no arquivo `app.py`
- Implemente um sistema de autenticação adequado (banco de usuários, hash de senhas, etc.)
- As credenciais atuais são apenas para demonstração

Gere uma chave segura usando:

```python
import secrets
print(secrets.token_hex(32))
```

## Banco de Dados

O banco de dados SQLite (`leads.db`) é criado automaticamente na primeira execução. A tabela `leads` contém:

- `id` - ID único do lead
- `nome` - Nome completo
- `email` - E-mail (único)
- `telefone` - Telefone
- `empresa` - Nome da empresa (opcional)
- `mensagem` - Mensagem do lead (opcional)
- `data_cadastro` - Data e hora do cadastro

## Personalização

Os estilos podem ser personalizados editando `static/css/style.css`. As variáveis CSS no início do arquivo permitem fácil customização de cores.

## Notas

- O sistema não permite edição de leads (escopo propositalmente limitado)
- A paginação exibe 10 leads por página
- Os leads são ordenados por data de cadastro (mais recentes primeiro)
- E-mails duplicados não são permitidos

## Contribuindo

Este é um projeto de escopo fechado, mas sinta-se livre para adaptar conforme suas necessidades.

## Licença

Este projeto é livre para uso pessoal e comercial.

---

Desenvolvido usando Flask e Python
