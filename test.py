import requests

url = "https://repairmyapple.ru/buy/buy-apple/buy-iphone/buy-iphne-15-pro"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Страница загружена успешно!")
else:
    print(f"Ошибка при загрузке страницы {url}: {response.status_code}")
