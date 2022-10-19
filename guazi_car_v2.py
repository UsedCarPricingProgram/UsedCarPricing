import json
import time
import requests
import xlwt
from get_token import get_token
#重试请求
#读取数据存入数据库
#更换价格区间
#更换城市

def get_car_list(page):
    """
    :param page: 从0开始，别从1
    :return: clue_id
    """
    session = requests.session()
    query_string = {
        'versionId': '0.0.0.0',
        'sourceFrom': 'wap',
        'osv': 'Windows 10',
        'tag': '-1',
        'priceRange': '0,-1',
        'page': page + 1,
        'pageSize': '20',
        'city_filter': '12',
        'city': '12',
        'guazi_city': '12',
        'platfromSource': 'wap'
    }

    headers = {
        'authority': 'mapi.guazi.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'client-time': '1665747148',
        'client-timestamp': '1665747116',
        'origin': 'https://www.guazi.com',
        'platform': '5',
        'referer': 'https://www.guazi.com/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': '',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    resp = session.get(url="https://mapi.guazi.com/car-source/carList/pcList", params=query_string, headers=headers)
    print(resp.text)
    all_car = resp.json()['data']['postList']
    clue_id = []
    for car in all_car:
        clue_id.append(car['clue_id'])
    return clue_id


def process_data(clueId, index):
    qs = f"ca_n=self&ca_s=self&clueId={clueId}&deviceId=17021fe5-14b3-4c8e-8ba7-f3cdaf5fcae5&fromCrm=0" \
         "&guazi_city=-1&guid=17021fe5-14b3-4c8e-8ba7-f3cdaf5fcae5&osv=ios" \
         "&platfromSource=wap&sourceFrom=wap&userId=&versionId=0.0.0.0"
    url = "https://mapi.guazi.com/car-source/carDetail/detail?" + qs
    client_time = str(int(time.time()))
    payload = {}
    headers = {
        'authority': 'mapi.guazi.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'client-time': client_time,
        'cookie': 'uuid=17021fe5-14b3-4c8e-8ba7-f3cdaf5fcae5; '
                  'cainfo=%7B%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22self%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22guid%22%3A%2217021fe5-14b3-4c8e-8ba7-f3cdaf5fcae5%22%7D; '
                  'sessionid=e35df00a-946c-4a22-a3bb-80f00beff232; '
                  'puuid=308211b1-2d5b-41d6-d7e9-8d72151c5046; '
                  'dsnDataObj=%7B%7D; browsingHistoryCount=1',
        'origin': 'https://m.guazi.com',
        'pragma': 'no-cache',
        'referer': 'https://m.guazi.com/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': '',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'verify-token': get_token(stringify_params=qs, ttt=client_time)
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    res = response.text
    if "security_intercept" in res:
        input("请完成验证码后再继续")
    if response.status_code == 200:
        print(f"{index}: success")
    else:
        print(f"{index}: fail - {res}")
        return ()

    data = json.loads(res)
    title = data['data']['carCommodityInfo']['basicInfo']['titleDesc']  # 标题
    price = data['data']['carCommodityInfo']['carPriceInfo']['styleData']['price']['priceDes']  # 价格

    new_car_price = data['data']['carCommodityInfo']['carPriceInfo']['styleData']['newPrice']['priceDes']  # 新车价格

    reg_date = ""  # 首次上牌
    mileage = ""  # 表显里程
    battery = ""  # 官方续航
    standard = ""  # 排放标准
    gearboxes = ""  # 变速箱
    number_of_transfer = ""  # 过户次数
    car_location = ""  # 车牌地
    car_color = ""  # 车身颜色
    power = ""  # 电动机总功率
    battery_capacity = ""  # 电池容量
    battery_type = ""  # 电池类型
    for each_summary in data['data']['carCommodityInfo']['carRecordInfo']['summary']:
        if each_summary['label'] == "首次上牌":
            reg_date = each_summary['value']
        if each_summary['label'] == "表显里程":
            mileage = each_summary['value']
        if each_summary['label'] == "官方续航":
            battery = each_summary['value']
        if each_summary['label'] == "排放标准":
            standard = each_summary['value']
        if each_summary['label'] == "变速箱":
            gearboxes = each_summary['value']
        if each_summary['label'] == "过户次数":
            number_of_transfer = each_summary['value']
        if each_summary['label'] == "车牌地":
            car_location = each_summary['value']
        if each_summary['label'] == "车身颜色":
            car_color = each_summary['value']

    for each_battery_summary in data['data']['carCommodityInfo']['carRecordInfo'].get("batteryMotorSummary", []):
        if each_battery_summary['label'] == "电动机总功率":
            power = each_battery_summary['value']
        if each_battery_summary['label'] == "电池容量":
            battery_capacity = each_battery_summary['value']
        if each_battery_summary['label'] == "电池类型":
            battery_type = each_battery_summary['value']

    return title, price, new_car_price, reg_date, mileage, battery, standard, gearboxes, number_of_transfer, \
           car_location, car_color, power, battery_capacity, battery_type


clue_id = []
for i in range(80):
    clue_id.extend(get_car_list(i))
city='shenzhen'
wb = xlwt.Workbook()
wb_tmp = xlwt.Workbook()

ws = wb.add_sheet('A Test Sheet')
ws_tmp = wb_tmp.add_sheet("Test")
sheet_titles = ["标题", "价格", "新车价格", "首次上牌", "表显里程", "官方续航", "排放标准",
                "变速箱", "过户次数", "车牌地", "车身颜色", "电动机总功率", "电池容量", "电池类型"]

for index in range(len(sheet_titles)):
    ws.write(0, index, sheet_titles[index])

start_time = time.time()
pause_num = 100
for index in range(len(clue_id)):
        try:
            res = process_data(clue_id[index], index)
            print(f"{index} write: {res[0]}")
            for y in range(len(res)):
                ws.write(index + 1, y, res[y])
                ws_tmp.write(index + 1, y, res[y])
            if index != 0 and index % pause_num == 0:
                wb_tmp.save(f"{time.time()}_tmp_{pause_num}.xls")
                wb_tmp = xlwt.Workbook()
                ws_tmp = wb_tmp.add_sheet("Test")
        except Exception:
            print(f"{index} - happened some error! skip it")
            continue
        file_name = f"{time.time()}_{city}_result_{pause_num}_{index}.xls"
        wb.save("/Users/apple/Desktop/pa_try/data/{}".format(file_name))
print(f"END Save as total: {len(clue_id)}, cost time {time.time() - start_time}s")

