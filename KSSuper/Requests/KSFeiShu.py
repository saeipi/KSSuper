# coding: utf-8
import requests
import json
from Requests.KSApi import KSApi
class KSFeiShu(object):

    #01
    def access_token_request(self,str_spreadsheet_token,callback):
        try:
            response = requests.post(
                url=KSApi.feishu_authen_access_token,
                headers={
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "code": "u1ToPJj8IzzQC8wtzlmBfe",
                    "app_access_token": "t-b280e8ab888075ee6eb2a516dec704b740d94e49",
                    "grant_type": "authorization_code"
                })
            )
            callback(response.status_code,response.text,str_spreadsheet_token)
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(
                content=response.content.decode('utf-8')))
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

    # 02
    def access_token_callback(self,int_status_code,str_content,str_spreadsheet_token):
        if int_status_code==200:
            dict_res = json.loads(str_content)
            str_access_token = dict_res["data"]["access_token"]
            self.spreadsheets_request(str_access_token,str_spreadsheet_token,str_range)

    # 03
    def spreadsheets_request(self,str_access_token,str_spreadsheet_token,callback):
        '''
        获取表格元数据
        :param str_access_token:
        :param str_spreadsheet_token:
        :param callback:
        :return:
        '''
        try:
            response = requests.get(
                url=KSApi.feishu_spreadsheets_all % (str_spreadsheet_token),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {str_access_token}",
                },
            )
            callback(response.status_code, response.text)
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(
                content=response.content))
        except requests.exceptions.RequestException:
            print('HTTP Request failed')


    def spreadsheets_rang_request(self,str_access_token,str_spreadsheet_token,str_range,callback):
        '''
        读取单个范围
        :param str_access_token:
        :param str_spreadsheet_token:
        :param str_range:
        :param callback:
        :return:
        '''
        try:
            response = requests.get(
                url=KSApi.feishu_spreadsheets_rang % (str_spreadsheet_token,str_range),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {str_access_token}"
                },
                params={
                    "valueRenderOption": "ToString",
                },
            )
            callback(response.status_code,response.text)
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            #print('Response HTTP Response Body: {content}'.format(content=response.content))
            #print(response.text.encode('utf8'))
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

    def spreadsheets_callback(self,int_status_code,str_content):
        if int_status_code == 200:
            json_res = json.loads(str_content)

#u-YfksIS5XizOflDW1Dtnzdf
fs = KSFeiShu()
str_access_token = "u-YfksIS5XizOflDW1Dtnzdf"
str_spreadsheet_token = "shtcnCq5xjRL7TMkr8bld2BaMWc"
str_range = "Y35XsM!A2:Z128"
fs.spreadsheets_request(str_access_token,str_spreadsheet_token,fs.spreadsheets_callback)