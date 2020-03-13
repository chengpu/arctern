import psycopg2
import sys

conn_config = "dbname='postgres' host='192.168.2.36' port=5432 user='postgres'"
conn = psycopg2.connect(conn_config)

cur = conn.cursor()
sql = r"select datname from pg_database;"

sql_template_1 = "select %s('%s'::geometry)"
sql_template_2 = "select %s('%s'::geometry, '%s'::geometry)"
sql_template_3 = "select st_astext(%s('%s'::geometry, %s))"
sql_template_4 = "select st_astext(%s('%s'::geometry, '%s'::geometry))"
sql_template_5 = "select st_astext(%s('%s'::geometry))"

st_buffer = ['st_buffer']
intersection = ['st_intersection']
convexhull = ['st_convexhull']


def get_sqls_from_data(function_name, file_path):
    sql_arr = []
    with open(file_path, 'r') as f:
        lines = f.readlines()[1:]
        lines = [x.strip().split('|') for x in lines]
        for line in lines:
            if len(line) == 1:
                if function_name in convexhull:
                    sql = sql_template_5 % (function_name, line[0])
                else:
                    sql = sql_template_1 % (function_name, line[0])
                    
            if len(line) == 2:
                if function_name in st_buffer:
                    sql = sql_template_3 % (function_name, line[0], line[1])
                elif function_name in intersection:
                    arr.append(sql_template_4 % (function_name, values[0], values[1]))
                else:
                    arr.append(sql_template_2 % (function_name, values[0], values[1]))    
            
            sql_arr.append(sql)
    return sql_arr

def execute_sql(sql):
    cur.execute(sql)
    rows = [row for row in cur.fetchall()]
    for r in rows:
        return r[0]


def get_postgis_result(sqls, result_path):
    results = [execute_sql(sql) for sql in sqls]
    with open(result_path, 'w') as f:
        for r in results:
            f.writelines(r + '\n')

if __name__ == '__main__':
    function_name = sys.argv[1]
    file_path = sys.argv[2]
    result_path = sys.argv[3]
    sqls = get_sqls_from_data(file_path)
    get_postgis_result(sqls, result_path)
