import pymysql
import os

def mysql_connection():
    # MySQL 연결 정보
    connection = pymysql.connect(
    user=os.environ['RDS_DB_ID'], 
    passwd=os.environ['RDS_DB_PWD'], 
    host=os.environ['RDS_DB_HOST'], 
    db=os.environ['RDS_DB_NAME'],
    cursorclass=pymysql.cursors.DictCursor
    )

    # cursor = rds_db.cursor(pymysql.cursors.DictCursor)
    
    return connection