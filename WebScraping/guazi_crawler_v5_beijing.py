import json
import sys
import time
import requests
import xlwt
import xlrd
from tqdm import tqdm
from get_token import get_verify_token


#首页买车获取所有的品牌
def get_all_brand():
    """
    :return: brand list
    """
    session = requests.session()
    current_timestamp = str(int(time.time()))
    query_string = "deviceId=09975a47-9aad-4639-befb-fc0e79c9d69b" \
                   "&osv=IOS" \
                   "&platfromSource=wap" \
                   "&sourceFrom=wap" \
                   "&versionId=0.0.0.0" \
                   "platfromSource=wap"

    headers = {
        'authority': 'mapi.guazi.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'anti-token': '1277105907',
        'client-time': current_timestamp,
        'client-timestamp': current_timestamp,
        'cookie': 'uuid=09975a47-9aad-4639-befb-fc0e79c9d69b; sessionid=cadff7d8-c15d-47ba-d2cb-41c21e166902; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22-%22%7D; cainfo=%7B%22ca_s%22%3A%22seo_google%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22guid%22%3A%2209975a47-9aad-4639-befb-fc0e79c9d69b%22%7D; puuid=2e3efc56-46f9-4475-cbd7-7c082fecbc33; user_city_id=17; dsnDataObj=%7B%7D; browsingHistoryCount=1; cityDomain=sz',
        'origin': 'https://www.guazi.com',
        'referer': 'https://www.guazi.com/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'szlm-id': 'D2jYeXZROy6gVzy7SoqbY4EQKTZvoK7VzoFS/Ih5ioO8wX44',
        'token': '',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'verify-token': get_verify_token(query_string, current_timestamp)
    }

    resp = session.get(url=f'https://mapi.guazi.com/car-source/option/list?{query_string}', params=query_string, headers=headers)
    if resp.status_code != 200:
        return [("全部", "")]  # http返回码不为200, 则代表获取品牌失败, 直接返回空

    try:
        data = resp.json()['data'][1]['filterValue']['common']
    except TypeError:
        return [("全部", "")]  # 解析失败, 未避免主流程无法跑通
    except Exception:
        return [("", "")]

    filter_list = []
    for key in data.keys():
        for each in data[key]:
            filter_list.append((each['name'], each['value']))
    print(f"{time.time()} 所有品牌获取成功, 共计{len(filter_list)}条结果: {filter_list}")
    return filter_list

