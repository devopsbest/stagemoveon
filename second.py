# from jira import client
#
# clients = client('HOST', 'USER', 'PASSWORD') # Host must have trailing slash

import pandas as pd

git_url = "https://www.open-open.com/github/"

page_result = pd.read_html(git_url)[0]
# print(type(page_result))
# print(len(page_result))
# print(page_result)
# print(page_result["语言"])
# print(page_result.loc[page_result["语言"] == "Python"])

#
import os
my_path = os.path.split(os.path.realpath(__file__))[0]
# my_file = my_path + "/" + file_name
#
# print(my_file)

def get_csv(language):

    python_result = page_result.loc[page_result["语言"] == language]

    # sort_values has already replace sort
    python_result.sort_values(["Star"],ascending=True)
    # print(python_result)
    #axis=1（按列方向操作）、inplace=True（修改完数据，在原数据上保存）

    #按标签来删除列

    python_result.drop(['语言'],axis=1,inplace=True)
    python_result['名称']= "https://github.com/" + python_result['名称']
    python_result.head(20).to_csv(my_path + "/" +"{}.csv".format(language),sep="\t",mode='a', index=True, header=True)
    #



if __name__ == "__main__":
    language = ["Python", "JavaScript","Java"]
    for lan in language:
        get_csv(lan)
import yagmail


# #链接邮箱服务器
#
# yag = yagmail.SMTP( user="lucklly@163.com", password="Good_Luck888", host='smtp.163.com',smtp_ssl=True)
#
# # 邮箱正文
# contents = ['python code for github']
#
# # 发送邮件
# yag.send(to='117732865@qq.com', subject='Read the code', contents=contents,attachments =my_file)
