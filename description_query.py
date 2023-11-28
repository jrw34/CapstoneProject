import pandas as pd
import os
from sqlalchemy import create_engine, text

def description_query_db(search_str):
    
    DB_URL = os.environ['DB_URL'].replace('postgres','postgresql')
    
    engine = create_engine(DB_URL)
    
    params = {'search_str': search_str}
    
    query = text("""
            
            SELECT *
            FROM parsed
            WHERE description ~* :search_str --regex 
    """)
    
    with engine.connect() as conn:
        results = conn.execute(query, params).fetchall()
        
    return pd.DataFrame(results)


def web_app_desc_query(search_str):
    
    DB_URL = st.secrets["DB_URL"]
    
    engine = create_engine(DB_URL)
    
    params = {'search_str': search_str}
    
    query = text("""
            
            SELECT *
            FROM parsed
            WHERE description ~* :search_str --regex 
    """)
    
    with engine.connect() as conn:
        results = conn.execute(query, params).fetchall()
        
    return pd.DataFrame(results)