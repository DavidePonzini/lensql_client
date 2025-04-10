from typing import Iterator
from flask import Flask, request
from flask_cors import CORS
import json
import pandas as pd

import db
from db import QueryResult
import server
from sql_errors import SQLException


app = Flask(__name__)
CORS(app)


def response(status: bool, **kwargs):
    return json.dumps({
        'status': 'success' if status else 'error',
        **kwargs
    })


def response_query(*results: QueryResult, is_builtin: bool = False) -> str:
    result = []
    
    for query in results:
        query_result = {
            'success': query.success,
            'builtin': is_builtin,
            'query': query.query,
        }

        if isinstance(query.result, SQLException):
            query_result['type'] = 'message'
            query_result['data'] = str(query.result)
        
        elif isinstance(query.result, str):
            query_result['type'] = 'message'
            query_result['data'] = query.result

        elif isinstance(query.result, pd.DataFrame):
            query_result['type'] = 'dataset'
            query_result['data'] = query.result.to_json(orient='split')
        else:
            query_result['type'] = 'message'
            query_result['data'] = 'Unknown error'

        result.append(query_result)

    return json.dumps(result)

@app.route('/run-query', methods=['POST'])
def run_query():
    query = request.get_json()['query']

    result = list(db.execute_query(query))

    return response_query(*result)

@app.route('/list-users', methods=['GET'])
def list_users():
    result = db.list_users()
    return response_query(QueryResult(result, 'Users', True), is_builtin=True)

@app.route('/list-schemas', methods=['GET'])
def list_schemas():
    result = db.list_schemas()
    return response_query(QueryResult(result, 'Schemas', True), is_builtin=True)

@app.route('/list-tables', methods=['GET'])
def list_tables():
    result = db.list_tables()
    return response_query(QueryResult(result, 'Tables', True), is_builtin=True)

@app.route('/login-db', methods=['POST'])
def login_db():
    data = request.get_json()
    db_name = data['db_name']
    db_username = data['db_username']
    db_password = data['db_password']

    result = db.connect(dbname=db_name, username=db_username, password=db_password)

    return response(result)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']

    result = server.login(username)

    return response(result)
    


if __name__ == '__main__':
    app.run(
    	host='0.0.0.0',
    	debug=True,
        port=5000,
    )
