
from tqdm import tqdm
import pymysql
import xlrd
from xlrd import xldate_as_datetime

def append_value_insert_sql(each_details, sheet):
    value = None
    if sheet == 0:
        value = f"( {each_details[0]}, '{each_details[1]}', {each_details[2]}, {each_details[3]}, " \
                f"'{xldate_as_datetime(each_details[4], 0)}', {each_details[5]}, '{each_details[6]}', " \
                f"{each_details[7]}, {each_details[8]}, {each_details[9]}, {each_details[10]}, {each_details[11]}, " \
                f"{each_details[12]}, {each_details[13]}, '{each_details[14]}', {each_details[15]}, {each_details[16]}, " \
                f"{each_details[17]}, {each_details[18]}, {each_details[19]}, {each_details[20]}), "
    if sheet == 1:
        value = f"( {each_details[0]}, '{each_details[1]}', {each_details[2]}, {each_details[3]}, " \
                f"'{xldate_as_datetime(each_details[4], 0)}', {each_details[5]}, {each_details[6]}, " \
                f"'{each_details[7]}', {each_details[8]}, {each_details[9]}, {each_details[10]}, {each_details[11]}, " \
                f"{each_details[12]}, {each_details[13]}, '{each_details[14]}', {each_details[15]}, {each_details[16]}, " \
                f"'{each_details[17]}', {each_details[18]}, {each_details[19]}, {each_details[20]}, " \
                f"{each_details[21]}, {each_details[22]}, {each_details[23]}), "
    if sheet == 2:
        battery_type = ("'" + each_details[14] + "'") if each_details[14] != "" else "null"
        value = f"( {each_details[0]}, '{each_details[1]}', {each_details[2]}, {each_details[3]}, " \
                f"'{xldate_as_datetime(each_details[4], 0)}', {each_details[5]}, " \
                f"{each_details[6] if each_details[6] != '' else 'null'}, " \
                f"'{each_details[7]}', {each_details[8]}, {each_details[9]}, {each_details[10]}, {each_details[11]}, " \
                f"{each_details[12] if each_details[12] != '' else 'null'}, " \
                f"{each_details[13] if each_details[13] != '' else 'null'}, " \
                f"{battery_type}, {each_details[15]}, {each_details[16] if each_details[16] != '' else 'null'}, " \
                f"{each_details[17]}, '{each_details[18]}', {each_details[19]}, {each_details[20]}, " \
                f"{each_details[21]}, {each_details[22]}, {each_details[23]}, {each_details[24]}), "
    return value


db = pymysql.connect(host='gz-cynosdbmysql-grp-52kxr8wn.sql.tencentcdb.com',
                     port=23783, user='root', passwd='Zz@123456',
                     db='guazi_car', charset='utf8mb4')
cursor = db.cursor()

prefix_sql = "INSERT INTO %s VALUES "


reader = xlrd.open_workbook("cleaned_car_all.xlsx")
sheet = ["petrol", "electric", "mixed"]
sql_list = []
for each, index in zip(sheet, range(len(sheet))):
    table = reader.sheets()[index]
    car_details_list = []
    for i in range(table.nrows):
        row_value = table.row_values(i)
        car_details_list.append(row_value)

    car_details_list = [car_details_list[i: i + 10] for i in range(1, len(car_details_list), 10)]
    for details in car_details_list:
        sql = ""
        for detail in details:
            each_sql = append_value_insert_sql(detail, index)
            if each_sql is not None:
                sql += each_sql
        sql_list.append((prefix_sql % each) + sql[:-2] + ";")

for sql in tqdm(sql_list):
    try:
        # 执行sql语句
        print(sql)
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
        # 如果发生错误则回滚
        db.rollback()
        db.close()
        exit()
