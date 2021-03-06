## Scrape reddit WSB and add to SQLite database

from psaw import PushshiftAPI
import config
import datetime
import sqlite3

connection = sqlite3.connect()
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT * FROM stock
""")

rows = cursor.fetchall()

stocks = {}
for row in rows: 
    stocks['$' + row['symbol']] = row['id']

api = PushshiftAPI()

start_time = int(datetime.datetime(2020, 9, 30).timestamp())

submissions = api.search_submissions(
                                     after=start_time,
                                     subreddit='wallstreetbets',
                                     filter=['url','author', 'title', 'subreddit'])
                                     
for submission in submissions:
    words = submission.title.split()
    cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))

    if len(cashtags) > 0:
        for cashtag in cashtags:
            if cashtag in stocks:
                submitted_time = datetime.datetime.fromtimestamp(submission.created_utc).isoformat()

                try:
                    cursor.execute("""
                        INSERT INTO mention (dt, stock_id, stock_symb, message, source, url)
                        VALUES (?, ?, ?, ?, 'wallstreetbets', ?)
                    """, (submitted_time, stocks[cashtag], cashtag.split('$')[1], submission.title, submission.url))

                    connection.commit()
                except Exception as e:
                    print(e)
                    connection.rollback()