#遍历brand获取不同品牌下80页所有车的clue_id
def get_car_list(current_page: int, brand: str) -> []:
    """
    :param current_page: 当前页数
    :param brand: 汽车品牌
    :return: clue_id: 当前页面所有汽车的所有唯一clue_id
    :return: total_page: 当前页面的最大页面数
    """
    session = requests.session()
    current_timestamp = str(int(time.time()))
    query_string = {
        'versionId': '0.0.0.0',
        'sourceFrom': 'wap',
        'osv': 'Windows 10',
        'tag': '-1',
        'priceRange': '0,-1',
        'page': current_page + 1,
        'pageSize': '20',
        'city_filter': '12',
        'city': '12',
        'guazi_city': '12',
        'platfromSource': 'wap',
        "minor": brand
    }

    headers = {
        'authority': 'mapi.guazi.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'anti-token': '1277105907',
        'client-time': current_timestamp,
        'client-timestamp': current_timestamp,
        'cookie': 'uuid=09975a47-9aad-4639-befb-fc0e79c9d69b; sessionid=cadff7d8-c15d-47ba-d2cb-41c21e166902; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22-%22%7D; cainfo=%7B%22ca_s%22%3A%22seo_google%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22guid%22%3A%2209975a47-9aad-4639-befb-fc0e79c9d69b%22%7D; puuid=2e3efc56-46f9-4475-cbd7-7c082fecbc33; user_city_id=17; dsnDataObj=%7B%7D; browsingHistoryCount=1; cityDomain=sz',
        'origin': 'https://www.guazi.com',
        'platform': '5',
        'referer': 'https://www.guazi.com/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'szlm-id': 'D2jYeXZROy6gVzy7SoqbY4EQKTZvoK7VzoFS/Ih5ioO8wX44',
        'token': '',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    # 用于控制失败次数
    the_number_of_failure = 0
    clue_id = []
    while the_number_of_failure < 3:
        try:
            resp = session.get(url="https://mapi.guazi.com/car-source/carList/pcList", params=query_string, headers=headers)
            res = resp.text
            if "security_intercept" in res:
                input("请完成验证码后再继续")

            if resp.status_code != 200:
                the_number_of_failure += 1  # 请求返回码不为200, 该请求失败直接跳过后面的内容解析, 进行重试
                pass

            if resp.status_code == 599:
                return [], -2

            all_car = resp.json()['data']['postList']
            print(f"{time.time()} 获取品牌{brand}的第{current_page}页所有club_id成功: {all_car}")
            total_page = resp.json()['data']['totalPage']
            for car in all_car:
                clue_id.append(car['clue_id'])
            return clue_id, total_page
        except Exception:
            print(f"{time.time()} 获取品牌{brand}的第{current_page}页所有club_id失败, 第{the_number_of_failure}次重试")
            the_number_of_failure += 1
            pass
    # 直接返回空
    print(f"{time.time()} 获取品牌{brand}的第{current_page}页所有club_id失败, 耗尽所有重试次数! 返回空")
    return [], -1

def get_all_clue_id(brand: str, total_page=80) -> []:
    """
    :param brand: 汽车品牌
    :param total_page: 所有的页数
    :return: clue_id 所有的clue_id
    """
    clue_id = []
    current_page = 0
    while current_page < total_page:
        temp_clue_id, temp_total_page = get_car_list(current_page, brand)
        if temp_total_page == -2:
            print(f"{time.time()} - ip被锁定, 直接跳过")
            break
        if temp_total_page != -1 and temp_total_page != total_page:
            print(f"{time.time()} - 更新最新页数, 更新前{total_page}, 更新后{temp_total_page}")
            total_page = temp_total_page
        clue_id.extend(temp_clue_id)
        current_page += 1
    return clue_id


def get_car_details_by_clueid(clueId) -> ():
    current_timestamp = str(int(time.time()))
    query_string = f"ca_n=self" \
                   f"&ca_s=self" \
                   f"&clueId={clueId}" \
                   f"&deviceId=17021fe5-14b3-4c8e-8ba7-f3cdaf5fcae5" \
                   f"&fromCrm=0" \
                   f"&guazi_city=-1" \
                   f"&guid=17021fe5-14b3-4c8e-8ba7-f3cdaf5fcae5" \
                   f"&osv=ios" \
                   f"&platfromSource=wap" \
                   f"&sourceFrom=wap" \
                   f"&userId=" \
                   f"&versionId=0.0.0.0"

    headers = {
        'authority': 'mapi.guazi.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'client-time': current_timestamp,
        'cookie': 'uuid=09975a47-9aad-4639-befb-fc0e79c9d69b; sessionid=cadff7d8-c15d-47ba-d2cb-41c21e166902; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22-%22%7D; cainfo=%7B%22ca_s%22%3A%22seo_google%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22guid%22%3A%2209975a47-9aad-4639-befb-fc0e79c9d69b%22%7D; puuid=2e3efc56-46f9-4475-cbd7-7c082fecbc33; user_city_id=17; dsnDataObj=%7B%7D; cityDomain=sz; browsingHistoryCount=2',
        'origin': 'https://m.guazi.com',
        'referer': 'https://m.guazi.com/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': '',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'verify-token': get_verify_token(query_string, current_timestamp)
    }
    the_number_of_failure = 0  # 用于控制失败次数
    MAX_RETRY =3
    while the_number_of_failure < MAX_RETRY:
        try:
            session = requests.session()
            response = session.get(url=f'https://mapi.guazi.com/car-source/carDetail/detail?{query_string}',
                                   headers=headers, timeout=10, proxies={})
            res = response.text

            if "security_intercept" in res:
                input("请完成验证码后再继续")
            if response.status_code != 200:
                the_number_of_failure += 1  # 请求返回码不为200, 该请求失败直接跳过后面的内容解析, 进行重试
                pass
            if response.status_code == 599:
                return None
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
            result_to_user= (title, price, new_car_price, reg_date, mileage, battery, standard, gearboxes,
                                  number_of_transfer, car_location, car_color, power, battery_capacity, battery_type)
            return result_to_user
        except Exception:
            the_number_of_failure += 1
            print(f"{time.time()} 获取车辆详细信息失败, clue_id {clueId}: 进行第{the_number_of_failure}次重试")
            pass
    print(f"{time.time()} 获取车辆详细信息失败, clue_id {clueId}: 重试次数达到上限, 跳过!")
    return ()  # 达到重试上限仍然失败, 直接返回空


def get_car_more_details(clueId) -> ():
    current_timestamp = str(int(time.time()))
    query_string = f"clueId={clueId}" \
                   f"&deviceId=17021fe5-14b3-4c8e-8ba7-f3cdaf5fcae5" \
                   f"&deviceid=17021fe5-14b3-4c8e-8ba7-f3cdaf5fcae5" \
                   f"&guazi_city=-1" \
                   f"&guid=17021fe5-14b3-4c8e-8ba7-f3cdaf5fcae5&osv=ios" \
                   f"&platfromSource=wap" \
                   f"&sourceFrom=wap" \
                   f"&userId=" \
                   f"&versionId=0.0.0.0"

    headers = {
        'authority': 'mapi.guazi.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'client-time': current_timestamp,
        'cookie': 'uuid=09975a47-9aad-4639-befb-fc0e79c9d69b; sessionid=cadff7d8-c15d-47ba-d2cb-41c21e166902; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22-%22%7D; cainfo=%7B%22ca_s%22%3A%22seo_google%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22guid%22%3A%2209975a47-9aad-4639-befb-fc0e79c9d69b%22%7D; puuid=2e3efc56-46f9-4475-cbd7-7c082fecbc33; user_city_id=17; dsnDataObj=%7B%7D; cityDomain=sz; browsingHistoryCount=2',
        'origin': 'https://m.guazi.com',
        'referer': 'https://m.guazi.com/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': '',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'verify-token': get_verify_token(query_string, current_timestamp)
    }
    the_number_of_failure = 0  # 用于控制失败次数
    MAX_RETRY = 3
    while the_number_of_failure < MAX_RETRY:
        try:
            session = requests.session()
            response = session.get(url=f'https://mapi.guazi.com/car-source/carRecord/carInfo?{query_string}',
                                   headers=headers, timeout=10, proxies={})
            res = response.text
            if "security_intercept" in res:
                input("请完成验证码后再继续")
            if response.status_code != 200:
                the_number_of_failure += 1  # 请求返回码不为200, 该请求失败直接跳过后面的内容解析, 进行重试
                pass
            if response.status_code == 599:
                return None
            data = json.loads(res)
            energy_type = ""  # 能源类型
            displace = ""  # 排量
            key_num = ""  # 钥匙数
            for each in data['data']['configurationSummary']:
                if each['label'] == "能源类型":
                    energy_type = each['value']
                if each['label'] == "钥匙数":
                    key_num = each['value']
                if each['label'] == "排量":
                    displace = each['value']
            result_to_user = (energy_type, displace, key_num)
            return result_to_user
        except Exception:
            the_number_of_failure += 1
            print(f"{time.time()} 获取车辆详细信息失败, clue_id {clueId}: 进行第{the_number_of_failure}次重试")
            pass
    print(f"{time.time()} 获取车辆详细信息失败, clue_id {clueId}: 重试次数达到上限, 跳过!")
    return ()  # 达到重试上限仍然失败, 直接返回空


if __name__ == '__main__':
    file_name = "../data/clue_id_all_shenzhen.xls"

    # read clue_id
    reader = xlrd.open_workbook(file_name)
    table = reader.sheets()[0]
    clue_id_list = []
    for i in range(table.nrows):
        row_value = table.row_values(i)
        clue_id_list.append(row_value)  # 此时得到了文件里的所有clue_id


    details_writer = xlwt.Workbook()  # 车辆详细数据
    clue_id_data_writer = xlwt.Workbook()  # clue_id读取
    details_worksheet = details_writer.add_sheet("all_details")
    clue_id_data_worksheet = clue_id_data_writer.add_sheet("clue_id", cell_overwrite_ok=True)

    sheet_titles = ["标题", "价格", "新车价格", "首次上牌", "表显里程", "官方续航", "排放标准", "变速箱", "过户次数", "车牌地",
                    "车身颜色", "电动机总功率", "电池容量", "电池类型", "能源类型", "排量", "钥匙数"]

    #  表头先加上
    for index in range(len(sheet_titles)):
        details_worksheet.write(0, index, sheet_titles[index])

    success_counter_a = 0
    success_counter_b = 0

    for each_clue_id, index in tqdm(zip(clue_id_list, range(len(clue_id_list))), file=sys.stdout):
        time.sleep(1.5)
        print(f"{time.time()} 正在读取clue_id: {each_clue_id[0]}")
        result = 0
        if int(each_clue_id[1]) == 2 or int(each_clue_id[1]) == 0:
            print(f"{time.time()} 当前club_id {each_clue_id[0]} 需要获取详细信息, 正在获取")
            res = get_car_details_by_clueid(each_clue_id[0])
            if res is None:
                print(f"{time.time()} 锁ip 直接结束")
                break
            if len(res) != 0:  # 说明有结果, 成功
                result += 1
                print(f"{time.time()} 当前club_id {each_clue_id[0]} 成功: {res}")
                clue_id_data_worksheet.write(index, 0, str(each_clue_id[0]))
                clue_id_data_worksheet.write(index, 1, result)
                for y in range(len(res)):
                    details_worksheet.write(index + 1, y, res[y])
                success_counter_a += 1
            else:
                clue_id_data_worksheet.write(index, 0, str(each_clue_id[0]))
                clue_id_data_worksheet.write(index, 1, result)
        if int(each_clue_id[1]) == 1 or int(each_clue_id[1]) == 0:  # 不为3就需要去爬全量
            print(f"{time.time()} 当前club_id {each_clue_id[0]} 需要获取更多详细信息, 正在获取")
            res = get_car_more_details(each_clue_id[0])
            if res is None:
                print(f"{time.time()} 锁ip 直接结束")
                break
            if len(res) != 0:  # 说明有结果, 成功
                result += 2
                print(f"{time.time()} 当前club_id {each_clue_id[0]} 成功: {res}")
                clue_id_data_worksheet.write(index, 0, str(each_clue_id[0]))
                clue_id_data_worksheet.write(index, 1, result)
                for y in range(len(res)):
                    details_worksheet.write(index + 1, y + 14, res[y])
                success_counter_b += 1
            else:
                clue_id_data_worksheet.write(index, 0, str(each_clue_id[0]))
                clue_id_data_worksheet.write(index, 1, result)
        if int(each_clue_id[1]) == 3:
            clue_id_data_worksheet.write(index, 0, str(each_clue_id[0]))
            clue_id_data_worksheet.write(index, 1, 3)
            print(f"{time.time()} 当前club_id {each_clue_id[0]} 无需获取详细信息, 已跳过")

    details_writer.save(f"{int(time.time())}_TOTAL_RESULT_{success_counter_a}_{success_counter_b}.xls")
    clue_id_data_writer.save(f"{time.time()}_{file_name}")

