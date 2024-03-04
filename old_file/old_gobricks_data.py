import csv
import pandas
import requests

# Read the ids from the id_List.csv file with utf-8 encoding
with open("id_List.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    ids = [row[0] for row in reader]

for id in ids:
    # URL to fetch data from
    url = f'https://gobricks.cn/frontend/v1/item/filter?product_id={id}&type=2&limit=96&offset=0'

    # Send a GET request to the URL and store the response
    response = requests.get(url)

    # Define the fieldnames for the CSV file
    fieldnames = ["id", "product_id", "caption", "picture", "pictures", "eshop_price", "price", "caption_en", "discount", "type", "color_id", "ldd_catalog", "inventory", "buy_limit", "ldraw_no", "npd_sign", "ldd_code", "sale_volume", "rand" ,"variety", "color_data", "mpd_sign"]

    # Open a CSV file in append mode with utf-8 encoding and write the data to it
    with open("data.csv", "a", newline="", encoding="utf-8_sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Only write the header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        for data in response.json()['rows']:
            writer.writerow(data)