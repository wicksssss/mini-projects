# BeautyShop 💄

Навчальний онлайн-магазин косметики розроблений на Python + Django.

## Технологічний стек

- Python 3.9
- Django 4.2
- SQLite (розробка)
- Pillow
- python-decouple

## Встановлення та запуск

### 1. Клонувати репозиторій

git clone https://github.com/wicksssss/mini-projects.git
cd mini-projects

### 2. Створити virtualenv та активувати

python3 -m venv venv
source venv/bin/activate

### 3. Встановити залежності

pip install -r requirements.txt

### 4. Створити файл .env

Створи файл .env у корені проєкту:

SECRET_KEY=*****
DEBUG=True

### 5. Застосувати міграції

python manage.py migrate

### 6. Завантажити тестові дані

python manage.py loaddata products/fixtures/products.json

### 7. Створити суперкористувача

python manage.py createsuperuser

### 8. Запустити сервер

python manage.py runserver

Відкрий браузер: http://127.0.0.1:8000
Адмінка: http://127.0.0.1:8000/admin

## Запуск тестів

python manage.py test products

## Структура проєкту

- products/ — каталог товарів, моделі Category, Brand, Product
- orders/ — замовлення, моделі Order, OrderItem
- accounts/ — профілі користувачів, модель UserProfile
- cart/ — логіка кошика

## Розробники

- Вікторія Качмар — моделі, БД, адмінка, views
- Олександр Анциферов — views кошика, авторизація