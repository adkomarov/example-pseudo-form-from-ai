import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('flaskapp\example.db')
cursor = conn.cursor()

# Выполнение запроса для проверки данных
cursor.execute("SELECT * FROM form_data")
rows = cursor.fetchall()

# Вывод данных
for row in rows:
    print(row)

# Закрытие соединения
conn.close()