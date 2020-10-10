from DBHelper.KSMySQL import KSMySQL

# 属性key
# 数据库配置
static_key_mysql = "static_key_mysql"

class KSSingleton(object):
    def __init__(self):
        self.dict_propertys = {}
        self.init_mysql()

    '''
    mysql
    '''
    @property
    def mysql(self):
        return self.dict_propertys.get(static_key_mysql)

    def init_mysql(self):
        mysql = KSMySQL()
        mysql.connect()
        self.dict_propertys[static_key_mysql] = mysql
        return mysql

    def close_mysql(self):
        mysql = self.dict_propertys.get(static_key_mysql)
        if mysql:
            mysql.close()

singleton = KSSingleton()
# singleton.mysql_helper #通过属性懒加载对象