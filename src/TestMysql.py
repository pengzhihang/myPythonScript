#coding:utf-8

import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='10.1.1.52',
                             user='root',
                             password='Stone@123',
                             db='new_coin_web',
                             port=3306)

try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
# 
#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "show tables"
        cursor.execute(sql)
        result = cursor.fetchall()
        print type(result)
        print(result)
finally:
    connection.close()
