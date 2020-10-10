import datetime
from dateutil.relativedelta import relativedelta
from enum import Enum

class KSEnDateFormatType(Enum):
    # 正常的，例如2018-08-08
    standard  = 1
    # 简约的，例如20180808
    simple    = 2

class KSDate(object):

    @staticmethod
    def last_month(en_format_type):
        '''
        上个月
        :return:
        '''
        str_date_format = '%Y-%m-%d'
        if en_format_type == KSEnDateFormatType.simple:
            str_date_format = '%Y%m%d'

        return (datetime.date.today() - relativedelta(months=+1)).strftime(str_date_format)

    @staticmethod
    def specified_date_last_month(str_specified_date,en_specified_date_type,en_target_date_type):
        '''
        指定日期上个月
        :param str_specified_date: 指定的日期
        :param en_specified_date_type: 指定的日期的类型
        :param en_target_date_type: 返回的数据类型
        :return:
        '''
        return KSDate.specified_date_month(str_specified_date,en_specified_date_type,1,en_target_date_type)

    @staticmethod
    def specified_date_month(str_specified_date,en_specified_date_type,int_previous_months,en_target_date_type):
        '''
        指定日期前个月
        :param str_specified_date: 指定的日期
        :param en_specified_date_type: 指定的日期的类型
        :param int_previous_months: 前几个月
        :param en_target_date_type: 返回的数据类型
        :return:
        '''
        str_specified_date_format = '%Y-%m-%d'
        if en_specified_date_type == KSEnDateFormatType.simple:
            str_specified_date_format = '%Y%m%d'

        str_target_date_format = '%Y-%m-%d'
        if en_target_date_type == KSEnDateFormatType.simple:
            str_target_date_format = '%Y%m%d'

        # 字符串转化为date形式
        dt_date = datetime.datetime.strptime(str_specified_date, str_specified_date_format)
        return (dt_date - relativedelta(months=+int_previous_months)).strftime(str_target_date_format)

    @staticmethod
    def format_date(str_specified_date, en_specified_date_type, en_target_date_type):
        str_specified_date_format = '%Y-%m-%d'
        if en_specified_date_type == KSEnDateFormatType.simple:
            str_specified_date_format = '%Y%m%d'

        str_target_date_format = '%Y-%m-%d'
        if en_target_date_type == KSEnDateFormatType.simple:
            str_target_date_format = '%Y%m%d'

        # 字符串转化为date形式
        dt_date = datetime.datetime.strptime(str_specified_date, str_specified_date_format)
        return  datetime.datetime.strftime(dt_date, str_target_date_format)

# print(ASDate.format_date("20190101",EnDateFormatType.simple,EnDateFormatType.standard))