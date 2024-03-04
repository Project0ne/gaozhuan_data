import urllib3
urllib3.disable_warnings()
import base64
import csv
import pandas as pd
import requests
import concurrent.futures
import ssl
from tqdm import tqdm
import time

# 从 item_List.csv 文件中使用 utf-8 编码读取 ids
url = 'aHR0cHM6Ly9naXRlZS5jb20vUHJvamVjdDBuZS9jZG4vcmF3L21hc3Rlci9zcmMvaXRlbV9MaXN0LmNzdg=='
bytes_url = base64.urlsafe_b64decode(url)
str_url = bytes_url.decode('utf-8')
df = pd.read_csv(str_url, header=None)
ids = df[0].tolist()

# 定义 CSV 文件的字段名
fieldnames =["alias", "caption", "caption_en", "picture", "inventory", "price", "designid", "lego_color_id", "ldraw_no", "product_weight", "ldd_catalog", "ldd_code"]

# 基于当前时间生成文件名
filename = "gobrick_detail._" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

def fetch_data(id):
    # 要从中获取数据的 URL
    url = f'https://gobricks.cn/frontend/v1/item/detail?id={id}'

    try:
        # 发送 GET 请求到 URL 并存储响应
        response = requests.get(url, verify=False)
    except requests.exceptions.ProxyError as e:
        print("ProxyError occurred:", e)
        return None

    # 解析响应数据
    data = response.json()

    # 创建一个字典，包含你需要的字段
    result = {
        "alias": data.get("alias"),
        "caption": data.get("caption"),
        "caption_en": data.get("caption_en"),
        "picture": data.get("picture"),
        "inventory": data.get("inventory"),
        "price": data.get("price"),
        "designid": data.get("designid"),
        "lego_color_id": data.get("lego_color_id"),
        "ldraw_no": data.get("ldraw_no"),
        "product_weight": data.get("product_weight"),
        "ldd_catalog": data.get("ldd_catalog"),
        "ldd_code": data.get("ldd_code"),
    }

    # 更新进度条
    pbar.update(1)

    return result

with concurrent.futures.ThreadPoolExecutor() as executor:
    # 以 utf-8 编码打开 CSV 文件并将数据写入其中
    with open(filename, "a", newline="", encoding="utf-8_sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # 仅在文件为空时写入标题
        if csvfile.tell() == 0:
            writer.writeheader()
        
        # 初始化进度条
        pbar = tqdm(total=len(ids))
        
        # 将请求提交给执行器并将数据写入 CSV 文件
        for data in executor.map(fetch_data, ids):
            if data is not None:
                writer.writerow(data)
        
        # 关闭进度条
        pbar.close()