# DiagPlan Software — Controle de Estoque OXXO

MVP acadêmico para demonstrar cadastro de produtos, controle de lotes e validade, movimentações de entrada e saída e consulta de estoque.

## Tecnologias
- Python 3.12
- Flask
- SQLite (`sqlite3`)
- HTML, CSS, JavaScript e Bootstrap 5
- Pytest

## Funcionalidades do MVP
- Cadastro de produtos com nome, categoria e SKU.
- Registro de entradas, com criação de lote e validade opcional.
- Registro de saídas, impedindo retirada acima do estoque disponível.
- Consulta do saldo total por produto.
- Listagem de lotes e datas de validade.
- Painel com resumo do estoque, lotes próximos do vencimento e movimentações recentes.
- Histórico de movimentações.

## Como executar localmente

1. Instale Python 3.12.
2. Abra o terminal na pasta do projeto.
3. Crie e ative um ambiente virtual:

   **Windows**
   ```bash
   py -3.12 -m venv .venv
   .venv\Scripts\activate
   ```

   **Linux/macOS**
   ```bash
   python3.12 -m venv .venv
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

6. Acesse `http://127.0.0.1:5000` no navegador.

O banco `diagplan.db` é criado automaticamente na primeira execução.

## Executar os testes
```bash
pytest
```

## Estrutura
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
Este é um MVP demonstrativo e não está integrado aos sistemas internos do OXXO. Antes de uso real, recomenda-se adicionar autenticação e perfis de acesso, trilha de auditoria, validação de permissões, proteção CSRF, configuração segura de `SECRET_KEY`, backups e implantação em servidor.

## Contexto acadêmico
Projeto DiagPlan Software, voltado ao problema de controle de mercadorias e acompanhamento de validade em uma loja de conveniência. O sistema é uma proposta acadêmica e não representa produto oficial nem integração com a rede OXXO.
