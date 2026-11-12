# DiagPlan Software — Controle de Estoque OXXO

MVP acadêmico desenvolvido para demonstrar o cadastro de produtos, controle de lotes e validade, movimentações de entrada e saída e consulta de estoque.

## Tecnologias utilizadas

- Python
- Flask
- SQLite (sqlite3)
- HTML
- CSS
- JavaScript
- Bootstrap 5
- Pytest

## Funcionalidades do MVP

- Cadastro de produtos com nome, categoria e SKU.
- Registro de entradas de produtos.
- Criação de lotes com datas de validade.
- Registro de saídas de mercadorias.
- Controle da quantidade disponível em estoque.
- Consulta do saldo total por produto.
- Listagem de lotes e respectivas datas de validade.
- Identificação de produtos vencidos.
- Identificação de produtos próximos do vencimento.
- Painel com resumo do estoque.
- Histórico de movimentações realizadas.

## Controle de validade dos produtos

O DiagPlan possui funcionalidades para auxiliar no acompanhamento da validade das mercadorias.

- Identifica lotes com produtos vencidos.
- Permite consultar a situação de cada lote.
- Prioriza a retirada dos lotes com vencimento mais próximo (FIFO).
- Impede a saída de produtos com validade vencida.
- Evita movimentações de saída em quantidade superior ao estoque disponível dentro da validade.
- Auxilia na prevenção de perdas de mercadorias.

## Como executar localmente

1. Instale o Python.
2. Abra o terminal na pasta do projeto.
3. Crie um ambiente virtual:

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Inicie o sistema:

```bash
python app.py
```

6. Acesse pelo navegador:

```text
http://127.0.0.1:5000
```

O banco de dados `diagplan.db` é criado automaticamente na primeira execução.

## Executar os testes

Para executar os testes automatizados, utilize:

```bash
pytest
```

## Estrutura do projeto

```text
diagplan_oxxo/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── product_form.html
│   ├── movements.html
│   └── lots.html
└── tests/
    └── test_app.py
```

## Limites e próximos passos

Este projeto é um MVP acadêmico demonstrativo e não possui integração com os sistemas internos da rede OXXO.

Como melhorias futuras, são recomendadas:

- Implementação de autenticação de usuários.
- Criação de perfis de acesso.
- Registro de auditoria das operações.
- Validação de permissões.
- Proteção contra ataques CSRF.
- Configuração segura da chave secreta da aplicação.
- Implementação de backups do banco de dados.
- Melhorias nos relatórios de estoque.
- Implantação em servidor para acesso externo.

## Contexto acadêmico

O projeto DiagPlan Software foi desenvolvido com o objetivo de propor uma solução para o controle de mercadorias e acompanhamento de datas de validade em uma loja de conveniência.

A proposta busca facilitar o trabalho dos funcionários e gerentes, melhorar a organização do estoque, identificar produtos próximos do vencimento e reduzir perdas de mercadorias.

O sistema representa uma proposta acadêmica e não possui vínculo ou integração oficial com a rede OXXO.

O sistema também permite identificar lotes vencidos e controlar as saídas de acordo com a validade dos produtos.

## Auto-revisão técnica do MVP

Foi realizada uma auto-revisão técnica do projeto DiagPlan Software, considerando os seguintes aspectos:

### Arquitetura
A aplicação utiliza Flask para organizar as rotas e regras de negócio, SQLite para armazenar os dados e HTML, CSS e JavaScript para a interface. Essa estrutura atende ao escopo do MVP e permite futuras melhorias.

### Legibilidade e organização
O projeto possui arquivos separados para aplicação, modelos de interface, estilos, testes e documentação. Essa organização facilita a manutenção e a identificação de cada responsabilidade.

### Regras de negócio
Foi revisado o controle de entradas e saídas, a consulta de estoque e o acompanhamento da validade dos lotes. A retirada considera os lotes dentro da validade e prioriza os vencimentos mais próximos.

### Segurança
Foi identificado que, antes de uma utilização em ambiente real, o sistema precisa de autenticação, controle de permissões, proteção CSRF e configuração segura da chave secreta. O modo de depuração também deve ser desativado em produção.

### Melhorias futuras
Recomenda-se ampliar os testes automatizados, reforçar as validações dos dados recebidos e implementar controles adicionais de segurança.

### Resultado da revisão
A estrutura atual atende à proposta acadêmica do MVP. Foram identificados pontos de melhoria para aumentar a segurança, a manutenção e a confiabilidade do sistema.