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

    def update_tag(self,str_text_tag_path):
        '''
        更新tag
        '''
        batch_sql = KSBatchSql()
        batch_sql.execute_txt_sqls(str_text_tag_path)

    def execute_select(self,str_xls_sql_path,str_out_path):
        batch_sql = KSBatchSql()
        batch_sql.execute_xls_sqls(str_xls_sql_path, str_out_path)
        pass


str_parent_path = os.path.dirname(os.path.realpath(__file__))
str_xls_sql_path = str_parent_path + "/Resources/SQL/job_sql.xls"
str_job_tag_path = str_parent_path + "/Resources/SQL/job_tags.txt"
print(str_xls_sql_path)
print(str_job_tag_path)

'''
1、导入数据
'''
print(os.path.abspath("../Resources/SQL/job_tags.txt"))
app = KSApplication()
app.import_csv_path("/Users/saeipi/Desktop/jobs")

# sql = "SELECT * FROM Orders"
# out_path = "/Users/saeipi/Desktop/jobs"
# out_name = "export_tb.csv"
# app.export_csv(sql,out_path,out_name)

'''
2、更新tag
'''
app.update_tag(str_job_tag_path)

'''
3、查询并导出数据
'''
str_out_path = "/Users/saeipi/Desktop/jobs"
app.execute_select(str_xls_sql_path,str_out_path)