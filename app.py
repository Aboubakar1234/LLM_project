from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def get_articles_from_db():
    """ Récupère les articles de la base de données PostgreSQL """
    try:
        conn = psycopg2.connect(
            dbname="articles_ml_S8;",
            user="postgres",
            password="Nourra2005",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT url, article_title, media_name, author, description, publication_date, media_logo FROM articles")
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return articles
    except Exception as e:
        print("Failed to fetch articles from database:", e)
        return []


@app.route('/')
def index():
    articles = get_articles_from_db()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
