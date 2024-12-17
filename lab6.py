from flask import Flask
import sqlite3

app = Flask(__name__)

def get_cars():
    """
    Получение списка машин из базы sqlite
    """
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute("SELECT make, model, year, price FROM cars")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/create_db', methods=['GET'])
def create_db():
    """
    Добавление списка машин в базу sqlite
    """
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS cars')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            price REAL NOT NULL,
            year TEXT NOT NULL
        );
    ''')
    data = [
        ("Toyota", "Camry", 2018, 1500000.00),
        ("Honda", "Civic", 2020, 1800000.00),
        ("Ford", "Focus", 2017, 1200000.00),
        ("Volkswagen", "Passat", 2019, 1700000.00),
        ("BMW", "3 Series", 2016, 2000000.00),
        ("Mercedes-Benz", "C-Class", 2018, 2200000.00),
        ("Audi", "A4", 2019, 2500000.00),
        ("Hyundai", "Elantra", 2021, 1900000.00),
        ("Kia", "Optima", 2020, 1600000.00),
        ("Chevrolet", "Cruze", 2016, 1000000.00),
    ]
    cursor.executemany("INSERT INTO cars (make, model, year, price) VALUES (?, ?, ?, ?)", data)
    conn.commit()
    conn.close()
    return 'Данные машин успешно записаны в БД'

@app.route('/', methods=['GET'])
def index():
    cars = get_cars()
    html = """
    <html>
    <head><title>Список машин</title></head>
    <body>
    <h1>Список машин</h1>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Марка</th>
            <th>Модель</th>
            <th>Год выпуска</th>
            <th>Цена</th>
        </tr>
    """

    for car in cars:
        make, model, year, price = car
        html += f"<tr><td>{make}</td><td>{model}</td><td>{year}</td><td>{price}</td></tr>"

    html += """
    </table>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(port=2080)
