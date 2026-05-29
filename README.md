# EchoMind - Totem de IA Institucional

EchoMind e um sistema de totem interativo com IA para instituicoes de ensino e empresas. O backend usa FastAPI, SQLAlchemy, pgvector, LangChain, Groq, FastEmbed e gTTS para responder perguntas com base na base de conhecimento cadastrada.

## Estrutura do projeto

```text
PI-EchoMind-auth/
├── echomind-backend/   # API FastAPI
└── echomind-front/     # Frontend Next.js
```

## Como rodar localmente

### Pre-requisitos

- Python 3.11+
- Conta no Supabase com projeto criado
- Chave de API do Groq em console.groq.com

### Configuracao

1. Instalar dependencias:

```bash
cd echomind-backend
pip install -r requirements.txt
```

2. Copiar e preencher o `.env`:

```bash
cp .env.example .env
```

Preencha `DATABASE_URL` com a connection string do Supabase e `GROQ_API_KEY` com sua chave.

3. Rodar as migrations:

```bash
alembic upgrade head
```

4. Popular o banco com dados iniciais e reindexar o pgvector:

```bash
python seed.py
```

5. Iniciar a API:

```bash
uvicorn app.main:app --reload
```

### Endpoints

Acesse [http://localhost:8000/docs](http://localhost:8000/docs) para a documentacao interativa.

## Variaveis de ambiente principais

| Variavel | Descricao |
| --- | --- |
| `DATABASE_URL` | URI PostgreSQL do Supabase. O backend adiciona `sslmode=require` automaticamente quando ausente. |
| `JWT_SECRET` | Chave usada para assinar tokens JWT. |
| `JWT_EXPIRE_HOURS` | Validade do token JWT em horas. |
| `SEED_ADMIN_EMAIL` | Email do admin criado pelo `seed.py`. |
| `SEED_ADMIN_PASSWORD` | Senha do admin criado pelo `seed.py`. |
| `GROQ_API_KEY` | Chave da API Groq. |
| `GROQ_LLM_MODEL` | Modelo Groq usado no chat. |
| `EMBED_MODEL` | Modelo local de embeddings. |
| `EMBEDDING_DIM` | Dimensao do vetor no pgvector. |
| `SIMILARITY_THRESHOLD` | Distancia maxima aceita no retrieval. |
| `TOP_K_DOCS` | Quantidade de documentos recuperados por pergunta. |

## Autenticacao

As rotas administrativas usam JWT Bearer. O login e feito em `POST /auth/login` com `application/x-www-form-urlencoded`, usando `username` como email e `password` como senha.

Credenciais padrao criadas pelo seed:

| Campo | Valor |
| --- | --- |
| Email | `admin@echomind.com` |
| Senha | `EchoMind@2025` |

## Rotas principais

| Metodo | Rota | Descricao |
| --- | --- | --- |
| `POST` | `/auth/login` | Login administrativo |
| `GET` | `/auth/me` | Usuario autenticado |
| `POST` | `/chat` | Chat com streaming |
| `GET/POST/PUT/DELETE` | `/faqs` | CRUD de FAQs |
| `GET/POST/PUT/DELETE` | `/events` | CRUD de eventos |
| `GET/PUT` | `/config` | Configuracoes institucionais |
| `GET/DELETE` | `/unanswered` | Perguntas nao respondidas |
| `POST` | `/unanswered/{id}/convert` | Converter pergunta em FAQ |
| `POST` | `/unanswered/{id}/learn` | Ensinar resposta ao RAG |
| `GET` | `/dashboard` | Metricas e estatisticas |
| `GET` | `/tts` | Sintese de voz MP3 |
| `GET` | `/health` | Health check |
| `GET` | `/metrics` | Metricas internas |

## Frontend

```bash
cd echomind-front
pnpm install
copy .env.local.example .env.local
pnpm dev
```

O frontend espera a API em `http://localhost:8000` por padrao.

## Ordem Recomendada Apos Atualizar Embeddings

```bash
cd echomind-backend
pip install -r requirements.txt
alembic upgrade head
python seed.py
uvicorn app.main:app --reload
```

Em outro terminal:

```bash
cd echomind-front
pnpm dev
```
