import datetime
import smtplib
from email.header import Header
from email.mime.text import MIMEText

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from jira import JIRA

MAIL_HOST = "smtp.office365.com"
SMTP_PORT = 587
mail_user = "qa"
mail_password = "test"
jira_server = 'http://jira.eflabs.cn'  # jira地址
jira_username = 'ming.'  # 用户名
jira_password = 'Good'  # 密码
MAX_RESULTS = 600

jira = JIRA(server=jira_server, basic_auth=(jira_username, jira_password))
datetimenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def sent_mails():
    try:
        server = smtplib.SMTP(MAIL_HOST, SMTP_PORT)
        server.starttls()

        server.login(mail_user, mail_password)
        me = mail_user

        msg = MIMEText("hello", 'text', 'utf-8')
        msg['From'] = me
        msg['To'] = "ming"
        msg['Subject'] = Header("hello", 'utf-8')
        server.sendmail(me, "min", msg.as_string())
        server.close()
        print("pass")
        return True

    except Exception:
        print("fail")
        return False


def get_account(sql):
    result = jira.search_issues(sql, maxResults=MAX_RESULTS)
    return len(result)


def jira_search_bug_status():
    # print(jira.user(jira.current_user()))#当前用户


    android_total = "labels = OneApp AND component = Android"
    android_closed = 'labels = OneApp AND component = Android and status in (Closed, "UAT GLed")'
    android_resolved = "labels = OneApp AND component = Android and status = Resolved"
    android_open = "labels = OneApp AND component = Android and status = Open"

    IOS_total = "labels = OneApp AND component = IOS"
    IOS_closed = 'labels = OneApp AND component = IOS  and status in (Closed, "UAT GLed")'
    IOS_resolved = 'labels = OneApp AND component = IOS and status = Resolved'
    IOS_open = 'labels = OneApp AND component = IOS and status = Open'

    BE_total = "labels = OneApp AND component in (Backend, Blurb, backend, BackEnd)"
    BE_closed = 'labels = OneApp AND component in (Backend, Blurb, backend, BackEnd) and status in (closed, "UAT GLed")'
    BE_resolved = "labels = OneApp AND component in (Backend, Blurb, backend, BackEnd) and status=Resolved"
    BE_open = "labels = OneApp AND component in (Backend, Blurb, backend, BackEnd) and status=Open"

    Android_numbers = [get_account(x) for x in [android_total, android_closed, android_resolved, android_open]]
    IOS_numbers = [get_account(x) for x in [IOS_total, IOS_closed, IOS_resolved, IOS_open]]
    BE_numbers = [get_account(x) for x in [BE_total, BE_closed, BE_resolved, BE_open]]

    bug_search_result = np.array([Android_numbers, IOS_numbers, BE_numbers]).reshape(3, 4)

    print(bug_search_result)

    bug_search_df = pd.DataFrame(bug_search_result, index=["Android", "IOS", "BE"],
                                 columns=['total', 'closed', 'resolved', 'open'])

    return bug_search_df


def bug_status_picture(df):
    df.plot.bar()
    plt.xlabel('Develop')
    # 设置y周标签
    plt.ylabel('Bug number')
    # 设置图表标题
    plt.title('OneApp bug status')
    # # 设置图例的文字和在图表中的位置
    # plt.legend(, loc='upper right')
    # 设置背景网格线的颜色，样式，尺寸和透明度
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.4)
    plt.show()
    plt.savefig("OneApp_bug_{}.png".format(datetimenow))


def bug_query():
    one_app_open_bug_filter_url = "https://jira.eflabs.cn/issues/?filter=163201"

    base_url = "https://jira.eflabs.cn/rest/gadget/1.0/login"
    data = {
        "os_username": jira_username,
        "os_password": jira_password,
        "os_cookie": True

    }
    res = requests.session()
    res.post(base_url, data)

    one_app_open_bug_status = res.get(one_app_open_bug_filter_url)

    #
    bug_result = pd.read_html(one_app_open_bug_status.text)
    bug_result_df = bug_result[0]
    print(bug_result_df)
    show_list = ["Key", "Summary", "Assignee", "Status", "Created"]
    bug_detail_df = bug_result_df[show_list]
    print(bug_detail_df)

    dev_detail = bug_result_df.groupby("Assignee").size()
    print(dev_detail)

    return bug_detail_df, dev_detail.to_frame()


