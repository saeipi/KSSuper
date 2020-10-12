import pandas as pd
import codecs
import csv
from Singleton.KSSingleton import singleton

class KSExport(object):

    def __init__(self):
        self.mysql = singleton.mysql
        pass

    def export_csv(self, str_sql, str_out_path, str_out_name):
        self.mysql.cursor.execute(str_sql)

        # 表头
        var_name = self.mysql.cursor.description
        name = []
        for i in range(len(var_name)):
            name.append(var_name[i][0])

        #数据
        datalist = []
        var_data = self.mysql.cursor.fetchall()
        for i in range(len(var_data)):
            datalist.append(var_data[i])

        df_file = pd.DataFrame(columns=name, data=datalist)

        df_file.to_csv(str_out_path+"/"+str_out_name,index=False)
        #关闭数据库
        self.mysql.close_cursor()

    def export_to_csv(self,str_sql, str_out_path, str_out_name):
        filename = str_out_path+"/"+str_out_name
        with codecs.open(filename=filename, mode='w', encoding='utf-8') as f:
            write = csv.writer(f, dialect='excel')
            try:
                self.mysql.cursor.execute(str_sql)
                results = self.mysql.cursor.fetchall()
                df_file = pd.DataFrame(results)
                df_file.to_csv(filename, index=False)
                print(str_out_name + ":导出成功")
            except Exception as msg:
                print(msg)

# my_export = KSExport()
# sql = "SELECT * FROM Orders"
# out_path = "/Users/saeipi/Desktop/jobs"
# out_name = "export_tb.csv"
# #my_export.export_csv(sql, out_path, out_name)
# my_export.export_to_csv(sql, out_path, out_name)