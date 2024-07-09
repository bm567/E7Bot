import os.path

import requests
from datetime import datetime, date


def get_news(_date=None):
    if _date is None:
        d = datetime.today().date()
    else:
        date_object = datetime.strptime(_date, "%Y-%m-%d")
        # 拆分成年、月、日
        year = date_object.year
        month = date_object.month
        day = date_object.day
        try:
            # 判断日期是否有效
            d = datetime(year, month, day).date()
        except ValueError:
            return False
    file_name = d.strftime("%Y-%m-%d") + '.jpg'
    file_path = "downloads/" + d.strftime("%Y-%m-%d") + '.jpg'


    # 判断日期是否有效
    if d == datetime.today().date():
        url = "https://ravelloh.github.io/EverydayNews/latest.jpg"
    elif d > datetime.today().date():
        return False
    else:
        url = f"https://ravelloh.github.io/EverydayNews/{year}/{month}/{d.strftime('%Y-%m-%d')}.jpg"
    r = requests.get(url)
    if r.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(r.content)

        url = "https://api.imgbb.com/1/upload?expiration=600&key=567adb50b1adcc697dedf730f4074130"
        files = [
            ('image', (file_name, open(file_path, 'rb'), 'image/jpeg'))
        ]
        response = requests.request("POST", url, files=files)
        if response.status_code == 200:
            return response.json()["data"]["url"]
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    print(get_news("2024-07-09"))
