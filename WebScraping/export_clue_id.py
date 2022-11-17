import xlrd
import xlwt

from get_all_brand import get_all_brand
from get_all_car import get_all_clue_id

#  1. 先获取所有汽车的品牌
brand_list = get_all_brand()  # 类型是tuple

clue_id_by_brand_list = []

GET_CLUE_ID_MODE = "NEW"  # 获取clue_id的三种模式
FILE_NAME = "clue_id.xls"
# 1: NEW 直接重新获取所有的clue_id, 然后储存在新的文件内
# 2: APPEND 增量模式: 重新再爬取一遍所有的clue_id, 然后添加新的进结果表

for brand_name, value in brand_list:
    clue_id_by_brand_list.extend(get_all_clue_id(value))  # 将所有车辆的clue_id存在里头


clue_id_by_brand_list = list(set(clue_id_by_brand_list))  # 去重


print(clue_id_by_brand_list)

writer = xlwt.Workbook()
workbook = writer.add_sheet("clue_id")

if GET_CLUE_ID_MODE == "NEW":
    for clue_id, index in zip(clue_id_by_brand_list, range(len(clue_id_by_brand_list))):
        workbook.write(index, 0, str(clue_id))
        workbook.write(index, 1, 0)  # 0 代表未读取
    writer.save(FILE_NAME)

if GET_CLUE_ID_MODE == "APPEND":
    reader = xlrd.open_workbook(FILE_NAME)
    table = reader.sheets()[0]
    clue_id_in_file = []
    for i in range(table.nrows):
        clue_id_in_file.append(table.row_values(i)[0])  # 此时得到了文件里的所有clue_id
    clue_id_by_brand_list.extend(clue_id_in_file)
    clue_id_by_brand_list = list(set(clue_id_by_brand_list))  # 去重
    for clue_id, index in zip(clue_id_by_brand_list, range(len(clue_id_by_brand_list))):  # 重新覆盖写入
        workbook.write(index, 0, str(clue_id))
        workbook.write(index, 1, 0)
    writer.save(FILE_NAME)
