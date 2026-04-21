import mysql.connector

def connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="movies_db"
    )
    return conn, conn.cursor()


def create_db():
    conn, cur = connection()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        movie_name VARCHAR(255),
        score VARCHAR(50),
        description TEXT,
        image_url TEXT,
        critics_consensus TEXT,
        cast JSON,
        reviews JSON,
        videos JSON
    )
    """)

    conn.commit()
    conn.close()