import pymysql

class KSMySQL(object):

    def __init__(self, str_db="casedb",
                 str_host="127.0.0.1",
                 str_user="root",
                 str_pwd="ksert888",
                 int_port=3306,
                 str_charset="utf8",
                 int_timeout=60):
        self.str_host = str_host
        self.str_user = str_user
        self.str_pwd = str_pwd
        self.str_db = str_db
        self.int_port = int_port
        self.str_charset = str_charset
        self.int_timeout = int_timeout

    def connect(self, dictCursor=True):
        if dictCursor:
            self.conn = pymysql.connect(
                host=self.str_host,
                user=self.str_user,
                passwd=self.str_pwd,
                port=self.int_port,
                connect_timeout=self.int_timeout,
                charset=self.str_charset,
                db=self.str_db,
                cursorclass=pymysql.cursors.DictCursor
            )
        else:
            try:
                self.conn = pymysql.connect(
                    host=self.str_host,
                    user=self.str_user,
                    passwd=self.str_pwd,
                    port=self.int_port,
                    connect_timeout=self.int_timeout,
                    charset=self.str_charset,
                    db=self.str_db,
                    cursorclass=pymysql.cursors.Cursor
                )
                print('数据库连接成功！')
            except:
                print('数据库连接失败！')

        self.cur = self.conn.cursor()
        return self.conn

    '''
    游标属性
    '''
    @property
    def cursor(self):
        if self.cur:
            return self.cur
        else:
            self.cur = self.conn.cursor()
            return self.cur

    def close_cursor(self):
        self.cur.close()
        self.cur = None

    def close_mysql(self):
        self.cur.close()
        self.conn.close()
