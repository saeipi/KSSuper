from Import.KSImport import KSImport
from Export.KSExport import KSExport
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

app = KSApplication()
app.import_csv_path("/Users/saeipi/Desktop/jobs")

sql = "SELECT * FROM Orders"
out_path = "/Users/saeipi/Desktop/jobs"
out_name = "export_tb.csv"
app.export_csv(sql,out_path,out_name)