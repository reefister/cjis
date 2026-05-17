import json 
import psycopg2
from datetime import datetime

with open('Reverie.json','r', encoding='utf-8') as file:
    data = json.load(file)                             


entries = data['entries']                            

conn = psycopg2.connect(                              
    host="localhost",                                      
    database="cjis",
    user="postgres",
    password="CJIS",
    port="5432"
)
cursor = conn.cursor()                                      

insert_query = """
INSERT INTO journal_entries (dayone_id, date, raw_text, raw_json)
VALUES (%s, %s, %s, %s)
ON CONFLICT (dayone_id) DO NOTHING;
"""


for entry in entries:
    text = entry.get('text')
    uuid = entry.get('uuid')
    creation_date_str = entry.get('creationDate')
    raw_json = entry

    if not text or not uuid or not creation_date_str:
        continue

    creation_date = datetime.fromisoformat(creation_date_str.replace("Z", "+00:00"))


    cursor.execute(
    insert_query,
    (
        uuid,
        creation_date,
        text,
        json.dumps(raw_json)
    )
    )
                              
conn.commit()                          
cursor.close()
conn.close()


