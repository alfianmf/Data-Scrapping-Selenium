import json

from scrapper.mongodb_config import MongoDBConfig
from scrapper.webdriver_config import WebDriver

from scrapper.utils import process_date

if __name__ == '__main__':
    f = open('metadata.json')
    metadata = json.load(f)

    location = metadata['data'][8]['name']
    location_url = metadata['data'][8]['url']
    reviews_count = metadata['data'][8]['reviews_count']

    f.close()
    # reviews_count = 12533
    loop_optimizer = 130 if reviews_count > 1000 else abs(int(reviews_count // 10) - 1)
    # print(loop_optimizer)

    wd = WebDriver("msedgedriver.exe")
    wd.scrape(location, location_url, loop_optimizer)

    # md = MongoDBConfig('config.yaml')
    # data = md.find_one('d06c3ec2ba9a4a83b1f50a84b8be0146')
    # print(data['text_review'].decode('ascii'))
    # md.delete_all()

    # date = 'setahun lalu'
    # print(process_date(date))
    