#from flask import Flask, render_template, request, jsonify
#import sqlite3
#
#app = Flask(__name__)
#DATABASE = 'example.db'
#
#
## Функция для подключения к базе данных
#def get_db_connection():
#    conn = sqlite3.connect(DATABASE)
#    conn.row_factory = sqlite3.Row
#    return conn
#
#
## Инициализация базы данных
#def init_db():
#    conn = get_db_connection()
#    cursor = conn.cursor()
#    cursor.execute('''
#        CREATE TABLE IF NOT EXISTS form_data (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            field_1 TEXT NOT NULL,
#            field_2 TEXT NOT NULL,
#            field_3 TEXT NOT NULL
#        )
#    ''')
#    conn.commit()
#    conn.close()
#
#
## Главная страница с формой
#@app.route('/')
#def index():
#    conn = get_db_connection()
#    cursor = conn.cursor()
#    cursor.execute("SELECT * FROM form_data")
#    rows = cursor.fetchall()
#    conn.close()
#
#    # Передаем данные из базы в HTML-шаблон
#    return render_template('index.html', form_data=rows)
#
#
## Сохранение данных формы
#@app.route('/save-form-data', methods=['POST'])
#def save_form_data():
#    data = request.get_json()
#
#    if not isinstance(data, list):
#        return jsonify({"error": "Invalid data format. Expected a list."}), 400
#
#    conn = get_db_connection()
#    cursor = conn.cursor()
#
#    try:
#        # Удаляем записи, которых нет в данных
#        incoming_ids = [row["id"] for row in data if "id" in row]
#        if incoming_ids:
#            cursor.execute(f"DELETE FROM form_data WHERE id NOT IN ({','.join(['?']*len(incoming_ids))})", incoming_ids)
#        else:
#            cursor.execute("DELETE FROM form_data")  # Удалить все, если данные пустые
#
#        for row in data:
#            if "id" in row:
#                # Обновляем существующую запись
#                cursor.execute('''
#                    UPDATE form_data
#                    SET field_1 = ?, field_2 = ?, field_3 = ?
#                    WHERE id = ?
#                ''', (row["field_1"], row["field_2"], row["field_3"], row["id"]))
#            else:
#                # Добавляем новую запись
#                cursor.execute('''
#                    INSERT INTO form_data (field_1, field_2, field_3)
#                    VALUES (?, ?, ?)
#                ''', (row["field_1"], row["field_2"], row["field_3"]))
#
#        conn.commit()
#        return jsonify({"message": "Form data saved successfully!"}), 200
#
#    except Exception as e:
#        conn.rollback()
#        return jsonify({"error": str(e)}), 500
#
#    finally:
#        conn.close()
#
#
#if __name__ == '__main__':
#    init_db()
#    app.run(debug=True)
#

from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS form_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_1 TEXT,
            field_2 TEXT,
            field_3 TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Сохранение данных в базу
@app.route('/save-form-data', methods=['POST'])
def save_form_data():
    data = request.get_json()

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    try:
        for i in range(len(data.get('field_1', []))):
            field_1 = data['field_1'][i]
            field_2 = data['field_2'][i] if i < len(data['field_2']) else None
            field_3 = data['field_3'][i] if i < len(data['field_3']) else None
            row_id = data['ids'][i]

            if row_id and row_id != "new":
                cursor.execute("""
                    UPDATE form_data
                    SET field_1 = ?, field_2 = ?, field_3 = ?
                    WHERE id = ?
                """, (field_1, field_2, field_3, row_id))
            else:
                cursor.execute("""
                    INSERT INTO form_data (field_1, field_2, field_3)
                    VALUES (?, ?, ?)
                """, (field_1, field_2, field_3))

        conn.commit()
        return jsonify({"message": "Form data saved successfully!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        
@app.route('/delete-row', methods=['POST'])
def delete_row():
    data = request.get_json()
    row_id = data.get('id')

    if not row_id:
        return jsonify({"error": "Row ID is required"}), 400

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM form_data WHERE id = ?", (row_id,))
        conn.commit()
        return jsonify({"message": "Row deleted successfully!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# Получение данных из базы и отображение формы
@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Получаем данные из базы данных
    cursor.execute("SELECT id, field_1, field_2, field_3 FROM form_data")
    rows = cursor.fetchall()

    # Преобразуем данные в удобный формат для отправки в шаблон
    form_data = [
        {"id": row[0], "field_1": row[1], "field_2": row[2], "field_3": row[3]}
        for row in rows
    ]

    conn.close()

    print(form_data)

    return render_template('index.html', form_data=form_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
