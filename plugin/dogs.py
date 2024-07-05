import requests


def dog():
    r = requests.get("https://api.oick.cn/dog/api.php")
    return r


if __name__ == '__main__':
    print(dog().text)
