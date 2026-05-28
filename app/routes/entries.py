from fastapi import APIRouter
from app.db import get_connection

entries_router = APIRouter()

@entries_router.get("/entries")
def get_entries(limit=10,offset=0,start_date=None,end_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    get_query = """
    Select id, dayone_id, date, raw_text from journal_entries 
    """
    conditions = []
    params = []
    if start_date is not None:
        conditions.append("date >= %s")
        params.append(start_date)
    if end_date is not None:
        conditions.append("date <= %s")
        params.append(end_date)
    if len(conditions)>=1:
        get_query += " Where "+" AND ".join(conditions)
    get_query += " ORDER BY date DESC LIMIT %s OFFSET %s"
    params.append(limit)
    params.append(offset)
    cursor.execute(get_query,(tuple(params)))
    tuple_rows = cursor.fetchall()
    
    entries_list = []
    for id_value,dayone_id_value,date_value,raw_text_value in tuple_rows:
        dict_row = {}
        dict_row["id"] = id_value
        dict_row["dayone_id"] = dayone_id_value
        dict_row["date"] = date_value
        dict_row["raw_text"] = raw_text_value
        entries_list.append(dict_row)
    
    cursor.close()
    conn.close()
    return entries_list
