# trsp_kr2

Небольшое учебное API на **FastAPI** (точка входа: `app.py`).

## Требования

- Python 3.10+ (рекомендуется)
- pip

## Установка

### 1) Клонировать репозиторий
```bash
git clone https://github.com/pkpal-uhobp/trsp_kr2.git
cd trsp_kr2
```

### 2) Создать и активировать виртуаль��ое окружение
**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3) Установить зависимости
```bash
pip install -r requirements.txt
```

## Запуск

Запуск через `uvicorn`:

```bash
uvicorn app:app --reload
```

После запуска сервер будет доступен по адресу:
- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Основные эндпоинты

- `POST /create_user` — принимает данные пользователя и возвращает их (заготовка).
- `GET /products/search?keyword=...&limit=10&category=...` — поиск по мок‑каталогу продуктов.
- `GET /product/{product_id}` — получить продукт по id (из мок‑данных).
- `POST /login` — логин, устанавливает cookie `session_token` (срок жизни ~5 минут).
- `GET /profile` — профиль текущего пользователя (требует авторизацию через cookie).
- `GET /headers` — возвращает выбранные заголовки запроса (`User-Agent`, `Accept-Language`).
- `GET /info` — возвращает сообщение и заголовки + добавляет ответный заголовок `X-Server-Time`.
