from typing import Iterator
from flask import Flask, request
from flask_cors import CORS
import json
import pandas as pd

import db
from sql_errors import SQLException


app = Flask(__name__)
CORS(app)


def response(status: bool, **kwargs):
    return json.dumps({
        'status': 'success' if status else 'error',
        **kwargs
    })


def response_query(*results: tuple[pd.DataFrame | str | SQLException, str], is_builtin: bool = False) -> str:
    result = []
    
    for query_result, query in results:
        print(query_result, type(query_result))
        if isinstance(query_result, SQLException):
            result.append({
                'success': False,
                'builtin': is_builtin,
                'type': 'message',
                'query': query,
                'data': str(query_result),
            })
        
        elif isinstance(query_result, str):
            result.append({
                'success': True,
                'builtin': is_builtin,
                'type': 'message',
                'query': query,
                'data': query_result,
            })

        elif isinstance(query_result, pd.DataFrame):
            result.append({
                'success': True,
                'builtin': is_builtin,
                'type': 'dataset',
                'query': query,
                'data': query_result.to_json(orient='split'),
            })
        else:
            result.append({
                'success': False,
                'builtin': is_builtin,
                'type': 'message',
                'query': query,
                'data': 'Unknown error',
            })

    return json.dumps(result)

@app.route('/run-query', methods=['POST'])
def run_query():
    query = request.get_json()['query']

    result = list(db.execute_query(query))

    return response_query(*result)

@app.route('/list-users', methods=['GET'])
def list_users():
    result = db.list_users()
    return response_query((result, 'Users'), is_builtin=True)

@app.route('/list-schemas', methods=['GET'])
def list_schemas():
    result = db.list_schemas()
    return response_query((result, 'Schemas'), is_builtin=True)

@app.route('/list-tables', methods=['GET'])
def list_tables():
    result = db.list_tables()
    return response_query((result, 'Tables'), is_builtin=True)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    db_name = data['db_name']
    db_username = data['db_username']
    db_password = data['db_password']

    result = db.connect(dbname=db_name, username=db_username, password=db_password)

    return response(result)

    


if __name__ == '__main__':
    app.run(
    	host='0.0.0.0',
    	debug=True,
        port=5000,
    )
