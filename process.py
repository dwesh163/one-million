import json
import os
import requests
import pymongo
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


def process_batch(batch, url_template, collection):
    processed_batch = []
    batch_log = []

    for item in batch:
        try:
            url = url_template.replace("_id_", str(item))
            response = requests.get(url)

            if response.status_code == 404:
                with open('/logs/404_errors.txt', 'a') as error_log:
                    error_log.write(f"{item},{datetime.now().isoformat()},404\n")
                continue

            response.raise_for_status()

            data = response.json()
            processed_batch.append(data)
            batch_log.append((item, datetime.now().isoformat()))

        except requests.RequestException as e:
            with open('/logs/request_errors.txt', 'a') as error_log:
                error_log.write(f"{item},{datetime.now().isoformat()},{str(e)}\n")

    if processed_batch:
        collection.insert_many(processed_batch)

    return batch_log


def main():
    url_template = os.environ['URL_TEMPLATE']

    with open('/data/list.json', 'r') as f:
        items = json.load(f)

    client = pymongo.MongoClient(os.environ['MONGODB_URI'])
    db = client['one-million']
    collection = db['products']

    with ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        batch_size = 1000
        for i in range(0, len(items), batch_size):
            batch = items[i:i+batch_size]
            future = executor.submit(process_batch, batch, url_template, collection)

            batch_logs = future.result()
            if batch_logs:
                with open('/logs/processed_ids.txt', 'a') as log_file:
                    for item_id, timestamp in batch_logs:
                        log_file.write(f"{item_id},{timestamp}\n")


if __name__ == '__main__':
    main()
