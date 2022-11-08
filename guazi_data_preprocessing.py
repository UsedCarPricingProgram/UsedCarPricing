import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

'''
修改程序前后两个读取/写入文件的路径，就可以在任何电脑运行。
本程序读取爬虫抓取的原始-瓜子二手车直卖网-数据
清洗包括：置换表头、去掉数据单位、将str类型转为float64或int64类型
'''

# raw_data是从原表读到的原始数据
raw_data = pd.read_excel(os.path.join(os.getcwd(),'data/car_all.xls'))
raw_data = raw_data.rename(columns={
    '标题':'title',
    '价格':'price',
    '新车价格':'price_new',
    '首次上牌':'date_regi',
    '表显里程':'mileage', 
    '官方续航':'official_endurance',
    '排放标准':'standard',
    '变速箱':'gearbox',
    '过户次数':'num_trans',
    '车牌地':'license_location',
    '车身颜色':'color',
    '电动机总功率':'motor_power',
    '电池容量':'battery_capacity',
    '电池类型':'battery_type',
    '能源类型':'energy_type',
    '排量':'displacement',
    '钥匙数':'keys'
    })

clean_data = raw_data.copy()
# title列拆c出brand
clean_data['brand'] = clean_data['title'].str.split(' ',expand=True)[0]
# 去掉单位
clean_data['mileage'] = clean_data['mileage'].str.replace('万公里','').apply(lambda x :float(x.replace('公里',''))/10000 if '公里' in str(x) else x).astype(np.float64)
clean_data['official_endurance'] = clean_data['official_endurance'].str.replace('km','').replace('-',np.nan).astype(np.float64)
clean_data['num_trans'] = clean_data['num_trans'].str.replace('次','').replace('-',np.nan).astype(np.float64)
clean_data['battery_capacity'] = clean_data['battery_capacity'].str.replace('kWh','').replace('-',np.nan).astype(np.float64)
clean_data['motor_power'] = clean_data['motor_power'].str.replace('kw','').replace('-',np.nan).astype(np.float64)
clean_data['keys'] = clean_data['keys'].str.replace('把','').astype(np.float64)

# location 一线城市（北上广深）为1，其他城市为0
clean_data['license_location'] = clean_data['license_location'].str.split('[(（]',expand=True)[0]
clean_data['license_location'] = clean_data['license_location'].apply(lambda x : 1 if x in ['上海','北京','广州','深圳'] else 0).astype(np.float64)

# color 黑色、白色、深灰色、银灰色为0，其他颜色为1
clean_data['color'] = clean_data['color'].apply(lambda x : 0 if x in ['白色','黑色','深灰色','银灰色'] else 1).astype(np.float64)

# displace：T*1.4变成L，方便分析，排放越大性能越好
clean_data['displacement'] = clean_data['displacement'].astype(str).apply(lambda x : float(x.replace('T',''))*1.4 if 'T' in x else float(x.replace('L',''))).astype(np.float64)

# 能源类型:汽油0，电动1，混合2
energy_type = list(clean_data['energy_type'].dropna().unique())
type_num = [2,0,1,2,2,2,2,0,2,2]
energy_type_num=dict(zip(energy_type,type_num))
clean_data['energy_type'] = clean_data['energy_type'].map(energy_type_num)

# 变速箱：手动0，自动1
clean_data['gearbox'] = clean_data['gearbox'].apply(lambda x : 1 if str(x)=='自动' else 0)

# 写入新文件
clean_data.to_excel(os.path.join(os.getcwd(),'data/cleaned_car_all.xlsx'),encoding='utf-8')