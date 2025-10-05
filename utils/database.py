from langchain_community.utilities import SQLDatabase
from config.config import DB_CONNECTION_STRING

def create_sql_database():
    """
    Create a SQLDatabase object from the connection string.
    
    Returns:
        SQLDatabase: A SQLDatabase object for querying
    """
    return SQLDatabase.from_uri(DB_CONNECTION_STRING, sample_rows_in_table_info=2)