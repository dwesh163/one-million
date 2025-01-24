import json
import os
import requests
import pymongo
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


def process_item(item, url_template):
    try:
        url = url_template.replace("_id_", str(item['id']))

        response = requests.get(url)
        data = response.json()

        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client['mydatabase']
        collection = db['mycollection']
        collection.insert_one(data)

        with open('/logs/processed_ids.txt', 'a') as log_file:
            log_file.write(f"{item['id']},{datetime.now().isoformat()}\n")

        return True
    except Exception as e:
        print(f"Error processing {item}: {e}")
        return False


def main():
    url_template = os.environ['URL_TEMPLATE']

    with open('/data/list.json', 'r') as f:
        items = json.load(f)

    with ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        futures = [executor.submit(process_item, item, url_template) for item in items]

        for future in as_completed(futures):
            future.result()


if __name__ == '__main__':
    main()