def generate_df_html(arg):
    html_str = ""
    html_temp = """
                <h2>{}</h2>

            <div>
                <h4></h4>
                {}

            </div>
            <hr>
    """

    for k, v in arg.items():
        df_html = v.to_html(escape=False)

        html_str = html_str + html_temp.format(k, df_html)

    return html_str


def get_html_msg(df):
    head = \
        """
        <head>
            <meta charset="utf-8">
            <STYLE TYPE="text/css" MEDIA=screen>

                table.dataframe {
                    border-collapse: collapse;
                    border: 2px solid #a19da2;
                    /*居中显示整个表格*/
                    margin: left;
                }

                table.dataframe thead {
                    border: 2px solid #91c6e1;
                    background: #f1f1f1;
                    padding: 10px 10px 10px 10px;
                    color: #333333;
                }

                table.dataframe tbody {
                    border: 2px solid #91c6e1;
                    padding: 10px 10px 10px 10px;
                }

                table.dataframe tr {

                }

                table.dataframe th {
                    vertical-align: top;
                    font-size: 14px;
                    padding: 10px 10px 10px 10px;
                    color: #105de3;
                    font-family: arial;
                    text-align: center;
                }

                table.dataframe td {
                    text-align: center;
                    padding: 10px 10px 10px 10px;
                }

                body {
                    font-family: 宋体;
                }

                # h1 {
                #     color: #5db446
                # }

                div.header h2 {
                    color: #0002e3;
                    font-family: 黑体;
                }

                div.content h2 {
                    text-align: left;
                    font-size: 28px;
                    # text-shadow: 2px 2px 1px #de4040;
                    color: #fff;
                    font-weight: bold;
                    background-color: #008eb7;
                    # line-height: 1.5;
                    # margin: 20px 0;
                    # box-shadow: 10px 10px 5px #888888;
                    # border-radius: 5px;
                }

                h3 {
                    font-size: 22px;
                    background-color: rgba(0, 2, 227, 0.71);
                    text-shadow: 2px 2px 1px #de4040;
                    color: rgba(239, 241, 234, 0.99);
                    line-height: 1.5;
                }

                h4 {
                    color: #e10092;
                    font-family: 楷体;
                    font-size: 20px;
                    text-align: center;
                }

            </STYLE>
        </head>
        """

    # 构造模板的附件（100）

    message = """
    Hi all,

  Latest bug status for one app, FYI
  All the bugs are tracked with labels = OneApp, any questions please let us know, thanks!"
  """
    body = \
        """
        <body>

        <div align="left" class="header">
            <!--标题部分的信息-->
            <h1 align="left">{}</h1>
        </div>

        <hr>

        <div class="content">
            <!--正文内容-->

            {}
            <p style="text-align: left">
                Any question, please let me know, Thanks!
            </p>
        </div>
        </body>
        """.format(message, df)
    html_msg = "<html>" + head + body + "</html>"
    print(html_msg)
    # 这里是将HTML文件输出，作为测试的时候，查看格式用的，正式脚本中可以注释掉
    fout = open('{}.html'.format(datetimenow), 'w', encoding='UTF-8', newline='')
    fout.write(html_msg)
    fout.close()
    return html_msg


import os


def write_htmls(df_list):
    HEADER = '''
        <html>
            <head>
                <meta charset="UTF-8">
            </head>
            <body>
        '''
    FOOTER = '''
            </body>
        </html>
        '''

    with open(os.path.join(os.getcwd(), 'test.html'), 'w') as f:
        f.write(HEADER)

        print(type(df_list))
        for afaf in df_list:
            print(type(afaf))
            # f.write('<h1><strong>' + '自定义dataframe名' +'</strong></h1>')
            f.write(afaf.to_html(classes='classname'))
        f.write(FOOTER)


if __name__ == "__main__":
    a = jira_search_bug_status()
    b, c = bug_query()

    write_htmls([a,b,c])

    messages = {"Total_bugs": a, "Bug list": b, "Open Bugs": c}
    html_text = generate_df_html(messages)
    print(html_text)
    #
    get_html_msg(html_text)
