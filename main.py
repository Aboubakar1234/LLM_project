import requests
from bs4 import BeautifulSoup, NavigableString
from datetime import datetime
import psycopg2




media_type_pqn = "Presse Quotidienne Nationale"
medias_pqn = [{"media_name":"BFMTV",
               "media_rss_feed_url" : "https://www.bfmtv.com/rss/sante/", "media_logo":"https://upload.wikimedia.org/wikipedia/commons/4/45/Logo_BFMTV_2019.svg"},
               {"media_name":"Le Monde",
"media_rss_feed_url" : "https://www.lemonde.fr/international/rss_full.xml", "media_logo":"https://logosandtypes.com/wp-content/uploads/2020/12/Le-Monde.png"},
{"media_name":"Le Figaro",
"media_rss_feed_url" : "https://www.lefigaro.fr/rss/figaro_actualites.xml","media_logo":"https://play-lh.googleusercontent.com/E5MMJKReOuAj4XmcqOZUWQF103SH8ynV7F8NvzyFJtmZSqtI3Oj2PSlr6lv0mcrZ4Q"},
{"media_name":"20 Minutes",
"media_rss_feed_url" : "https://partner-feeds.20min.ch/rss/20minutes", "media_logo":"https://store-images.microsoft.com/image/apps.38947.13510798885263626.9ba47a8c-d1b0-43f9-9212-ae83c58ca9fd.5698e5aa-5eaf-40c2-892f-55c5feededef"},
{"media_name":"Les Echos",
"media_rss_feed_url" : "https://services.lesechos.fr/rss/les-echos-politique.xml", "media_logo":"https://play-lh.googleusercontent.com/FEzHLFKfB1rPt9zfoZxy_CYNXmej7G1i7udE3Bge7V636sd_PoBHWSiMrl1h_i3tsUPO"},
{"media_name":"Ouest France",
"media_rss_feed_url" : "https://www.ouest-france.fr/rss/une","media_logo":"https://laplace.ouest-france.fr/wp-content/uploads/favicon-OF-512x512.png" },
{"media_name":"Libération",
"media_rss_feed_url" : "https://www.liberation.fr/arc/outboundfeeds/rss-all/?outputType=xml", "media_logo":"https://cdn.worldvectorlogo.com/logos/liberation.svg"},
{"media_name":"Le Parisien",
"media_rss_feed_url" : "https://feeds.leparisien.fr/leparisien/rss","media_logo":"https://i.pinimg.com/originals/de/f1/47/def147a27d81983973832afc81062682.jpg"},
{"media_name":"La Croix",
"media_rss_feed_url" : "https://www.la-croix.com/RSS/UNIVERS", "media_logo":"https://pbs.twimg.com/profile_images/689352370128588800/3VfuYJV9_400x400.png"}]


# Insert les articles dans la base de données
def insert_article_to_db(article):
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(
            dbname="articles_ml_S8;",
            user="postgres",
            password="Nourra2005",
            host="localhost",
            port="5432"
        )

        # Create a cursor object
        cursor = conn.cursor()

        # Prepare SQL query to insert data into the table
        sql = """INSERT INTO articles (url, article_title, media_name, media_type, author, description, content, publication_date, publication_hour, media_logo)
        VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s )
        """


        # Insert data into the table
        cursor.execute(sql, (
            article['url'],
            article['article_title'],
            article['media_name'],
            article['media_type'],
            article['author'],
            article['description'],
            article['content'],
            article['publication_date'],
            article['publication_hour'],
            article['media_logo']
        ))

        # Commit the transaction
        conn.commit()
        print("Article inserted successfully")

    except psycopg2.IntegrityError as e:
        if 'unique constraint' in str(e).lower():
            print(f"Duplicate article not inserted: {article['url']}")
        else:
            print("Error inserting article due to integrity error:", e)
    except Exception as e:
        print("General error inserting article:", e)
    finally:
        # Ensure that the cursor and connection are closed properly
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Fetch l'url du flux rss
def fetch_rss_feed(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch RSS feed with status code: {response.status_code}")


# Nettoie le texte des balises html
def clean_html_content(html_content):
    if(html_content):
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the text from the parsed HTML
        clean_text = soup.get_text()

        return clean_text
    return html_content


# Reformatte la date de l'article au format "%Y-%m-%d %H:%M:%S"
def parse_date(date_string):
    if "GMT" in date_string:
        date_string = date_string.replace("GMT", "+0000")

    # Define the date format including the timezone
    date_format = "%a, %d %b %Y %H:%M:%S %z"

    # Parse the date string into a datetime object
    dt = datetime.strptime(date_string, date_format)

    # Extract the date and time in the desired formats
    publication_date = dt.strftime("%Y-%m-%d")
    publication_hour = dt.strftime("%H:%M:%S")

    return publication_date, publication_hour

# Scrap!p!!e les données en fonction des différentes balises html dans lesquelles elles sont
def parse_rss_feed(media_name, media_type, media_logo, xml_content):
    soup = BeautifulSoup(xml_content, features="xml")
    items = soup.find_all('item')
    rss_data = []
    for item in items:
        title = item.find('title').text if item.find('title') else None
        link = item.find('link').text if item.find('link') else None
        pub_date = item.find('pubDate').text if item.find('pubDate') else None
        description = item.find('description').text if item.find('description') else None
        author = item.find('dc:creator')  # Chercher la balise <dc:creator>
        if author and isinstance(author, NavigableString):
            author = author.text
        elif author:
            author = author.text.strip()
        else:
            author = None

        if(pub_date):
            publication_date, publication_hour = parse_date(pub_date)
        else:
            publication_date, publication_hour = None, None

        rss_data.append({
            'article_title': clean_html_content(title),
            'url': link,
            'publication_date': publication_date,
            'publication_hour': publication_hour,
            'author': author,
            'description': clean_html_content(description),
            'content': None,
            'media_name': media_name,
            'media_type': media_type,
            'media_logo': media_logo
        })
    return rss_data


for media in medias_pqn:
    # Access each dictionary's keys
    media_name = media["media_name"]
    media_type = media_type_pqn
    media_logo = media["media_logo"]
    media_rss_feed_url = media["media_rss_feed_url"]
    rss_feed_content = fetch_rss_feed(media_rss_feed_url)
    rss_data = parse_rss_feed(media_name, media_type, media_logo, rss_feed_content)
    print("Scraping for "+media_name+"...")
    for article in rss_data:
        insert_article_to_db(article)


