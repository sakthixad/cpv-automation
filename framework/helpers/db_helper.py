import psycopg2

def db_pg_connect():

    conn_string = "host='poi-slave.mgmt.xad.com' dbname='xaddb' user='apps' password='x@d4P55'"
    conn = psycopg2.connect(conn_string)

    return conn


def db_close_connection(cnx):
    cnx.close()


def get_result(cnx,query):

    sql = query
    cur = cnx.cursor(dictionary=True)
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        return row

def get_all_result(cnx,query):

    sql = query
    cur = cnx.cursor(dictionary=True)
    cur.execute(sql)
    result = cur.fetchall()
    return result

def get_result_set_list(cnx, query, col_name):

    list = []
    sql = query
    cur = cnx.cursor(dictionary=True)
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        list.append(row[col_name])
    list.sort()
    return list