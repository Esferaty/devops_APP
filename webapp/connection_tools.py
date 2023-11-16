from db_config import db_config
import mysql.connector


def cursor_wrapper(func):
    def wrapper(*args, **kwargs):
        print(func)
        connection = mysql.connector.connect(**db_config)
        print('Connection opened')
        cursor = connection.cursor()
        print('Cursor opened')
        query = func(*args, **kwargs)
        print(query)
        cursor.execute(query)
        if 'SELECT' in query:
            results = cursor.fetchall()
        else:
            results = None
        print('Cursor executed')
        cursor.close()
        print('Cursor closed')
        if 'INSERT' in query:
            connection.commit()
            print('Changes commited')
        connection.close()
        print('Connection closed\n')
        return results

    return wrapper


def wrap_in_quotes(iterable):
    return [f"'{i}'" for i in iterable]


class ConnectorDB:

    @cursor_wrapper
    def select(self, it_columns, target_table, joins=None, where=None, order_by=None, between=None):
        query = f"SELECT {', '.join(it_columns)} FROM {target_table} "
        query += ' '.join(['JOIN ' + i for i in joins]) if joins else ''
        query += f' WHERE {where}' if where else ''
        query += f' BETWEEN {between[0]} AND {between[1]}' if between else ''
        query += f' ORDER BY {order_by}' if order_by else ''
        return query

    @cursor_wrapper
    def insert(self, target_table, it_columns, it_values):
        query = f"INSERT INTO {target_table} ({','.join(it_columns)}) VALUES({','.join(wrap_in_quotes(it_values))})"
        return query