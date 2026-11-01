# Task Manager

Простое учебное веб-приложение для практики Linux и DevOps.

## Технологии

- Frontend: HTML, CSS, JavaScript
- Backend: Python + Flask
- API: REST + JSON
- База данных: SQLite
- Docker не используется

## Запуск на Ubuntu

Установите необходимые пакеты:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git curl -y
```

Перейдите в папку проекта и создайте виртуальное окружение:

```bash
cd task-manager
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Запустите приложение:

```bash
python app.py
```

Откройте в браузере Ubuntu: http://127.0.0.1:5000

Остановка сервера: `Ctrl+C`.

## API

- `GET /api/tasks` — получить все задачи
- `POST /api/tasks` — создать задачу. JSON: `{"title":"Моя задача","description":"Описание"}`
- `PATCH /api/tasks/<id>` — изменить статус. JSON: `{"completed":true}`
- `DELETE /api/tasks/<id>` — удалить задачу

База `tasks.db` создаётся автоматически рядом с `app.py`.

## Важно

Это учебный вариант. Flask запускается с `debug=True` и привязан к `127.0.0.1`.
Перед размещением в сети нужно отключить debug-режим и настроить production-сервер,
например Gunicorn за Nginx, а также автозапуск через systemd.
