'''

提供数据库读写操作

'''

import pymysql


class Tag:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='douban',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    def insert(self, name, url):
        sql = "INSERT INTO tag(name,url) VALUES (%s,%s);"
        self.cursor.executemany(sql, [(name, url)])
        self.conn.commit()

    def query(self):
        sql = "SELECT * FROM tag;"
        self.cursor.execute(sql)
        names = []
        urls = []
        for i in self.cursor.fetchall():
            names.append(i[1])
            urls.append(i[2])
        print('共查询到数据' + str(self.cursor.rowcount))
        return names, urls

    def __del__(self):
        pass
        # self.cursor.close()
        # self.conn.close()


class Book:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='douban',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    def insert(self, name, url):
        sql = "INSERT INTO book(name,url) VALUES (%s,%s);"
        self.cursor.executemany(sql, [(name, url)])
        self.conn.commit()

    def __del__(self):
        pass
    # self.cursor.close()
    # self.conn.close()

'''
上面可以删掉
下面重构
'''


class Db:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='douban',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    def taginsert(self, name, url):#插入标签数据
        sql = "INSERT INTO tag(name,url) VALUES (%s,%s);"
        self.cursor.executemany(sql, [(name, url)])
        self.conn.commit()

    def tagquery(self):#查询标签数据
        sql = "SELECT * FROM tag;"
        self.cursor.execute(sql)
        names = []
        urls = []
        for i in self.cursor.fetchall():
            names.append(i[1])
            urls.append(i[2])
        print('共查询到数据' + str(self.cursor.rowcount))
        return names, urls

    def bookinsert(self, name, auth, press, time, pages, price, ISBN, score, assessor,url):#插入书本数据
        sql = "INSERT INTO book(name, auth, press, time, pages, price, ISBN, score, assessor,url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        self.cursor.executemany(sql, [(name, auth, press, time, pages, price, ISBN, score, assessor,url)])
        self.conn.commit()

    def __del__(self):
        pass
        # self.cursor.close()
        # self.conn.close()
