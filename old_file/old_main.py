import urllib3
urllib3.disable_warnings()

import csv
import pandas as pd
import requests
import concurrent.futures
import ssl
from tqdm import tqdm
import time

# 从 id_List.csv 文件中使用 utf-8 编码读取 ids
url = 'https://gitee.com/Project0ne/cdn/raw/master/src/id_List.csv'
df = pd.read_csv(url, header=None)
ids = df[0].tolist()

# 定义 CSV 文件的字段名
fieldnames = ["id", "product_id", "caption", "picture", "pictures", "eshop_price", "price", "caption_en", "color_id", "ldd_catalog", "inventory", "ldraw_no","ldd_code", "sale_volume", "rand"]

# 增加 color_data 里面的字段名
color_data_fieldnames = ["main_id","id", "name", "lego_color_id", "font-color", "color", "colorType", "ldraw_color_id", "ldraw_color_value", "index", "name_en"]

# 合并所有的字段名
all_fieldnames = fieldnames + color_data_fieldnames

# 基于当前时间生成文件名
filename = "gobrick_data_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

def fetch_data(id):
    # 要从中获取数据的 URL
    url = f'https://gobricks.cn/frontend/v1/item/filter?product_id={id}&type=2&limit=96&offset=0'

    try:
        # 发送 GET 请求到 URL 并存储响应
        response = requests.get(url, verify=False)
    except requests.exceptions.ProxyError as e:
        print("ProxyError occurred:", e)
        return []

    # 仅提取我们想要写入 CSV 文件的字段
    data = response.json()['rows']
    filtered_data = []
    for d in data:
        # 把 color_data 里面的键值对也加入到 d 里面
        for k, v in d['color_data'].items():
            d[k] = v
        # 把 d 中只包含我们需要的字段的部分保存到 filtered_data 里面
        filtered_data.append({k: v for k, v in d.items() if k in all_fieldnames})
    
    # 更新进度条
    pbar.update(1)
    
    return filtered_data

with concurrent.futures.ThreadPoolExecutor() as executor:
    # 以 utf-8 编码打开 CSV 文件并将数据写入其中
    with open(filename, "a", newline="", encoding="utf-8_sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_fieldnames)
        # 仅在文件为空时写入标题
        if csvfile.tell() == 0:
            writer.writeheader()
        
        # 初始化进度条
        pbar = tqdm(total=len(ids))
        
        # 将请求提交给执行器并将数据写入 CSV 文件
        for data in executor.map(fetch_data, ids):
            for d in data:
                writer.writerow(d)
        
        # 关闭进度条
        pbar.close()