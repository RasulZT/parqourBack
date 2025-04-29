# 🚦 Parqour Support System

Интеллектуальная система поддержки тикетов с интеграцией Telegram, Asana и WebSocket, построенная на Django, Celery и Docker.

---

## 📌 Возможности

- 📬 Приём тикетов от пользователей через Telegram-бота
- 🔄 Синхронизация с задачами Asana (статусы, секции, завершённость)
- 📡 WebSocket-уведомления об изменениях тикетов (создание, обновление, удаление)
- 📊 Панель администратора Django с фильтрацией и управлением
- 🔔 Уведомления в Telegram-группы поддержки
- ⏱ Периодическая проверка статусов тикетов через Celery Beat
- 📦 Полностью контейнеризировано (Docker + Docker Compose)

---

## 🛠 Стек технологий

- **Backend:** Django 4.x, Django REST Framework, Django Channels
- **WebSockets:** Channels + Redis
- **Очереди:** Celery + RabbitMQ
- **Планировщик:** Celery Beat
- **Интеграции:** Telegram Bot API, Asana API
- **DevOps:** Docker, Docker Compose, NGINX (с поддержкой WebSocket), Certbot (HTTPS)

---

## 🚀 Быстрый старт (Docker Compose)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/your-org/parqour-support.git
cd parqour-support
