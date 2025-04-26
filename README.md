# TO DO LIST API 🛡️📝

## Visão Geral
Uma API RESTful **rápida, robusta e segura** para gerenciamento de tarefas com **autenticação JWT**. Ideal para projetos pessoais, testes, ou como ponto de partida para aplicações maiores.

## Como Rodar

### 1. Instalar o Poetry
```bash
pipx install poetry
```

### 2. Instalar Dependências
```bash
poetry install
```

### 3. Ativar Ambiente Virtual
```bash
eval $(poetry env activate)
```

### 4. Rodar a API
- **Modo Desenvolvimento**
  ```bash
  task dev
  ```
- **Modo Produção**
  ```bash
  task run
  ```

> **Obs:** `task` é usado para rodar tasks definidas no arquivo `Taskfile.yml`. Se não tiver instalado, use `poetry install`.

## Funcionalidades

### 🔐 Autenticação
- `POST /create_user` — Cria novo usuário.
- `POST /login` — Autentica usuário e gera token JWT.
- `GET /get_user` — Retorna dados do usuário autenticado.
- `POST /logout` *(opcional)* — Invalida o token atual.

### ✅ Gerenciamento de Tarefas
- `GET /todos` — Lista todas as tarefas.
- `GET /todos/:id` — Detalhes de uma tarefa específica.
- `POST /todos` — Cria uma nova tarefa.
- `PUT /todos/:id` — Atualiza uma tarefa inteira.
- `PATCH /todos/:id/complete` — Marca tarefa como concluída.
- `DELETE /todos/:id` — Deleta uma tarefa.

## Requisitos de Uso
- Autenticação via Bearer Token obrigatória em todas as rotas de tarefas.
- Respostas em **JSON** com estrutura padronizada para fácil integração.

## Boas Práticas Implementadas
- Código modular e escalável.
- Autenticação segura usando JWT.
- Pronto para deploy em produção.

## Próximos Passos
- [ ] Adicionar sistema de prioridade nas tarefas: **baixa**, **média**, **alta**.
- [ ] Implementar busca e filtros nas tarefas.
- [ ] Paginação nas listagens.