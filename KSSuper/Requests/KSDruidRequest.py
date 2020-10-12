import requests
import json
import os
from Communal.Category.KSFile import KSFile
from Export.KSExportDruidSql import KSExportDruidSql
class KSDruidRequest(object):

    def __init__(self):
        pass

    def request_body(self, str_json_path, str_base_dir, str_data_source="my_data_source"):
        with open(str_json_path, 'r', encoding='utf8')as fp:
            json_data = json.load(fp)
            json_data["spec"]["ioConfig"]["inputSource"]["baseDir"] = str_base_dir
            json_data["spec"]["dataSchema"]["dataSource"] = str_data_source
            return json_data

    def request_mysql_body(self, str_json_path,str_data_source,list_sqls):
        with open(str_json_path, 'r', encoding='utf8')as fp:
            json_data = json.load(fp)
            json_data["spec"]["dataSchema"]["dataSource"] = str_data_source
            json_data["spec"]["ioConfig"]["inputSource"]["sqls"] = list_sqls
            print(json_data)
            return json_data

    def send_request(self,str_json_path, str_base_dir, str_data_source,callback):
        try:
            response = requests.post(
                url="http://116.66.17.9:8888/druid/indexer/v1/task",
                headers={
                    "Content-Type": "application/json;charset=utf-8",
                },
                data=json.dumps(self.request_body(str_json_path,str_base_dir,str_data_source))
            )
            if callback:
                callback(response.status_code,response.content)
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(
                content=response.content))
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

    def send_mysql_request(self,str_json_path,str_data_source,list_sqls,callback):
        try:
            response = requests.post(
                url="http://127.0.0.1:8888/druid/indexer/v1/task",
                headers={
                    "Content-Type": "application/json;charset=utf-8",
                },
                data=json.dumps(self.request_mysql_body(str_json_path,str_data_source,list_sqls))
            )
            if callback:
                callback(response.status_code,response.content)
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(
                content=response.content))
        except requests.exceptions.RequestException:
            print('HTTP Request failed')
    pass



# str_json_path = os.path.abspath("../Resources/Json/task_json.json")
# base_dir = "/home/sa/apache-druid/datas/level"
# data_source = "ks_test_data_02"
# req.send_request(str_json_path, base_dir, data_source,None)

#str_xls_sql_path = os.path.abspath("../Resources/SQL/job_sql_v1.0.xls")
#list_sqls = KSFile.read_xls_sql(str_xls_sql_path,1)
# print(list_sqls)
# #list_sqls = ["SELECT * FROM Orders","SELECT * FROM Persons"]
# req.send_mysql_request(str_json_path,data_source,list_sqls,None)

req = KSDruidRequest()
str_json_path = os.path.abspath("../Resources/Json/task_json_v3.0.json")
data_source = "ks_test_data_25"
list_sqls = KSExportDruidSql.druid_sqls
req.send_mysql_request(str_json_path,data_source,list_sqls,None)