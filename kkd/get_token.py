#получаем X-AUTH-TOKEN со stage

import psycopg2

try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect(dbname='ispk8s', user='ispk8s_stage', password='lwSGSHli2Et5nWhZ', host='10.207.33.194')
except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Can`t establish connection to database')

cursor = conn.cursor()
sql_command = "select token, user_id, status from msp_admin_service.tokens where status = 'ALLOWED' AND user_id = '66';"
cursor.execute(sql_command)
tokens = cursor.fetchall()

for token in tokens:
    print('token: ', token[0])
    print('user_id: ', token[1])
    print('status: ', token[2])
    print('-----------------')
cursor.close()
conn.close()