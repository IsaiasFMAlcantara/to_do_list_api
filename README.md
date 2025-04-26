# TO DO LIST (API) 📝

## Visão Geral
Uma API RESTful simples e robusta para gerenciamento de tarefas (To-Do List) com autenticação de usuários via token JWT. Ideal para uso em projetos pessoais, testes de integração ou como base para aplicações maiores.

## Funcionalidades

### 🛡️ Autenticação de Usuário
- **POST `/create_user`** – Cadastro de novo usuário.
- **POST `/login`** – Autenticação e geração de token JWT.
- **GET `/get_user`** - Busca usuário por id
- **POST `/logout`** (opcional) – Invalidação do token atual.

### 📝 Gerenciamento de Tarefas
- **GET `/todos`** – Lista todas as tarefas do usuário autenticado.
- **GET `/todos/:id`** – Retorna os detalhes de uma tarefa específica.
- **POST `/todos`** – Cria uma nova tarefa.
- **PUT `/todos/:id`** – Atualiza todos os campos de uma tarefa existente.
- **PATCH `/todos/:id/complete`** – Marca uma tarefa como concluída.
- **DELETE `/todos/:id`** – Remove uma tarefa.

## Observações
- Todas as rotas de tarefas exigem autenticação prévia (Bearer Token).
- Design de API pensado para escalabilidade e fácil manutenção.
- Padrão de resposta consistente (JSON) para facilitar integrações.

## Próximos Passos (Sugestão)
- Adicionar prioridade às tarefas (baixa, média, alta).