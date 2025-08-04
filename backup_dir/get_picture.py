import requests
from bs4 import BeautifulSoup

BASE_URL = "https://cars.################.ru"

url = BASE_URL + "/user/########/"
params = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"}
cookie = {} # {"PHPSESSID": "####################"}
parking_photo = []

r = requests.get(url=url, params=params, cookies=cookie)
soup = BeautifulSoup(r.text, "lxml")

# snaps = soup.findAll('div', id='snaps')
snaps = soup.findAll('div', class_='img snapImg')
for snap in snaps:
    image_url = snap.find("img")['src']
    img_data = requests.get(BASE_URL + image_url).content
    with open("img" + image_url[:10].rstrip("_") + ".jpg", 'wb') as handler:
        handler.write(img_data)
    parking_photo.append(image_url)

print("\n".join(parking_photo))
