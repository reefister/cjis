from app.db import get_connection
import cohere
import os
from dotenv import load_dotenv

load_dotenv()
co = cohere.ClientV2(api_key=os.environ.get("COHERE_API_KEY"))

conn = get_connection()
cursor = conn.cursor()

get_query = """Select e.entry_id,j.raw_text from journal_entries j left join entry_features e on j.id = e.entry_id where e.embeddings is NULL"""
cursor.execute(get_query)

tuple_rows = cursor.fetchall()

insert_query = """UPDATE entry_features SET embeddings = %s where entry_id = %s;"""

batch_size = 96
processed = 0
batch_ids = []
batch_texts = []

for entry_id_value,raw_text_value in tuple_rows:
    
    entry_id = entry_id_value
    raw_text = raw_text_value

    batch_ids.append(entry_id)
    batch_texts.append(raw_text)

    if len(batch_ids) == batch_size:
    
        response = co.embed(
        texts=batch_texts,
        model="embed-english-v3.0",
        input_type="search_document",
        embedding_types=["float"]
        )
        embeddings = response.embeddings.float
        for eid, emb in zip(batch_ids, embeddings):
            cursor.execute(insert_query, (emb, eid))
        conn.commit()
        processed += batch_size
        print(f"Processed {processed} entries")
        batch_ids,batch_texts = [],[]

if len(batch_ids) > 0:
    response = co.embed(
    texts=batch_texts,
    model="embed-english-v3.0",
    input_type="search_document",
    embedding_types=["float"]
    )
    embeddings = response.embeddings.float
    for eid, emb in zip(batch_ids, embeddings):
        cursor.execute(insert_query, (emb, eid))
    conn.commit()
    batch_ids,batch_texts = [],[]    

cursor.close()
conn.close()
        







