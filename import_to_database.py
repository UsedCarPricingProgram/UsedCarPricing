from datetime import datetime
from tqdm import tqdm
import pymysql
import xlrd

#数据类型处理，公里数转化为float
def deal_with_mileage(mileage: str):
    mileage = mileage.split("公里")[0]
    actual = mileage.split("万")
    if len(actual) == 1:
        return float(actual[0])
    else:
        return float(actual[0]) * 10000

def deal_with_mileage(mileage: str):
    mileage = mileage.split("公里")[0]
    actual = mileage.split("万")
    if len(actual) == 1:
        return float(actual[0])
    else:
        return float(actual[0]) * 10000


def append_value_insert_sql(each_details):
    car_title = each_details[0]  # 标题
    if car_title == "":
        return None
    car_price = float(each_details[1])  # 价格
    new_car_price = float(each_details[2])  # 新车价格
    first_register_date = datetime.strptime(each_details[3], "%Y-%m")
    mileage = deal_with_mileage(each_details[4])  # 表显里程
    electric_vehicle_range = int(each_details[5][:-2]) if each_details[5][:-2] != "" else None  # 官方续航
    emission_standards = each_details[6]  # 排放标准
    transmission = each_details[7]  # 变速箱
    number_of_transfers = int(each_details[8][:-1])  # 过户次数
    license_plate_place = each_details[9]  # 车牌地
    color = each_details[10]  # 车身颜色
    total_motor_power = float(each_details[11][:-2]) if each_details[11][:-2] != "" else None  # 电机总功率
    battery_capacity = int(each_details[12][:-3]) if each_details[12][:-3] != "" else None  # 电池容量
    battery_type = each_details[13] if each_details[13] != "" else None  # 电池类型
    energy_type = each_details[14] if each_details[14] != "" else None # 能源类型
    displace = each_details[15] if each_details[15] != "" else None # 排量
    key_num = int(each_details[16][:-1]) if each_details[16][:-1] != "" else None # 排量 # 钥匙数量

    value = f"('{car_title}', {car_price}, {new_car_price}, '{first_register_date}', {mileage}," \
            f" {electric_vehicle_range if electric_vehicle_range is not None else 'null'}, '{emission_standards}', " \
            f"'{transmission}', {number_of_transfers}, '{license_plate_place}', '{color}'," \
            f"{total_motor_power if total_motor_power is not None else 'null'}, " \
            f"{battery_capacity if battery_capacity is not None else 'null'}, " \
            + (("'" + battery_type + "'") if battery_type is not None else "null") + ", " \
            + (("'" + energy_type + "'") if energy_type is not None else "null") + ", " \
            + (("'" + displace + "'") if displace is not None else "null") + ", " \
            f"{key_num if key_num is not None else 'null'} ), "
    return value


db = pymysql.connect(host='gz-cynosdbmysql-grp-52kxr8wn.sql.tencentcdb.com',
                     port=23783, user='root', passwd='Zz@123456',
                     db='guazi_car', charset='utf8mb4')
cursor = db.cursor()

prefix_sql = """INSERT INTO car_details_v2(car_title, car_price, new_car_price, first_register_date, mileage,
                electric_vehicle_range, emission_standards, transmission, number_of_transfers, license_plate_place, 
                color, total_motor_power, battery_capacity, battery_type,energy_type,displace,key_num)
                VALUES """

reader = xlrd.open_workbook("/UsedCarPricing/data/car_all.xls")
table = reader.sheets()[0]

car_details_list = []
sql_list = []
for i in range(table.nrows):
# for i in range(1, 3):
    row_value = table.row_values(i)
    car_details_list.append(row_value)

car_details_list = [car_details_list[i: i + 10] for i in range(1, len(car_details_list), 10)]
for details in car_details_list:
    sql = ""
    for detail in details:
        each_sql = append_value_insert_sql(detail)
        if each_sql is not None:
            sql += each_sql
    sql_list.append(sql[:-2] + ";")

for sql in tqdm(sql_list):
    try:
        # 执行sql语句
        final_sql = prefix_sql + sql
        cursor.execute(final_sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
# 关闭数据库连接
db.close()
