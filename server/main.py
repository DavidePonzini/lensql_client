from flask import Flask, request
from flask_cors import CORS
import json
import pandas as pd


from client.server.sql_errors import SQLException
import llm
import client.server.db as db


app = Flask(__name__)
CORS(app)


def response(data: pd.DataFrame | SQLException) -> str:
    return str(data)

@app.route('/run-query', methods=['POST'])
def run_query():
    query = json.loads(request.form['query'])

    result = db.execute_query(query)

    return response(result)

@app.route('/list-users', methods=['GET'])
def list_users():
    result = db.list_users()
    return response(result)

@app.route('/list-schemas', methods=['GET'])
def list_schemas():
    result = db.list_schemas()
    return response(result)

@app.route('/list-tables', methods=['GET'])
def list_tables():
    result = db.list_tables()
    return response(result)


if __name__ == '__main__':
    app.run(
    	host='0.0.0.0',
    	debug=True
    )
