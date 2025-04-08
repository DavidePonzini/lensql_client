import sqlparse
from typing import Self


class SQLCode:
    def __init__(self, query: str):
        self.query = query

    def strip_comments(self) -> Self:
        '''Remove comments from the SQL query'''
        code = sqlparse.format(self.query, strip_comments=True)
        return SQLCode(code)

    def has_clause(self, clause: str) -> bool:
        '''Check if the SQL query has a specific clause'''
        return clause.upper() in self.query.upper()

    def split(self) -> list[Self]:
        '''Split the SQL query into individual statements'''
        queries = sqlparse.split(self.query)
        return [SQLCode(query) for query in queries]
    
    @property
    def first_token(self) -> str:
        statement = sqlparse.parse(self.query)[0]
        first_token = statement.token_first(skip_cm=True)
        return first_token.value.upper()


    def __str__(self) -> str:
        return self.query
    