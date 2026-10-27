import random

import psycopg

# Вкажіть ваш актуальний пароль замість "ваш_пароль"
DSN = "postgresql://postgres:postgress@localhost:5432/postgres"

# Списки для генерації реалістичних даних
FIRST_NAMES = ["Олександр", "Андрій", "Максим", "Дмитро", "Артем", "Іван", "Михайло", "Олена", "Марія", "Анна", "Вікторія", "Юлія", "Оксана", "Наталія"]
LAST_NAMES = ["Коваленко", "Бондаренко", "Ткаченко", "Кравченко", "Ковальчук", "Шевченко", "Бойко", "Марченко", "Мельник", "Мороз", "Лисенко", "Петренко"]

def generate_resident_data(index: int):
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    full_name = f"{first} {last}"
    # Форматування під вимоги regex (+380 та 9 цифр)
    phone = f"+38067{random.randint(1000000, 9999999)}"
    email = f"user{index}@osbb.ua"
    return full_name, phone, email

def init_database():
    with psycopg.connect(DSN) as conn:
        conn.execute("DROP TABLE IF EXISTS residents;")
        conn.execute("DROP TABLE IF EXISTS apartments;")

        # Створення таблиці Квартир
        conn.execute("""
            CREATE TABLE apartments (
                id SERIAL PRIMARY KEY,
                number INTEGER NOT NULL,
                floor INTEGER NOT NULL
            )
        """)
        
        # Створення таблиці Жителів (зв'язок 1:N)
        conn.execute("""
            CREATE TABLE residents (
                id SERIAL PRIMARY KEY,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                apartment_id INTEGER REFERENCES apartments(id)
            )
        """)

        # Створення 15 квартир
        for i in range(1, 16):
            conn.execute(
                "INSERT INTO apartments (number, floor) VALUES (%s, %s)", 
                (i, (i // 4) + 1)
            )

        # Генерація 50 жителів з реалістичними даними
        for i in range(1, 51):
            full_name, phone, email = generate_resident_data(i)
            apt_id = random.randint(1, 15)  # Випадкове розселення по 15 квартирах
            
            conn.execute(
                "INSERT INTO residents (full_name, phone, email, apartment_id) VALUES (%s, %s, %s, %s)", 
                (full_name, phone, email, apt_id)
            )
            
        print("Базу даних переініціалізовано. Створено 15 квартир та 50 реалістичних жителів!")

if __name__ == "__main__":
    init_database()