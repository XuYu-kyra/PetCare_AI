# PetCare AI — Explainable Chinese Pet-Care Q&A Prototype

[English](#english) · [中文](#中文)

PetCare AI is a Django-based Chinese question-answering prototype that places **local retrieval, extractive language-model experiments, and optional conversational generation** behind one web interface. Its purpose is to make different answer paths visible and comparable instead of hiding every decision behind a single generated response.

> The project is designed for educational exploration and information assistance. It does not replace professional veterinary diagnosis.

## English

### Project concept

A pet-care question may be answered in several ways: retrieve a closely related answer from a maintained knowledge base, extract a span from a supplied context, or ask a conversational model to generate a response. Each approach offers different levels of traceability and flexibility.

I built PetCare AI as a layered prototype that keeps these routes separate:

```text
Chinese user question
        │
        ├──► jieba keywords ─► TF-IDF vectors ─► cosine/KNN retrieval
        │                                      └─► local Q&A answers
        │
        ├──► bert-base-chinese extractive QA experiment
        │
        └──► optional SparkAI conversation API
                         │
                         ▼
                Django JSON response
                         │
                         ▼
                 browser chat interface
```

The local retrieval branch remains usable without an external model account. SparkAI is an optional integration and is only called when all required credentials are present.

### What I implemented

#### Django application and data workflow

- Built the Django project, URL routing, views, templates, static assets, and JSON response path for the chat interface.
- Designed `QandA`, `Oridata`, and `ODIndex` models with migrations for question-answer content and indexing experiments.
- Registered the data models with Django Admin and `django-import-export` so source material can be searched, imported, reviewed, and exported without editing code.
- Added a separate inverted-index builder that tokenises source records and persists keyword-to-document mappings in `ODIndex`.

#### Chinese retrieval pipeline

- Extracted Chinese keywords with `jieba.analyse`.
- Built TF-IDF vectors from the current `QandA` records and compared the incoming question through cosine similarity.
- Used `NearestNeighbors` to return several related answers while keeping the highest-similarity answer as the primary local response.
- Sized the neighbour count to the available corpus, allowing small datasets to run without a fixed minimum record count.

#### Model integrations

- Added an extractive QA experiment with `bert-base-chinese`, `BertTokenizer`, and `BertForQuestionAnswering` to explore span selection from a supplied answer context.
- Integrated SparkAI through its Python SDK as a separate conversational response branch.
- Kept SparkAI credentials, Django settings, allowed hosts, and optional stopword paths in environment-based configuration.

#### Browser interaction

- Created a Chinese chat page with user and assistant message states.
- Connected the interface to the Django endpoint through Ajax and rendered local retrieval, extractive-model, and optional external-model outputs as separate responses.
- Included empty-input checks, disabled-button states during requests, scrolling behaviour, and fallback messages for unanswered queries.

### Why the answer paths are separated

The application intentionally does not collapse every output into one “best” answer. Local corpus retrieval is easy to trace back to maintained records; extractive QA tests whether a span can be selected from context; external generation offers more conversational flexibility. Returning these paths separately makes their behaviour easier to inspect and compare during development.

This also keeps the deterministic local path independent: the knowledge base and retrieval interface continue to work when SparkAI is not configured.

### Tech stack

| Area | Technology | Role |
|---|---|---|
| Web application | Django, Django Admin, SQLite | Routing, data models, management interface, and responses |
| Data operations | `django-import-export` | Import/export and review of Q&A records |
| Chinese NLP | jieba | Tokenisation and keyword extraction |
| Retrieval | TF-IDF, cosine similarity, scikit-learn KNN | Local question matching and related-answer retrieval |
| Extractive experiment | Transformers, PyTorch, `bert-base-chinese` | Context-based answer-span exploration |
| Conversational model | SparkAI Python SDK | Optional external response generation |
| Front end | HTML, CSS, JavaScript, jQuery/Ajax | Chat interaction and multi-path result display |
| Configuration | Environment variables | Secrets, Django options, endpoints, and local resource paths |

### Configuration

[`.env.example`](.env.example) documents the supported values. Load them through your shell or deployment environment; real credentials should remain outside version control.

```powershell
$env:DJANGO_SECRET_KEY = 'replace-with-a-random-secret'
$env:DJANGO_ALLOWED_HOSTS = '127.0.0.1,localhost'
$env:SPARKAI_APP_ID = 'replace-with-your-app-id'
$env:SPARKAI_API_KEY = 'replace-with-your-api-key'
$env:SPARKAI_API_SECRET = 'replace-with-your-api-secret'
```

`STOPWORDS_PATH` is optional. When it is not set, the index builder looks for `data/stopwords.txt` relative to the project; if the file is absent, it continues with an empty stopword list.

### Run locally

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows:     .\.venv\Scripts\Activate.ps1

pip install django django-import-export jieba numpy scikit-learn torch transformers spark-ai-python
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/admin/` to import or create `QandA` records, then use the question-answering page to test the retrieval flow. SparkAI is optional; without its credentials, the local retrieval and extractive branches remain available.

### Project scope

The repository represents a working learning prototype for comparing Chinese QA approaches inside one web application. The primary engineering focus is the full path from managed source records to retrieval, model adapters, structured responses, and browser interaction—not the claim of a clinically validated veterinary model.

---

## 中文

PetCare AI 是一个基于 Django 的中文宠物知识问答原型。我把 **本地知识库检索、抽取式语言模型实验和可选的对话模型调用** 放在同一个 Web 应用中，但保留三条回答链路各自的结果，使不同方法的依据和行为能够被直接观察，而不是全部藏在一个生成答案背后。

> 项目用于技术学习与信息辅助，不替代专业兽医诊断。

### 项目思路

同一个宠物护理问题可以有不同的处理方式：从已维护的问答库中找到相近问题，基于给定上下文抽取答案片段，或者交给对话模型生成更自然的回复。这三种方式在可追溯性、灵活性和外部依赖上并不相同。

因此，我将系统设计为三条彼此独立的路径：

```text
中文用户问题
      │
      ├──► jieba 关键词 ─► TF-IDF 向量 ─► 余弦相似度 / KNN
      │                                  └─► 本地问答库结果
      │
      ├──► bert-base-chinese 抽取式问答实验
      │
      └──► 可选的 SparkAI 对话接口
                       │
                       ▼
                Django JSON 响应
                       │
                       ▼
                  浏览器聊天界面
```

本地检索不依赖外部模型账号，可以单独运行；只有在配置完整凭据后，系统才会调用 SparkAI 分支。

### 我的实现

#### Django 应用与数据管理

- 完成 Django 项目结构、URL 路由、视图、模板、静态资源和聊天接口的 JSON 返回；
- 设计 `QandA`、`Oridata` 和 `ODIndex` 数据模型及对应 migration，用于保存问答内容和索引实验数据；
- 将模型接入 Django Admin 与 `django-import-export`，可以在管理页面中检索、导入、检查和导出语料，无需直接修改代码；
- 实现独立的倒排索引构建功能：对原始记录分词，并将关键词到文档 ID 的映射持久化到 `ODIndex`。

#### 中文检索流程

- 使用 `jieba.analyse` 从用户问题中提取中文关键词；
- 根据当前 `QandA` 数据动态构建 TF-IDF 向量，并通过余弦相似度比较用户问题；
- 使用 scikit-learn 的 `NearestNeighbors` 返回若干相关答案，同时将相似度最高的答案作为主要本地回复；
- 根据现有语料数量动态确定近邻个数，使少量数据也可以运行，而不依赖固定的数据规模。

#### 模型接入

- 使用 `bert-base-chinese`、`BertTokenizer` 和 `BertForQuestionAnswering` 实现抽取式问答实验，观察模型如何从给定文本中选择答案区间；
- 通过 SparkAI Python SDK 接入独立的对话生成分支；
- 将 SparkAI 凭据、Django secret、允许访问的 host 和停用词路径全部改为环境配置，避免依赖某台电脑的绝对路径。

#### 前端交互

- 实现中文聊天页面和用户/助手两类消息状态；
- 通过 Ajax 调用 Django 接口，将本地检索、抽取模型和可选外部模型的结果分别展示；
- 加入空输入检查、请求期间按钮禁用、消息区滚动和未找到答案时的反馈。

### 为什么保留三类结果

这个项目没有把所有输出强行合成为一个“最终答案”。本地检索能够回溯到维护过的问答记录；抽取式模型用于观察从上下文中选择片段的效果；外部对话模型则提供更自由的自然语言表达。分开返回结果，可以更直观地比较每条链路在实际问题上的表现，也便于定位问题来自语料、检索还是模型调用。

这种结构还保证了本地路径的独立性：即使没有配置 SparkAI，知识库管理、TF-IDF/KNN 检索和 Web 界面仍然可以工作。

### 技术栈

| 模块 | 技术 | 在项目中的作用 |
|---|---|---|
| Web 应用 | Django、Django Admin、SQLite | 路由、数据模型、管理后台与接口响应 |
| 数据操作 | `django-import-export` | 问答语料的导入、导出与检查 |
| 中文 NLP | jieba | 分词与关键词提取 |
| 本地检索 | TF-IDF、余弦相似度、scikit-learn KNN | 问题匹配与相关答案召回 |
| 抽取式实验 | Transformers、PyTorch、`bert-base-chinese` | 从上下文中选择答案区间 |
| 对话模型 | SparkAI Python SDK | 可选的外部生成式回复 |
| 前端 | HTML、CSS、JavaScript、jQuery/Ajax | 聊天交互与多路径结果展示 |
| 配置 | 环境变量 | 管理认证信息、Django 参数、服务地址和本地资源路径 |

### 配置

[`.env.example`](.env.example) 列出了可用配置项。实际值通过终端或部署环境注入，真实凭据不进入版本控制。

```powershell
$env:DJANGO_SECRET_KEY = 'replace-with-a-random-secret'
$env:DJANGO_ALLOWED_HOSTS = '127.0.0.1,localhost'
$env:SPARKAI_APP_ID = 'replace-with-your-app-id'
$env:SPARKAI_API_KEY = 'replace-with-your-api-key'
$env:SPARKAI_API_SECRET = 'replace-with-your-api-secret'
```

`STOPWORDS_PATH` 是可选配置。未指定时，索引构建器会查找项目内的 `data/stopwords.txt`；文件不存在时使用空停用词列表继续执行。

### 本地运行

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows:     .\.venv\Scripts\Activate.ps1

pip install django django-import-export jieba numpy scikit-learn torch transformers spark-ai-python
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

先访问 `http://127.0.0.1:8000/admin/` 导入或创建 `QandA` 记录，再进入问答页面测试检索流程。SparkAI 是可选能力；未配置凭据时，本地检索和抽取式实验仍可使用。

### 项目定位

这个仓库是一套可以运行的中文问答方法对比原型，工程重点是把“可维护的源数据—本地检索—模型适配—结构化响应—浏览器交互”完整串起来，而不是把它描述成经过临床验证的宠物医疗模型。

