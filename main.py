import csv
import pandas as pd
import requests
from github import Github

# Read the ids from the id_List.csv file with utf-8 encoding
url = 'https://gitee.com/Project0ne/gaozhuan_data/blob/main/id_List.csv'
df = pd.read_csv(url, header=None)
ids = df[0].tolist()

# Define the fieldnames for the CSV file
fieldnames = ["id", "caption","price", "caption_en", "color_id",  "inventory" ]

# Authenticate with the GitHub API using your personal access token
g = Github("YOUR_PERSONAL_ACCESS_TOKEN")

# Get the repository object
repo = g.get_repo("Project0ne/gaozhuan_data")

for id in ids:
    # URL to fetch data from
    url = f'https://gobricks.cn/frontend/v1/item/filter?product_id={id}&type=2&limit=96&offset=0'

    # Send a GET request to the URL and store the response
    response = requests.get(url)

    # Open a CSV file in append mode with utf-8 encoding and write the data to it
    with open("data.csv", "a", newline="", encoding="utf-8_sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Only write the header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        for data in response.json()['rows']:
            # Extract only the fields that we want to write to the CSV file
            filtered_data = {k: v for k, v in data.items() if k in fieldnames}
            writer.writerow(filtered_data)

# Commit the changes to the repository
with open("data.csv", "r", encoding="utf-8_sig") as file:
    content = file.read()
    repo.create_file("data.csv", "Updated data.csv", content, branch="main")
