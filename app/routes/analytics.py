from fastapi import APIRouter
from app.db import get_connection

analytics_sentiment_router = APIRouter()
analytics_concept_frequency_router = APIRouter()
analytics_concept_coocurrence_router = APIRouter()

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

@analytics_concept_frequency_router.get("/analytics/concept/frequency")
def concept_frequency():
    conn = get_connection()
    cursor = conn.cursor()
    get_query = """ SELECT lower(concept),count(*) as total_count FROM entry_features e join journal_entries j on e.entry_id = j.id,jsonb_array_elements_text(e.concepts) AS concept GROUP BY lower(concept) ORDER BY total_count desc"""

    cursor.execute(get_query)
    tuple_rows = cursor.fetchall()

    retrieved_list = []
    for concept,count in tuple_rows:
        dict_row = {}
        dict_row['concept'] = concept
        dict_row['count'] = count
        retrieved_list.append(dict_row)

    cursor.close()
    conn.close()
    return retrieved_list

@analytics_concept_coocurrence_router.get("/analytics/concept/cooccurence")
def concept_coocurrence(word):
    conn = get_connection()
    cursor = conn.cursor()
    get_query = """with matched_entries as (
SELECT 
	e.*,j.*
FROM 
    entry_features e join journal_entries j on e.entry_id = j.id,
	jsonb_array_elements_text(e.concepts) AS concept
WHERE 
	concept ilike %s
)

select lower(concept),count(*) as co_occurence_count
from matched_entries m,jsonb_array_elements_text(m.concepts) AS concept

where lower(concept) != %s
group by lower(concept)
order by co_occurence_count desc"""
    params = []
    
    params.append(word)
    params.append(word.lower())

    cursor.execute(get_query,tuple(params))
    tuple_rows = cursor.fetchall()
    
    retrieved_list = []
    for concept,count in tuple_rows:
        dict_row = {}
        dict_row['concept'] = concept
        dict_row['count'] = count
        retrieved_list.append(dict_row)
    
    cursor.close()
    conn.close()
    return retrieved_list



