# GRS

> Game Recommendation System

Quick links: [中文版](#chinese-summary)

GRS is a game recommendation project that combines a rule-based matching pipeline with optional LLM-enhanced reranking.

---

## Overview

Users answer a quiz, the backend builds a preference profile from their choices, matches that profile against game tags, and returns ranked recommendations.

After the rule-based layer produces top candidates, an LLM can optionally rerank them and generate more natural recommendation reasons.

## Project Structure

```text
grs/
|-- frontend/                  # React + Vite frontend
|-- backend/                   # FastAPI + SQLModel backend
|   |-- app/                   # Application code
|   |-- alembic/               # Database migrations
|   |-- tests/                 # Backend tests
|   |-- data_pipeline/         # Seed files and import scripts
|   |-- requirements.txt
|   `-- .env.example
|-- .github/workflows/         # GitHub Actions CI
`-- README.md
```

## Tech Stack

| Layer | Stack |
| --- | --- |
| Frontend | React, Vite, React Router, i18next, Tailwind CSS |
| Backend | FastAPI, SQLModel, SQLAlchemy, Alembic, PostgreSQL, pytest |
| LLM Layer | OpenAI API, top-15 candidate reranking, top-3 explanation enhancement, rule-based fallback |

## Current Features

- Core product: home page, quiz page, result page, bilingual UI, database-backed questions, and a complete rule-based recommendation pipeline.
- Recommendation output: the backend returns top 15 candidates, and the frontend supports showing another batch of results with cover images.
- Data pipeline: JSON seed import plus game and game-tag upsert workflows under `backend/data_pipeline/`.
- LLM integration: optional reranking for top candidates and enhanced recommendation reasons for top results.
- Engineering: Alembic migrations, minimal backend API tests, and GitHub Actions CI.

## Recommendation Flow

```text
User answers quiz
-> validate_answers
-> build_user_profile
-> score_games
-> select_top_candidates(limit=15)
-> rerank_candidates_with_fallback
-> build_recommend_response
-> frontend displays results
```

## Local Development

### Frontend

From the project root:

```bash
cd frontend
pnpm install
pnpm dev
```

Typical local URL:

```text
http://localhost:5173
```

### Backend

From the project root:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

Typical local URL:

```text
http://127.0.0.1:8000
```

## Environment Variables

Create a `.env` file inside `backend/`.

You can copy the template from:

```text
backend/.env.example
```

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/grs
OPENAI_API_KEY=
OPENAI_RERANK_MODEL=gpt-5.4-mini
OPENAI_RERANK_ENABLED=false
```

| Variable | Description |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection string |
| `OPENAI_API_KEY` | OpenAI API key |
| `OPENAI_RERANK_MODEL` | Model used for reranking |
| `OPENAI_RERANK_ENABLED` | Whether LLM reranking is enabled |

## Database and Migrations

Run migrations:

```bash
cd backend
alembic upgrade head
```

Create a new migration:

```bash
alembic revision --autogenerate -m "your migration message"
```

## Data Pipeline

The main data workflow lives in:

```text
backend/data_pipeline/
```

It stores JSON seed files and import or update scripts.

Reset business data:

```bash
cd backend
python -m app.db.reset_seed_data
```

Import full JSON seed data:

```bash
python -m app.db.import_json_seed_data
```

Upsert games and game-tag relations:

```bash
python -m app.db.upsert_games_and_tags
```

## Testing

Run backend tests from `backend/`:

```bash
python -m pytest
```

Current minimal test coverage includes:

- `GET /questions`
- `POST /recommend`
- invalid answer rejection
- rule-based flow when LLM reranking is disabled

## CI

The project uses GitHub Actions for minimal CI checks.

Current CI coverage:

- frontend install + build
- backend install + pytest

Workflow file:

```text
.github/workflows/ci.yml
```

## LLM Reranking

The LLM does not replace the full recommendation system. It works only on the candidate set produced by the rule-based layer.

What the LLM does:

- reranks the top 15 rule-based candidates
- generates better reasons for the top 3 results

What the LLM does not do:

- recommend arbitrary games outside the candidate set
- replace the database or tag system
- replace the rule-based scoring pipeline

Fallback to rule-based results happens when:

- LLM reranking is disabled
- API calls fail
- model output is invalid
- model output fails business validation

## Notes

- Older development-only seed scripts are no longer the primary data entry path.
- The recommended data workflow now lives under `backend/data_pipeline/`.

---

<a id="chinese-summary"></a>

## 中文简版

### 项目简介

GRS 是一个游戏推荐系统项目，核心流程是：

- 用户填写问卷
- 后端根据答案构建偏好画像
- 使用标签和权重进行规则匹配
- 返回排序后的推荐结果

在规则推荐结果的基础上，系统还可以选择接入 LLM，对候选游戏进行精排，并优化推荐理由。

### 技术栈

- 前端：React、Vite、React Router、i18next、Tailwind CSS
- 后端：FastAPI、SQLModel、SQLAlchemy、Alembic、PostgreSQL、pytest
- LLM：OpenAI API，用于候选结果精排和推荐理由增强

### 当前功能

- 提供首页、问卷页和结果页
- 支持中英文界面
- 问题数据从数据库读取
- 后端可返回 Top 15 推荐结果
- 前端支持继续查看下一批结果
- 集成 JSON seed 导入与数据更新脚本
- 支持 Alembic 迁移、基础接口测试和 GitHub Actions CI

### 本地运行

前端：

```bash
cd frontend
pnpm install
pnpm dev
```

后端：

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 环境变量

在 `backend/` 下创建 `.env` 文件，可参考 `backend/.env.example`。

关键变量包括：

- `DATABASE_URL`
- `OPENAI_API_KEY`
- `OPENAI_RERANK_MODEL`
- `OPENAI_RERANK_ENABLED`

### 测试与数据脚本

运行测试：

```bash
cd backend
python -m pytest
```

常用数据脚本：

```bash
python -m app.db.reset_seed_data
python -m app.db.import_json_seed_data
python -m app.db.upsert_games_and_tags
```
