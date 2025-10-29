## 项目说明

这是一个基于 Django 的小型网站项目（项目名：`petcare`），包含基础页面、静态资源、媒体上传目录与一个应用 `cwyl`。可用于本地运行、开发与部署到服务器或容器环境。本文档帮助你在本地快速启动并推送到 GitHub。

## 环境要求

- Python 3.9+（推荐 3.10/3.11）
- pip / venv（或 conda）
- Git（用于推送到 GitHub）
- 操作系统：Windows 10/11（示例命令使用 PowerShell）

## 目录结构

```text
petcare/
├─ manage.py
├─ db.sqlite3
├─ 1/                       # 一些 CSV 数据示例
├─ cwyl/                    # 业务应用（models、views、urls 等）
├─ media/uploads/           # 媒体上传目录
├─ static/                  # 静态资源（CSS/JS/Images）
├─ templates/               # 模板页（index/questionAnswering/wqq 等）
└─ petcare/                 # 项目配置（settings/urls/asgi/wsgi）
```

## 快速开始（本地开发）

以下以 PowerShell 为例，在项目根目录 `petcare` 下执行：

```powershell
# 1) 创建与激活虚拟环境（可选但强烈推荐）
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) 安装依赖（若无 requirements.txt，可先安装 Django）
pip install --upgrade pip
pip install django
```

如果后续使用了额外库（如 pandas、django-import-export 等），请根据需要安装：

```powershell
pip install pandas django-import-export
```

### 初始化数据库

```powershell
python manage.py migrate
```

### 创建超级用户（可登录 /admin/）

```powershell
python manage.py createsuperuser
```

### 运行开发服务器

```powershell
python manage.py runserver
```

启动成功后访问：

- 主页（如已路由）：`http://127.0.0.1:8000/`
- 管理后台：`http://127.0.0.1:8000/admin/`
- 其他模板页（如配置了路由）：`/questionAnswering/`、`/wqq/`

> 注：实际可访问路径以 `petcare/urls.py` 与 `cwyl/urls.py` 中的路由为准。

## 静态与媒体文件

- 开发环境下，Django 会直接从 `static/` 提供静态资源。
- 上传文件默认位于 `media/uploads/`，可在 `petcare/settings.py` 调整 `MEDIA_ROOT` 与 `MEDIA_URL`。
- 生产环境建议使用 `collectstatic` 收集静态文件并交由 Web 服务器（Nginx 等）托管：

```powershell
python manage.py collectstatic
```

## 推送到 GitHub

1) 在 GitHub 创建一个空仓库（例如：`yourname/petcare`）。

2) 在项目根目录执行：

```powershell
git init
git add .
git commit -m "chore: initial commit"
git branch -M main
git remote add origin https://github.com/yourname/petcare.git
git push -u origin main
```

> 建议添加合适的 `.gitignore` 防止将虚拟环境、编译产物等推送到仓库。示例内容：

```gitignore
# Python
__pycache__/
*.py[cod]
*.sqlite3
.venv/

# Django
staticfiles/
media/

# IDE/OS
.vscode/
.idea/
*.log
```

## 常见问题（FAQ）

- 数据库锁或权限问题（Windows）：若出现 SQLite 被占用，先关闭运行中的服务或编辑器占用进程，再重试 `migrate`/`runserver`。
- 静态资源不生效：确认模板中引用了正确的 `{% load static %}`，并使用 `{% static 'path/to/file' %}`。生产环境需完成 `collectstatic` 并正确配置静态目录。
- 中文路径/编码：本项目路径包含中文，确保终端编码为 UTF-8（PowerShell 可执行 `chcp 65001`），或将项目移至无中文路径位置。

## 许可证

未指定许可证。若需开源，建议添加 `LICENSE` 文件（如 MIT/Apache-2.0）。

## 贡献

欢迎提交 Issue 或 PR 改进代码与文档。提交前请确保：

- 代码可运行、通过基本检查
- 变更点简要说明（Commit message 清晰）
- 如涉及依赖变化，请同步更新文档


