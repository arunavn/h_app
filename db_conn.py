#import mysql
#mydb = mysql.connector.connect(host='sql228.main-hosting.eu',user='u474015652_arunav03',passwd='03@arunav')




import pymysql

def connect_to_db():
    connection = pymysql.connect(host='sql228.main-hosting.eu',
                                 port=3306,
                                 user='u474015652_arunav03',
                                 password='03@arunav',
                                 db='u474015652_demo1',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection



