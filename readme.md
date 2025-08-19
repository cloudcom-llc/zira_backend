# Zirafest Payment Backend

Django backend для обработки платежей билетов на Zirafest через OCTO Bank.

## Быстрый старт

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте .env файл:
```bash
cp .env.example .env
```

4. Сгенерируйте SECRET_KEY и добавьте в .env:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

5. Выполните миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустите сервер:
```bash
python manage.py runserver
```

## API Endpoints

- `POST /api/payment/uzs/` - Оплата в сумах (Humo/Uzcard)
- `POST /api/payment/usd/` - Оплата в долларах (Bank Card)  
- `GET /api/payment/status/<id>/` - Проверка статуса
- `POST /api/payment/notify/` - Webhook от OCTO
- `/admin/` - Админ панель

## Тарифы

- Standard: 2,000,000 UZS
- Gold: 3,000,000 UZS  
- Platinum: 10,000,000 UZS

## Структура проекта

```
zirafest_backend/
├── manage.py
├── requirements.txt
├── .env
├── README.md
├── zirafest/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── payments/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── admin.py
│   ├── serializers.py
│   ├── services.py
│   ├── views.py
│   └── urls.py
└── templates/
    └── payment_success.html
```