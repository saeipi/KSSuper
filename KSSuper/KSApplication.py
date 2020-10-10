import os
from Import.KSImport import KSImport
from Export.KSExport import KSExport
from BatchSql.KSBatchSql import KSBatchSql
from Requests.KSDruidRequest import KSDruidRequest

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
        '''
        查询并导出数据
        :param str_xls_sql_path: sql语句表路径
        :param str_out_path: 导出路径
        :return:
        '''
        batch_sql = KSBatchSql()
        batch_sql.execute_xls_sqls(str_xls_sql_path, str_out_path)

    def request_druid_task_callback(self,int_status_code,str_content):
        print("druid 任务回调")
        pass

    def request_druid_task(self,str_json_path,base_dir,data_source):
        req = KSDruidRequest()

        req.send_request(str_json_path, base_dir, data_source,self.request_druid_task_callback)
        pass

str_parent_path = os.path.dirname(os.path.realpath(__file__))
str_xls_sql_path = str_parent_path + "/Resources/SQL/job_sql.xls"
str_job_tag_path = str_parent_path + "/Resources/SQL/job_tags.txt"
str_json_path = str_parent_path + "/Resources/Json/task_json.json"
print(str_xls_sql_path)
print(str_job_tag_path)

'''
1、导入数据
'''
app = KSApplication()
str_import_path = "/Users/saeipi/Desktop/MyDatabase/1009data"
app.import_csv_path(str_import_path)

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
app.execute_select(str_xls_sql_path, str_out_path)

'''
4、提交任务
'''
base_dir = "/home/sa/apache-druid/datas/level"
data_source = "ks_test_data_03"
app.request_druid_task(str_json_path,base_dir,data_source)