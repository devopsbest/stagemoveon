import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd

case_list = []

tree = ET.parse("/Users/Anderson/Downloads/OneApp_Android.xml")
root = tree.getroot()

for t in root.findall("testcase"):
    # print(t.attrib["external_id"])
    case_list.append(t.attrib["external_id"])


# print(case_list)
# print(len(case_list))

import testlink

def get_case_detail(id):

    # 连接test link
    url = "http://town.cn/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
    key = "eb82178aa328c2334f2c1a2d5c74ff3f"
    tlc = testlink.TestlinkAPIClient(url, key)

    print(tlc)

    # test_case_id = "ET-81899"
    # test_case_id = "ET-83077"
    # test_case_id = "ET-82123"
    test_case = tlc.getTestCase(None, testcaseexternalid=id)
    # print(test_case)
    # print(test_case[0].get("summary"))
    # print(test_case[0].get("name"))
    # print(test_case[0].get("steps"))

    return id, test_case[0]["name"],test_case[0]["summary"],test_case[0]["steps"]


def put_result():
    df = pd.read_excel('/Users/anderson/Downloads/output.xlsx')
    data = df[["id","result"]]
    mydata = data.head(5)
    print(mydata)


# def update_testlink():
    tree = ET.parse("/Users/Anderson/Downloads/OneApp_Android.xml")
    root = tree.getroot()

    # for t in root.findall("testcase"):
    #     # print(t.attrib["external_id"])
    #     case_list.append(t.attrib["external_id"])
    # Element.set('AttributeName', 'AttributeValue')
    for ix, row in mydata.iterrows() and t in root.iterfind("testcase/external_id"):
        print(t)
        if row['id'] == t.attrib:
            t.set('result', data(row['result']))
            t.set('tester', '')
            t.set('timestamp', '')



def main():

    # for x in case_list:
    #     result = get_case_detail(x)
    #     print(result)

    get_case = (get_case_detail(x) for x in case_list)
    case_pd = pd.DataFrame(get_case, columns=["id","name","summary","steps"])
    case_pd["result"] =""

    case_pd.to_csv("/Users/Anderson/Downloads/case.csv")



    # with pd.ExcelWriter('output.xlsx') as writer:
    #     case_pd.to_excel(writer, sheet_name='Sheet_name_1')

    #result =
    # get_case = (get_case_detail(x) for x in case_list)
    # case_np = np.array(list(get_case)).reshape(len(case_list), 4)
    #
    # case_pd = pd.DataFrame(case_np, columns=["id","name","summary","steps","result"])
    # print(case_pd)

if __name__ == "__main__":
    put_result()

# for i in test_case:
#     print("序列", "执行步骤", "预期结果")
#     for m in i.get("steps"):
#         print(m.get("step_number"), m.get("actions"), m.get("expected_results"))
