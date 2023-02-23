import json

from scrapper.mongodb_config import MongoDBConfig
from scrapper.webdriver_config import WebDriver

from scrapper.utils import process_date

if __name__ == '__main__':
    # f = open('metadata.json')
    # metadata = json.load(f)

    # location = metadata['data'][10]['name']
    # location_url = metadata['data'][10]['url']
    # reviews_count = metadata['data'][10]['reviews_count']

    # f.close()

    # loop_optimizer = 120 if reviews_count > 1000 else abs(int(reviews_count // 10) - 1)
    # wd = WebDriver("C:\\edgedriver_win64\\msedgedriver.exe")
    # wd.scrape(location, location_url, loop_optimizer)

    md = MongoDBConfig('config.yaml')
    # md.delete_all()

    f = open("metadata.json")
    metadata = json.load(f)

    datas = metadata["data"]

    f.close()

    count = 0
    count_place = 0
    for data in datas:

        reviews_scrapped = 0
        status = 'Not yet'
        if (md.count_data({'location': data['name']}) > 0):
            reviews_scrapped = md.count_data({'location': data['name']})
            status = 'Done'
            count_place += 1

        result = {
            'id': data['id'],
            'name': data['name'],
            'reviews_count': data['reviews_count'],
            'reviews_scrapped': reviews_scrapped,
            'status': status
        }

        count += reviews_scrapped
        print(result)
    print({'total_place_scrapped': count_place-1, 'total_reviews_scrapped': count})