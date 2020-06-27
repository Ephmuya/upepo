import pyodbc
import arrow

today = arrow.now().format('DD')
month = arrow.now().format('MM')
year = arrow.now().format('YYYY')


def db_access():
    server = 'tcp:baharidbsvr.database.windows.net'
    database = 'BahariDb2'
    username = 'upepo'
    password = 'B@db81@R4'
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=' + server + ';'
        'DATABASE=' + database + ';'
        'UID=' + username + ';'
        'PWD=' + password)
    cursor = cnxn.cursor()
    return cursor
