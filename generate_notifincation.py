import arrow
import requests
import zeep

host = "www"
member_id = "35043397"

wsdl = 'http://{}.englishtown.cn/services/ecplatform/StudyPlanService.svc?wsdl'.format(host)
# client = zeep.Client(wsdl=wsdl, wsse=UsernameToken('SalesforceSmartUser', 'SalesforceSmartPwd'))
client = zeep.Client(wsdl=wsdl)

current_time = arrow.now()
lastmonth = current_time.shift(months=-1)
year = lastmonth.year
month = lastmonth.month


import datetime


def join_group():
    client.service.JoinGroup(studentId=member_id)


def generate_monthly_report():
    client.service.UpdateMonthlyKeywordCount(studentId=member_id, cultureCode='zh-CN',
                                             year=year,
                                             month=month, forceSendNotification=True)


def generate_weekly_study_goal_reminder():
    client.service.SendWeeklyStudyGoalReminder(studentId=member_id, cultureCode='zh-CN', forceSend=True)


def generate_this_week_study_status():
    client.service.SendThisWeekStudyStatus(studentId=member_id, cultureCode='zh-CN', forceSend=True)


def engage_inactive_check():
    check_url = "http://{}.englishtown.com/services/ecsystem/task/studyplan/EngageInactiveCheck".format(host)
    headers = {'content-type': "application/x-www-form-urlencoded"}

    basic_data = {

        "timezone_id": 1,
        "partnercodes": "cool,mini",
        "notActiveDays": 30,
        "cultureCode": "zh-cn"

    }

    response = requests.post(url=check_url, data=basic_data, headers=headers)
    return response


if __name__ == '__main__':
    #generate_monthly_report()
    #generate_weekly_study_goal_reminder()
    # import os
    # os.system('say "Someone has sent red bag" ')
    generate_this_week_study_status()
    # engage_inactive_check()
    # import tkinter.messagebox
    #
    # tkinter.messagebox.showinfo('重要提醒', '有人发红包啦！')