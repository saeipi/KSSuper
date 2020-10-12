import os
import pandas as pd
from Singleton.KSSingleton import singleton
class KSImport(object):

    def __init__(self):
        self.mysql = singleton.mysql

    def import_csv_path(self, str_path):
        os.chdir(str_path)
        path = os.getcwd()
        files = os.listdir(path)

        i = 0  # 计数器，后面可以用来统计一共导入了多少个文件
        for file in files:
            if file.split('.')[-1] in ['csv']:  # 判断文件是不是csv文件，file.split('.')[-1]获取‘.’后的字符串
                i += 1
                filename = file.split('.')[0]  # 获取剔除后缀的名称
                f = pd.read_csv(file, encoding='utf8')  # 用pandas读取文件，得到pandas框架格式的数据
                columns = f.columns.tolist()  # 获取表格数据内的列标题文字数据

                types = f.dtypes  # 获取文件内数据格式
                field = []  # 设置列表用来接收文件转换后的数据，为写入mysql做准备
                table = []
                char = []
                for item in range(len(columns)):  # 开始循环获取文件格式类型并将其转换成mysql文件格式类型
                    if 'object' == str(types[item]):
                        if columns[item] == "description" or columns[item] == "comment":
                        #if len(f[columns[item]][item]) > 255:
                            char = '`' + columns[item] + '`' + ' LONGTEXT'  # 临时处理
                        else:
                            char = '`' + columns[item] + '`' + ' VARCHAR(255)'  # 必须加上`这个点，否则在写入mysql是会报错
                    elif 'int64' == str(types[item]):
                        char = '`' + columns[item] + '`' + ' INT'
                    elif 'float64' == str(types[item]):
                        char = '`' + columns[item] + '`' + ' FLOAT'
                    elif 'datetime64[ns]' == str(types[item]):
                        char = '`' + columns[item] + '`' + ' DATETIME'
                    else:
                        char = '`' + columns[item] + '`' + ' VARCHAR(255)'
                    table.append(char)
                    field.append('`' + columns[item] + '`')

                tables = ','.join(table)  # 将table中的元素用，连接起来为后面写入mysql做准备
                fields = ','.join(field)

                self.mysql.cursor.execute('drop table if exists {};'.format(filename))
                self.mysql.conn.commit()

                # 创建表格并设置表格的列文字跟累数据格式类型
                table_sql = 'CREATE TABLE IF NOT EXISTS ' + filename + '(' + tables + ');'
                print('表:' + filename + ',开始创建数据表...')
                self.mysql.cursor.execute(table_sql)
                self.mysql.conn.commit()
                print('表:' + filename + ',创建成功!')

                print('表:' + filename + ',正在写入数据当中...')
                f_sql = f.astype(object).where(pd.notnull(f), None)  # 将原来从csv文件获取得到的空值数据设置成None，不设置将会报错
                values = f_sql.values.tolist()  # 获取数值
                s = ','.join(['%s' for _ in range(len(f.columns))])  # 获得文件数据有多少列，每个列用一个 %s 替代
                insert_sql = 'insert into {}({}) values({})'.format(filename, fields, s)
                self.mysql.cursor.executemany(insert_sql, values)
                self.mysql.conn.commit()
                print('表:' + filename + ',数据写入完成！')

        self.mysql.close_cursor()
        print('文件导入数据库完成！一共导入了 {} 个CSV文件。'.format(i))

# imp = KSImport()
# str_path = "/Users/saeipi/Desktop/MyDatabase/928data/source"
# imp.import_csv_path(str_path)

