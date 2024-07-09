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
    file_path = "downloads/" + d.strftime("%Y-%m-%d") + '.jpg'
    if os.path.exists(file_path):
        return file_path

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
        return file_path
    else:
        return False


if __name__ == '__main__':
    print(get_news("2024-07-09"))
