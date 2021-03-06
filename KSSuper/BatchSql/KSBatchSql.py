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
            except Exception as msg:
                print(msg)
        self.mysql.close_cursor()

    def execute_select_sql(self,str_sql,str_out_path,out_name):
        self.export_csv(str_sql, str_out_path, out_name + ".csv")

    def execute_xls_sqls(self, str_sql_path, str_out_path):
        excel_sqls = xlrd.open_workbook(str_sql_path)
        sheet = excel_sqls.sheet_by_index(0)
        for index in range(sheet.nrows):
            sql = sheet.cell(int(index), 1).value
            out_name = sheet.cell(int(index), 0).value
            self.export_csv(sql, str_out_path, out_name+".csv")

    def execute_sql_file(self, str_sql_file):
        fd = open(str_sql_file, 'r', encoding='utf-8')
        sql_file = fd.read()
        fd.close()
        sqlCommands = sql_file.split(';')

        for command in sqlCommands:
            try:
                self.mysql.cursor.execute(command)
            except Exception as msg:
                print(msg)

        self.mysql.close_cursor()

    def execute_file(self, str_sql_file):
        '''
        读取整个sql文件
        '''
        with open(str_sql_file, "r") as f:
            str_sql = f.read()
            try:
                self.mysql.cursor.execute(str_sql)
            except Exception as msg:
                print(msg)
        self.mysql.close_cursor()

# batch_sql = KSBatchSql()
# str_xls_sql_path = os.path.abspath("../Resources/SQL/job_sql.xls")
# str_out_path = "/Users/saeipi/Desktop/jobs"
# batch_sql.execute_xls_sqls(str_xls_sql_path, str_out_path)
#
# str_txt_sql_path = os.path.abspath("../Resources/SQL/job_tags.txt")
# batch_sql = KSBatchSql()
# batch_sql.execute_txt_sqls(str_txt_sql_path)

# sql_path = os.path.abspath("../Resources/SQL/export_sql.sql")
# batch_sql = KSBatchSql()
# print(sql_path)
# batch_sql.execute_file(sql_path)