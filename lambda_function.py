import requests
import os
import json
import boto3
import psycopg2
from datetime import datetime
from textblob import TextBlob

my_api = os.getenv('api')
my_pass = os.getenv('rds_pass')
endpoint = os.getenv('rds_end')
aws_access = os.getenv('AWS_ACCESS_KEY')
aws_secret = os.getenv('AWS_SECRET_KEY')

def lambda_handler(event, context):
    try:
        url = f"https://newsapi.org/v2/top-headlines?apiKey={my_api}&country=us"
        response = requests.get(url)
        news = response.json().get('articles', [])

        s3 = boto3.client('s3', aws_access_key_id=aws_access, aws_secret_access_key=aws_secret)
        bucket = 'apinews-raw-data'
        times = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        s3.put_object(Bucket=bucket, Key=f'news_{times}.json', Body=json.dumps(news))
        print(f"Uploaded news to S3: news_{times}.json")

        conn = psycopg2.connect(
            host=endpoint,
            database='newsdb',
            user='techyy',
            password=my_pass
        )
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS news_articles (
            id SERIAL PRIMARY KEY,
            source_name TEXT,
            title TEXT,
            description TEXT,
            url TEXT,
            published_at TIMESTAMP,
            sentiment TEXT
        )
        """)
        conn.commit()

        success_count = 0
        for article in news:
            desc = article.get('description', '')
            sentiment = analyze_sentiment(desc)
            try:
                published_at = datetime.strptime(article.get('publishedAt'), "%Y-%m-%dT%H:%M:%SZ")
            except (ValueError, TypeError):
                published_at = None

            try:
                cur.execute(
                    "INSERT INTO news_articles (source_name, title, description, url, published_at, sentiment) VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        article.get('source', {}).get('name'),
                        article.get('title'),
                        desc,
                        article.get('url'),
                        published_at,
                        sentiment
                    )
                )
                success_count += 1
            except Exception as e:
                print(f"Failed to insert article: {article.get('title')}\nReason: {e}")

        conn.commit()
        cur.close()
        conn.close()

        print(f"Inserted {success_count}/{len(news)} articles into RDS")
        return {"status": "done"}

    except Exception as e:
        print(f"Lambda failed: {str(e)}")
        return {"status": "error", "message": str(e)}

def analyze_sentiment(text):
    blob = TextBlob(text)
    pol = blob.sentiment.polarity
    if pol > 0:
        return 'positive'
    elif pol < 0:
        return 'negative'
    else:
        return 'neutral'
