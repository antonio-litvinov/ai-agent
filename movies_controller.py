from flask import Flask, jsonify, request, abort
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def get_connection():
    try:
        connection = psycopg2.connect(
            user=os.getenv('DB_USER', ''),
            password=os.getenv('DB_PASSWORD', ''),
            host=os.getenv('DB_HOST', ''),
            port=os.getenv('DB_PORT', ''),
            database=os.getenv('DB_NAME', '')
        )
        return connection
    except psycopg2.Error as e:
        print(f"Ошибка подключения к БД: {e}")
        raise

# Получить все фильмы
@app.route('/api/movies', methods=['GET'])
def get_movies():
    # Установить соединение с базой данных
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movies")
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    # Преобразовать результаты в список словарей
    movies = []
    for row in results:
        movie = {
            "id": int(row[0]),
            "title": row[1],
            "type": row[2],
            "year": int(row[3]),
            "genre": row[4],
            "rating": float(row[5])
        }
        movies.append(movie)

    return jsonify(movies), 200

# Получить фильм по ID
@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    # Установить соединение с базой данных
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    # Если фильм не найден
    if not result:
        abort(404)

    # Преобразовать результат в словарь
    movie = {
        "id": int(result[0]),
        "title": result[1],
        "type": result[2],
        "year": int(result[3]),
        "genre": result[4],
        "rating": float(result[5])
    }

    return jsonify(movie), 200

# Добавить новый фильм
@app.route('/api/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    if not data or 'title' not in data or 'type' not in data or 'year' not in data or 'genre' not in data or 'rating' not in data:
        abort(400)

    # Установить соединение с базой данных
    connection = get_connection()
    cursor = connection.cursor()
    
    # Вставить новый фильм в базу данных
    cursor.execute(
        "INSERT INTO movies (title, type, year, genre, rating) VALUES (%s, %s, %s, %s, %s) RETURNING *",
        (data['title'], data['type'], int(data['year']), data['genre'], float(data['rating']))
    )
    result = cursor.fetchone()
    connection.commit()

    cursor.close()
    connection.close()

    # Преобразовать результат в словарь
    new_movie = {
        "id": int(result[0]),
        "title": result[1],
        "type": result[2],
        "year": int(result[3]),
        "genre": result[4],
        "rating": float(result[5])
    }

    return jsonify(new_movie), 201

# Удалить фильм по ID
@app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    # Установить соединение с базой данных
    connection = get_connection()
    cursor = connection.cursor()
    
    # Проверить, существует ли фильм
    cursor.execute("SELECT id FROM movies WHERE id = %s", (movie_id,))
    result = cursor.fetchone()
    
    if not result:
        cursor.close()
        connection.close()
        abort(404)
    
    # Удалить фильм из базы данных
    cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)