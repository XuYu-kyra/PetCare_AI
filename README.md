# PetCare AI — Intelligent Veterinary Dialogue Prototype

[English](#english) · [中文](#中文)

## English

PetCare AI is a Django prototype for turning a pet-care question into a layered answer: retrieve similar knowledge from a local Q&A corpus, extract Chinese keywords, optionally run a BERT-style answer step, and connect to an external conversational model for richer responses.

### The story

Veterinary dialogue is a good test of applied NLP because users ask short, ambiguous questions and expect an answer that feels both relevant and conversational. I built the project as an experiment in combining deterministic retrieval with model-based generation instead of relying on one opaque response path.

### What I built

- A Django web application with separate question-answering and administration flows.
- Persistent Q&A models (`QandA`, `Oridata`, and `ODIndex`) plus migrations for evolving the local knowledge base.
- Chinese keyword extraction with `jieba`, TF–IDF vectorisation, cosine similarity, and nearest-neighbour retrieval.
- A layered response path that can combine retrieved answers, a BERT question-answering step, and an external SparkAI chat model.
- A simple browser interface and Django Admin workflow for managing data and testing interactions.

### Quick start

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows:    .\.venv\Scripts\Activate.ps1
pip install django jieba numpy scikit-learn torch transformers spark-ai-python
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Review [`cwyl/views.py`](cwyl/views.py) and [`cwyl/models.py`](cwyl/models.py) for the retrieval and data paths.

### Engineering notes

The repository is a learning/research prototype, not a medical diagnostic system. External API credentials should be supplied through environment variables and rotated before any public deployment; do not copy secrets from historical code into a new environment. A production version would also add retrieval evaluation, model caching, request validation, rate limits, and explicit medical-safety messaging.

## 中文

PetCare AI 是一个 Django 宠物健康问答原型：用户提出问题后，系统可以从本地问答库检索相似内容，提取中文关键词，运行 BERT 风格的答案抽取步骤，并连接外部对话模型生成更自然的回复。

### 项目故事

宠物健康问答很适合验证应用型 NLP：用户问题通常很短、上下文不完整，但又希望得到相关且像对话一样的回答。我没有只依赖一个黑盒接口，而是把确定性的检索链路和模型生成链路并列起来，便于比较、调试和继续迭代。

### 我的工作

- 搭建 Django 页面、问答接口和 Admin 管理流程；
- 设计 `QandA`、`Oridata`、`ODIndex` 数据模型及迁移，支持本地知识库演进；
- 使用 `jieba`、TF–IDF、余弦相似度和近邻搜索实现中文问题检索；
- 组合检索答案、BERT 问答步骤和 SparkAI 对话模型，形成分层响应路径；
- 提供浏览器端交互和可管理的数据录入入口，方便快速演示和实验。

### 快速运行

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install django jieba numpy scikit-learn torch transformers spark-ai-python
python manage.py migrate
python manage.py runserver
```

打开 `http://127.0.0.1:8000/`。核心检索与响应逻辑见 [`cwyl/views.py`](cwyl/views.py)，数据模型见 [`cwyl/models.py`](cwyl/models.py)。

### 边界与下一步

这是学习/研究原型，不是医疗诊断系统。公开部署前应把外部 API 凭据改为环境变量并轮换历史密钥；后续还应补充检索评测、模型缓存、输入校验、限流和明确的医疗安全提示。
