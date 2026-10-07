# PetCare AI — Layered Chinese Pet-Care Q&A Prototype

[English](#english) · [中文](#中文)

**Tech stack:** Python · Django · SQLite · jieba · TF-IDF · cosine similarity · KNN · Transformers/PyTorch · SparkAI

## English

PetCare AI is an applied-NLP prototype that compares three answer paths for Chinese pet-care questions: deterministic retrieval from a local Q&A corpus, an experimental extractive BERT path, and optional conversational generation through SparkAI.

> This is an educational prototype, not veterinary advice or a medical diagnostic system.

### Response architecture

```text
user question
  -> jieba keyword extraction
  -> TF-IDF + cosine/KNN retrieval from QandA records
  -> optional bert-base-chinese extractive experiment
  -> optional SparkAI conversational response
  -> browser UI
```

### What I implemented

- A Django application with question-answering pages, JSON responses, and Django Admin data management.
- `QandA`, `Oridata`, and `ODIndex` models plus migrations for maintaining local source material and an inverted index.
- Chinese keyword extraction, TF-IDF vectorisation, similarity scoring, and nearest-neighbour retrieval.
- A layered interface that exposes retrieved answers, an extractive-model experiment, and an optional external-model answer separately.
- Lazy index construction from the current database so an empty project starts cleanly and reports that source data is required.
- Environment-based configuration for SparkAI, Django settings, and the optional stopword file.

### Technical accuracy

The Transformer path loads `bert-base-chinese` with `BertForQuestionAnswering`. This repository does not contain evidence of domain fine-tuning or an evaluation set, so it should be read as an exploratory extractive baseline—not as a trained veterinary QA model. Similarly, the SparkAI path is an API integration; it is not model fine-tuning.

### Configuration

Current source files do not contain live SparkAI credentials. Supply them through the environment; [`.env.example`](.env.example) lists the expected names.

```powershell
$env:DJANGO_SECRET_KEY = 'replace-with-a-random-secret'
$env:SPARKAI_APP_ID = 'replace-with-your-app-id'
$env:SPARKAI_API_KEY = 'replace-with-your-api-key'
$env:SPARKAI_API_SECRET = 'replace-with-your-api-secret'
```

`STOPWORDS_PATH` is optional. If it is not set, the index builder looks for `data/stopwords.txt` and continues with an empty stopword list when the file is absent.

### Run locally

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows:    .\.venv\Scripts\Activate.ps1
pip install django django-import-export jieba numpy scikit-learn torch transformers spark-ai-python
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/admin/` and add `QandA` records before testing retrieval. SparkAI is optional; without its credentials, the local retrieval and BERT branches remain available.

### Evidence and limitations

The repository contains the web application, migrations, a data-preparation notebook, and large CSV working files, but no held-out accuracy, safety, or latency evaluation. The BERT model is loaded per request, which is expensive; a production design would cache models, version the corpus, validate requests, add retrieval benchmarks and medical-safety messaging, and avoid committing generated datasets or runtime artefacts.

Any SparkAI or Django secrets exposed in earlier public commits must be revoked/rotated; deleting them from the current files does not erase Git history.

## 中文

PetCare AI 是一个中文宠物健康问答实验项目，用来比较三条回答路径：本地问答库的确定性检索、BERT 抽取式实验，以及可选的 SparkAI 对话生成。

> 这是教学/研究原型，不是兽医建议或医疗诊断系统。

### 系统链路

用户问题先经过 `jieba` 关键词提取，再用 TF-IDF、余弦相似度和 KNN 从 `QandA` 数据中检索；随后可以运行 `bert-base-chinese` 抽取式实验，并在配置凭据后调用 SparkAI。三类结果分别返回，便于比较，而不是混成一个无法解释的答案。

### 我的实现

- 搭建 Django 页面、JSON 响应和 Admin 数据管理；
- 设计 `QandA`、`Oridata`、`ODIndex` 模型与迁移；
- 实现中文关键词、TF-IDF、相似度和近邻检索；
- 将检索、抽取模型和外部对话模型拆成可观察的分层结果；
- 改为从当前数据库按请求建立索引，空数据库会明确提示先添加数据；
- 把 SparkAI、Django 和停用词文件配置改成环境变量，移除本机绝对路径。

### 技术边界

当前 Transformer 路径只是加载 `bert-base-chinese` 与 `BertForQuestionAnswering`，仓库没有宠物问答领域微调或评测证据，所以不能描述成“训练好的宠物 BERT 模型”。SparkAI 也是 API 集成，不是模型微调。

### 运行

按上面的命令完成迁移和管理员创建后，先在 `/admin/` 中添加 `QandA` 数据，再测试检索。SparkAI 凭据是可选的；未配置时，本地检索和 BERT 路径仍可运行。

仓库暂时没有留出集上的准确率、安全性或延迟评测；BERT 仍按请求加载，成本较高。产品化需要模型缓存、语料版本、输入校验、检索评测、医疗安全提示，以及更严格的数据和生成文件管理。

历史公开提交中出现过的 SparkAI 或 Django 密钥必须在服务端撤销/轮换；当前文件删除明文并不会清除 Git 历史。
