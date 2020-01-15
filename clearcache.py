import zeep
import arrow
import requests

import sys


host="mobilefirst"
member_id = 23978752

clear_cache_tool_url = "http://{}.englishtown.com/services/ecplatform/Tools/CacheClear/Clear".format(host)
headers = {'content-type': "application/x-www-form-urlencoded"}

basicinfo_data = {

    'cachetype': 'StudentBasicInfo',
    'paras': member_id

}

member_site_setting_data = {

    'cachetype': 'MemberSiteSettings',
    'paras': {"Member_id":member_id,"SiteArea":""}

}


def clear_cache_for_basicinfo(data):

    response =requests.post(url = clear_cache_tool_url, data=data, headers=headers)
    return response



if __name__ == '__main__':
    clear_cache_for_basicinfo(basicinfo_data)
    clear_cache_for_basicinfo(member_site_setting_data)