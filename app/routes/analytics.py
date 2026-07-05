from fastapi import APIRouter
from app.db import get_connection

analytics_sentiment_router = APIRouter()

@analytics_sentiment_router.get("/analytics/sentiment")
def sentiment_analytics(word):
    conn = get_connection()
    cursor = conn.cursor()
    get_query = """SELECT j.raw_text, e.sentiment,j.date FROM  entry_features e join journal_entries j on e.entry_id = j.id, jsonb_array_elements_text(e.concepts) AS concept"""
    params = []
    if word is not None:
       pattern = "%"+ word +"%"
       params.append(pattern)
       get_query += " where concept ilike %s ORDER BY j.date ASC "         
        
    cursor.execute(get_query,tuple(params))
    tuple_rows = cursor.fetchall()

    retrieved_list = []
    for raw_text_value,sentiment,date in tuple_rows:
        dict_row = {}
        dict_row["raw_text"] = raw_text_value
        dict_row["sentiment"] = sentiment
        dict_row["date"] = date
        retrieved_list.append(dict_row)

    cursor.close()
    conn.close()
    return retrieved_list



