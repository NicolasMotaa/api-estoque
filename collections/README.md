# Collections do Postman - API de Estoque

Esta pasta contém o arquivo `.json` com a collection do Postman para testes e documentação das rotas da API. Todos os endpoints já estão configurados com corpos de requisição (payloads) reais e exemplos de resposta (sucesso e erros de validação).

## Como importar
1. Abra o Postman.
2. Clique em **Import** no menu superior esquerdo.
3. Selecione e importe o arquivo `.json` contido neste diretório.

## Ordem sugerida de execução
O banco de dados utiliza chaves estrangeiras relacionais. Para testar o fluxo completo sem tomar erros de integridade (400/404), siga obrigatoriamente esta ordem de criação nos testes de `POST`:

1. **Categorias:** Crie ao menos uma categoria base (ID 1).
2. **Fornecedores:** Crie ao menos um fornecedor (ID 1).
3. **Produtos:** Crie produtos vinculando à Categoria 1 e Fornecedor 1. Teste o bloqueio de preço de venda menor que o custo e a listagem de estoque baixo.
4. **Movimentações:** Faça requisições de `ENTRADA` e `SAIDA` apontando para os produtos criados. Teste o bloqueio de estoque insuficiente tentando registrar uma saída maior que o saldo do produto.

*Nota para testes locais: se precisar recomeçar os testes do zero e resetar a contagem dos IDs de auto-incremento para 1, utilize os comandos do Alembic ou rode um `TRUNCATE` em cascata no banco.*