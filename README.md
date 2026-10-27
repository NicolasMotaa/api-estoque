# API de Gerenciamento de Estoque

Uma API RESTful robusta desenvolvida para gestão de estoque, controle de fornecedores e auditoria de movimentações de produtos. O sistema foi projetado com foco em integridade de dados, histórico de auditoria imutável e arquitetura escalável.

## > Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Framework Web:** FastAPI
* **Banco de Dados:** PostgreSQL
* **ORM & Migrations:** SQLAlchemy + Alembic
* **Validação de Dados:** Pydantic V2
* **Testes Automatizados:** Pytest e `unittest.mock`

## > Arquitetura e Padrões de Projeto

O projeto adota princípios de **Clean Architecture** e separação de responsabilidades em camadas lógicas:
* **Routers/Controllers:** Gerenciamento de rotas e injeção de dependências.
* **Services:** Isolamento das regras de negócio.
* **Repositories:** Abstração do acesso ao banco de dados (Repository Pattern).
* **Schemas (DTOs):** Validação estrita de entrada e saída via Pydantic.

## > Principais Funcionalidades

### - Gestão de Catálogo (CRUD)
* Gerenciamento completo de **Produtos**, **Fornecedores** e **Categorias**.
* **Integridade Referencial:** Bloqueio de exclusão de categorias e fornecedores que possuam produtos vinculados no sistema.
* Validação estrita de regras de negócio (ex: preço de venda não pode ser menor que o preço de custo, impedimento de CNPJs ou códigos duplicados).

### - Auditoria de Movimentações
* Sistema de **Movimentações de Estoque (Entradas e Saídas)**.
* **Imutabilidade:** Registros de movimentação não podem ser alterados ou excluídos após a criação, garantindo um histórico de auditoria confiável.
* Atualização em tempo real do saldo de produtos a cada transação registrada.

### - Consultas Estratégicas
* Monitoramento de estoque: Endpoint dedicado para listar produtos que atingiram ou caíram abaixo do nível de estoque mínimo.
* Relatórios de movimentação: Filtragem avançada por período (data de início e fim) e por fornecedor.

### - Tratamento de Erros e Validação
* Respostas de erro padronizadas, utilizando os códigos HTTP adequados (400 Bad Request, 404 Not Found, 422 Unprocessable Entity, 500 Internal Server Error).
* Tratamento centralizado de exceções, garantindo que "stack traces" não sejam expostos ao cliente.

## 📚 Documentação da API

A documentação interativa baseada no padrão OpenAPI pode ser acessada de duas formas:
1. **Swagger UI:** Acessando a rota `/docs` após inicializar o servidor local.
2. **Postman Collection:** O arquivo `.json` com todos os *payloads* reais, rotas e exemplos mapeados de respostas (sucesso e erro) está disponível no diretório `collections/` deste repositório para importação.

## Instalação, Execução e Testes

Siga o passo a passo abaixo para configurar o ambiente, rodar a API e validar as regras de negócio.

**1. Preparação do Ambiente:**
```bash
# Clone o repositório e acesse a pasta
git clone [https://github.com/seu-usuario/api-estoque.git](https://github.com/seu-usuario/api-estoque.git)
cd api-estoque

# Crie e ative o ambiente virtual (Linux/Mac)
python -m venv .venv
source .venv/bin/activate
# Obs: No Windows, utilize .venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

```
**2. Configuração do Banco de Dados:**
```
Crie um arquivo .env na raiz do projeto contendo a sua string de conexão com o PostgreSQL:
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
```
**3. Migrations, Testes e Execução:**
```
# Construa as tabelas estruturais no banco de dados
alembic upgrade head

# Execute a suíte de testes unitários com cobertura da camada de Services
pytest -v

# Inicie o servidor da API
uvicorn main:app --reload
```

**A API estará disponível em http://localhost:8000 e a documentação interativa em http://localhost:8000/docs.**
