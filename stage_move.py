import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

ENV = input("please input env: uat,qa,staging \n")
member_id = input("please input memberid \n")
level = input("please input current level \n")
# " we can use this case to test: qa,11446478,6"

option = webdriver.ChromeOptions()

option.add_argument('disable-infobars')
# option.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=option)
Max_Time_Out = 30
Time_Out = 10
Mini_Time_Out = 3


def current_host(env):
    envs = {
        "uat": "smartuat2.englishtown.com",
        "qa": "qaoboe.ef.com",
        "staging": "staging.ef.com"
    }
    return envs[env]


def get_move_on_stage(current_level):
    stage_list = [1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15, 16]
    stage = (stage_list)

    move_on_index = [i + 1 + 1 for i in range(len(stage)) if current_level in stage[i]]
    print("current level is: {}, and will move on stage is: {}".format(current_level, move_on_index[0]))
    return move_on_index[0]


class change_stage():
    def __init__(self):
        self.host = "qaoboe"
        self.user_name_btn = "i0116"
        self.user_pwd_btn = "i0118"
        self.next_btn = "idSIButton9"
        self.user_name = "qa.testauto@ef.com"
        self.user_password = "test@456"
        self.member_id = member_id
        self.target_stage = get_move_on_stage(int(level))
        self.home_url = "https://{}/oboe2/home".format(current_host(ENV))
        self.check_url = "https://{}/oboe2/Smart/StageChange/ChangeStage".format(current_host(ENV))

    def open_url(self):
        url = self.home_url
        driver.set_page_load_timeout(Max_Time_Out)
        try:
            driver.get(url)
        except TimeoutError:
            print("cannot open the page for {} seconds".format(Max_Time_Out))
            driver.execute_script('window.stop()')

    def find_element(self, obj):
        WebDriverWait(driver, Time_Out).until(EC.visibility_of_element_located((By.ID, obj)))
        element = WebDriverWait(driver, Time_Out).until(lambda x: driver.find_element(By.ID, obj))
        return element

    def type(self, obj, value):
        self.find_element(obj).clear()
        self.find_element(obj).send_keys(value)

    def clickat(self, obj):
        WebDriverWait(driver, Time_Out).until(EC.element_to_be_clickable((By.ID, obj)))
        self.find_element(obj).click()

    def select_at(self, father, type, child):

        s = driver.find_element_by_id(father)

        if type == "value":
            Select(s).select_by_value(child)
        elif type == "index":
            Select(s).select_by_value(child)
        else:
            print("select by text")
            Select(s).select_by_visible_text(child)

    def login(self):
        self.open_url()

        self.type(self.user_name_btn, self.user_name)

        self.clickat(self.next_btn)

        self.type(self.user_pwd_btn, self.user_password)

        self.clickat(self.next_btn)

        self.clickat(self.next_btn)

        cookies = driver.get_cookies()

        home_cookies = ""
        for cookie in cookies:
            print(cookie)

            if cookie['name'] == ".AspNet.Cookies" and cookie['domain'] in driver.current_url:
                print("find")
                print(cookie['name'])
                print(cookie['value'])
                home_cookies = cookie['name'] + "=" + cookie['value']
                break

        driver.quit()
        return home_cookies

    def move_stage(self, cookies):

        headers = {'content-type': "application/x-www-form-urlencoded",
                   'Cookie': cookies
                   }

        basic_data = {

            "studentId": self.member_id,
            "stageId": self.target_stage,
            "grade": 90
        }
        s = requests.session()
        s.verify = False

        response = s.post(url=self.check_url, data=basic_data, headers=headers)
        print(response.content)
        if (response.json()["IsSuccess"]):
            print("success!")
        else:
            print("fail, please check!")


if __name__ == '__main__':
    t = change_stage()
    t.open_url()
    cookie = t.login()
    t.move_stage(cookie)
