import xlrd
import os

import sys;
print('Python %s on %s' % (sys.version, sys.platform))
print(sys.path)
from Export.KSExport import KSExport

class KSBatchSql(object):

    def __init__(self):
        pass

    def export_csv(self, str_sql, str_out_path, str_out_name):
        '''
        导出查询数据
        '''
        my_export = KSExport()
        my_export.export_to_csv(str_sql,str_out_path,str_out_name)

    def execute_sqls(self, str_sql_path, str_out_path):
        excel_sqls = xlrd.open_workbook(str_sql_path)
        sheet = excel_sqls.sheet_by_index(0)
        for index in range(sheet.nrows):
            sql = sheet.cell(int(index), 1).value
            out_name = sheet.cell(int(index), 0).value
            self.export_csv(sql, str_out_path, out_name+".csv")

# batch_sql = KSBatchSql()
# str_sql_path = os.path.abspath("../Resources/SQL/job_sql.xls")
# str_out_path = "/Users/saeipi/Desktop/jobs"
# batch_sql.execute_sqls(str_sql_path, str_out_path)


# sys.path.extend([WORKING_DIR_AND_PYTHON_PATHS])