from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.db import get_connection

analyzer = SentimentIntensityAnalyzer()


conn = get_connection()
cursor = conn.cursor()

get_query = """Select * from journal_entries"""
cursor.execute(get_query)

tuple_rows = cursor.fetchall()

insert_query = """INSERT INTO entry_features (entry_id,sentiment) VALUES (%s, %s);"""

for id_value,dayone_id,date,raw_text_value,raw_json,created_at in tuple_rows:
    
    entry_id = id_value
    scores = analyzer.polarity_scores(raw_text_value)
    compound_score  = scores["compound"]
    cursor.execute(insert_query,(entry_id,compound_score))


conn.commit()
cursor.close()
conn.close()
        







