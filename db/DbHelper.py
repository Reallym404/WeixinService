import pymysql
import pymysql.cursors
import time
import config

class dbHelper():

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                     user=config.DB_USER,
                                     password=config.DB_PASS,
                                     db=config.DB_NAME,
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        self.sql = """INSERT INTO suggest(date_time, suggest) VALUES (%s, %s)"""

    def suggest(self,info):
        data_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            self.cursor.execute(self.sql,(data_time,info))
            self.connection.commit()
        except:
            print('db suggest insert error!')
            self.connection.rollback()
        finally:
            self.connection.close()


