import os
import pandas as pd
import xlrd

class KSFile(object):

    @staticmethod
    def save_df_to_csv(df_data, str_path):
        '''
        讲df数据保存到指定路径
        :param df_data: df数据
        :param str_path: 路劲
        :return:
        '''
        is_exists = os.path.exists(str_path)
        try:
            if is_exists:
                os.remove(str_path)
            df_data.to_csv(str_path)
        except:
            print('保存文件:%s失败' % str_path)

    @staticmethod
    def read_csv(str_path):
        '''
        读取csv文件
        :param str_path: 文件路径
        :return:
        '''
        is_exists = os.path.exists(str_path)
        if is_exists:
            df_data = pd.read_csv(str_path)
            return df_data

    @staticmethod
    def read_xls_sql(str_path,column):
        excel_sqls = xlrd.open_workbook(str_path)
        sheet = excel_sqls.sheet_by_index(0)
        list_res = [str(sheet.cell_value(i, column)) for i in range(column, sheet.nrows)]
        return list_res

