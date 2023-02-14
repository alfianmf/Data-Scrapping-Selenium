import json

from scrapper.sqlite_config import SQLiteConfig
from scrapper.mongodb_config import MongoDBConfig
from scrapper.webdriver_config import WebDriver

from scrapper.utils import process_date

if __name__ == '__main__':
    f = open('metadata.json')
    metadata = json.load(f)

    location = metadata['data'][0]['name']
    location_url = metadata['data'][0]['url']
  
    f.close()

    wd = WebDriver("C:\\edgedriver_win64\\msedgedriver.exe")
    wd.scrape(location, location_url)

    # md = MongoDBConfig('config.yaml')
    # data = md.find_one('d06c3ec2ba9a4a83b1f50a84b8be0146')
    # print(data['text_review'].decode('ascii'))
    # md.delete_all()

    # date = 'setahun lalu'
    # print(process_date(date))

    # sql = SQLiteConfig('gmaps_review.db', 'tb_review')
    # sql.insert_data('tb_review', {
    #     'location': 'Curug Malela', 
    #     'text': 'Coba', 
    #     'rating': 3, 
    #     'datetime': '2022-01-03 21:54:54'
    #     })
    # sql.close_conn()
    