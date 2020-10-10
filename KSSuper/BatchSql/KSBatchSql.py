import xlrd
import os
from Export.KSExport import KSExport
from Singleton.KSSingleton import singleton

class KSBatchSql(object):

    def __init__(self):
        self.mysql = singleton.mysql

    def export_csv(self, str_sql, str_out_path, str_out_name):
        '''
        导出查询数据
        '''
        my_export = KSExport()
        my_export.export_to_csv(str_sql,str_out_path,str_out_name)

    def execute_txt_sqls(self, str_sql_path):
        for line in open(str_sql_path):
            sql = line.strip()
            if len(sql) == 0:
                break
            try:
                self.mysql.cursor.execute(sql)
                self.mysql.conn.commit()
            except:
                print("sql执行错误:"+sql)
        self.mysql.close_cursor()

    def execute_xls_sqls(self, str_sql_path, str_out_path):
        excel_sqls = xlrd.open_workbook(str_sql_path)
        sheet = excel_sqls.sheet_by_index(0)
        for index in range(sheet.nrows):
            sql = sheet.cell(int(index), 1).value
            out_name = sheet.cell(int(index), 0).value
            self.export_csv(sql, str_out_path, out_name+".csv")

# batch_sql = KSBatchSql()
# str_sql_path = os.path.abspath("../Resources/SQL/job_sql.xls")
# str_out_path = "/Users/saeipi/Desktop/jobs"
# batch_sql.execute_xls_sqls(str_sql_path, str_out_path)

# str_txt_sql_path = os.path.abspath("../Resources/SQL/job_tags.txt")
# batch_sql = KSBatchSql()
# batch_sql.execute_txt_sqls(str_txt_sql_path)
