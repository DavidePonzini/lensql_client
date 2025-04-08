import os
from typing import Iterator
import pandas as pd
import psycopg2
from psycopg2.extensions import cursor, connection
from dav_tools import messages
from sql_errors import SQLException
from sql_code import SQLCode

HOST        =       os.getenv('DB_HOST')
PORT        =   int(os.getenv('DB_PORT'))

DBNAME = None
USERNAME = None
PASSWORD = None

CONNECTION: connection = None

def are_credentials_set():
    '''Checks if all database credentials are set.'''

    for cred in (HOST, PORT, DBNAME, USERNAME, PASSWORD):
        if cred is None:
            return False
    return True

def get_cursor() -> cursor:
    '''Returns the current database connection.'''

    if CONNECTION is None:
        raise Exception('Database connection is not set')
    
    return CONNECTION.cursor()

def connect(dbname: str, username: str, password: str) -> bool:
    '''Sets the database credentials and tests the connection.'''
    
    global CONNECTION, DBNAME, USERNAME, PASSWORD
    
    if CONNECTION is not None:
        CONNECTION.close()
        CONNECTION = None
    
    DBNAME = dbname
    USERNAME = username
    PASSWORD = password

    if not are_credentials_set():
        raise Exception('Database credentials not set')
    
    try:
        CONNECTION = psycopg2.connect(
            host=HOST,
            port=PORT,
            dbname=DBNAME,
            user=USERNAME,
            password=PASSWORD
        )

        return True
    except Exception as e:
        messages.error('Error connecting to the database:', e)
        return False
    

def execute_query(query_str: str) -> Iterator[pd.DataFrame | str | SQLException]:
    '''
    Executes a query on the database and returns the result as a DataFrame.
    - If the query is a SELECT statement, the result will be a DataFrame.
    - If the query is an INSERT, UPDATE, or DELETE statement, the result ...
    - If the query fails, an SQLException will be returned.

    Parameters:
        query (str): The SQL query to execute.

    Returns:
        pd.DataFrame | str | SQLException: The result of the query.
    '''

    for statement in SQLCode(query_str).strip_comments().split():
        try:
            cur = get_cursor()

            cur.execute(statement.query)
            # conn.commit()
                
            if cur.description:  # Check if the query has a result set
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                result = pd.DataFrame(rows, columns=columns)
                
                yield result
            else:  # No result set, return the number of affected rows
                if cur.rowcount < 0:
                    yield f'{statement.first_token}'
                else:
                    yield f'{statement.first_token} {cur.rowcount}'
        except Exception as e:
            yield SQLException(e)
        finally:
            cur.close()
            # conn.close()


def list_users() -> pd.DataFrame:
    '''Lists all users in the database.'''

    cur = get_cursor()

    cur.execute(Queries.LIST_USERS)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    result = pd.DataFrame(rows, columns=columns)

    cur.close()
    # conn.close()

    return result

def list_schemas() -> pd.DataFrame:
    '''Lists all schemas in the database.'''

    cur = get_cursor()

    cur.execute(Queries.LIST_SCHEMAS)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    result = pd.DataFrame(rows, columns=columns)

    cur.close()
    # conn.close()

    return result

def list_tables() -> pd.DataFrame:
    '''Lists all tables in the database.'''

    cur = get_cursor()

    cur.execute(Queries.LIST_TABLES)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    result = pd.DataFrame(rows, columns=columns)

    cur.close()
    # conn.close()

    return result


class Queries:
    LIST_USERS = '''
        SELECT
            usename AS username
        FROM
            pg_catalog.pg_user
        ORDER BY
            usename;
    '''

    LIST_SCHEMAS = '''
        SELECT
            schema_name,
            schema_owner
        FROM
            information_schema.schemata
        ORDER BY
            schema_name;
    '''

    LIST_TABLES = '''
        SELECT
            table_schema AS schema,
            table_name as table,
            table_type as type
        FROM
            information_schema.tables
        WHERE
            table_schema <> 'pg_catalog'
            AND table_schema <> 'information_schema'
        ORDER BY
            table_schema,
            table_name;
    '''