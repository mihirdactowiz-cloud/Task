from log import get_all_movie_urls
from parsers import process
from db import connection, create_db
import json

create_db()

urls = get_all_movie_urls(
    "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:newest"
)

conn, cur = connection()

for url in urls:
    try:
        data = process(url)

        if not data:
            continue

        cur.execute("""
        INSERT INTO movies (
            movie_name, score, description, image_url,
            critics_consensus, cast, reviews, videos
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data.get("movie_name"),
            data.get("score"),
            data.get("description"),
            data.get("image_url"),
            data.get("critics_consensus"),
            json.dumps(data.get("cast", [])),
            json.dumps(data.get("reviews", [])),
            json.dumps(data.get("videos", []))
        ))

        print(f"Inserted: {data.get('movie_name')}")

    except Exception as e:
        print("Error:", url, e)

conn.commit()
conn.close()

print("ALL DONE ✅")