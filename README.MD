# Scrapper Google Maps

This is script is a scraping script developed with Python and its automation library Selenium. Consists of a text review, rating, location, and date review from Google Maps place. The script goes one by one searching for a place in Google Maps and storing the data in MongoDB.

## Responses examples
Google Maps (Places) response example:
```json
[
    {
        "_id": "7dafe4bf2338415f9634eb1b2a8c62ac",
        "location": "Curug Malela",
        "text": "Akses jalannya waktu itu masih sulit di jangkau, perjalanan menuji curug lumayan jauh",
        "rating": 4,
        "datetime": "2022-05-14 19:55:29",
        "scrapped_at": "2023-02-14 19:55:29"
    },
    {
        "_id": "b940d215653b4b60b4e72cff44ff06df",
        "location": "Curug Malela",
        "text": "Perjalanan touring motor dari bekasi melewati Track saguling... Pas sampai curug terbayar kan dengan keindahan panorama alam sekitar curug yang masih asri...",
        "rating": 5,
        "datetime": "2022-08-14 19:55:30",
        "scrapped_at": "2023-02-14 19:55:30"
    }
]
```

## Requirements
The used requirements are specified in the requirements.txt file. If you want to execute the .py script from python, you can install the dependencies with the next command:
```bash
pip install -r requirements.txt
```

## Contributor
- Alfian Maulana Fardhani a.k.a [alfianmf](https://github.com/alfianmf)
- Fakhri Hassan Maulana a.k.a [dzzlr](https://github.com/dzzlr)