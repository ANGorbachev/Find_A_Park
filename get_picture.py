import requests
from bs4 import BeautifulSoup

snap_ids = [101, 301, 701, 901, 1001, 3701, 3801, 3901, 4001, 4101, 4201, 4301, 4401, 4601, 4701, 4801, 5601, 5701]

def get_picture():
    BASE_URL = "https://cars.###########.ru"

    parking_photo = []
    for snap_id in snap_ids:
        url = BASE_URL + f"/get_snap.php?id={snap_id}"
        params = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"}
        cookie = {} # {"PHPSESSID": "#####################"}
        r = requests.get(url=url, params=params, cookies=cookie)

        pic_url = BASE_URL + r.text
        r = requests.get(url=pic_url, params=params, cookies=cookie)

        with open(f"img/snap_{snap_id}.jpg", "wb") as file:
            file.write(r.content)
        parking_photo.append(pic_url)

    return parking_photo


if __name__ == "__main__":
    photos = get_picture()
    print("\n".join(photos))
