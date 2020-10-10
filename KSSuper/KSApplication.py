import os
from Import.KSImport import KSImport
from Export.KSExport import KSExport
from BatchSql.KSBatchSql import KSBatchSql

class KSApplication(object):
    def __init__(self):
        pass

    def import_csv_path(self, str_path):
        '''
        导入文件夹csv文件到数据库
        '''
        my_import = KSImport()
        my_import.import_csv_path(str_path)

    def export_csv(self, str_sql, str_out_path, str_out_name):
        '''
        导出查询数据
        '''
        my_export = KSExport()
        my_export.export_to_csv(str_sql,str_out_path,str_out_name)

'''
1、导入数据
'''
app = KSApplication()
app.import_csv_path("/Users/saeipi/Desktop/jobs")

# sql = "SELECT * FROM Orders"
# out_path = "/Users/saeipi/Desktop/jobs"
# out_name = "export_tb.csv"
# app.export_csv(sql,out_path,out_name)

'''
2、更新tag
'''
batch_sql = KSBatchSql()
str_txt_sql_path = os.path.abspath("../Resources/SQL/job_tags.txt")
batch_sql = KSBatchSql()
batch_sql.execute_txt_sqls(str_txt_sql_path)

'''
3、查询并导出数据
'''
str_xls_sql_path = os.path.abspath("../Resources/SQL/job_sql.xls")
str_out_path = "/Users/saeipi/Desktop/jobs"
batch_sql.execute_xls_sqls(str_xls_sql_path, str_out_path)

