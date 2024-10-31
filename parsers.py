import requests
from bs4 import BeautifulSoup
import requests
import time
import random

# Настройка сессии
session = requests.Session()
url = "https://example.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://example.com/",
    "Connection": "keep-alive"
}

# Запрос к сайту с задержкой
for _ in range(5):  # Пример для нескольких попыток
    time.sleep(random.randint(1, 3))  # Случайная задержка
    response = session.get(url, headers=headers)

    if response.status_code == 200:
        print("Страница загружена успешно!")
        break  # Выход из цикла, если запрос успешен
    else:
        print(f"Ошибка при загрузке страницы: {response.status_code}")

# Дальнейшая обработка контента

# URL страницы авторизации и защищенной страницы
login_url = "https://madstore.ru/"  # Замените на реальный URL входа
protected_url = "https://madstore.ru/price-iphone-15"  # Замените на защищенный URL

# Данные для входа
payload = {
    'username': 'your_username',  # Замените на ваше имя пользователя
    'password': 'your_password'     # Замените на ваш пароль
}

# Создание сессии
session = requests.Session()

# Выполнение авторизации
response = session.post(login_url, data=payload)

# Проверка успешности входа
if response.status_code == 200 and "Welcome" in response.text:  # Замените на свою проверку
    print("Авторизация успешна!")

    # Запрос к защищенной странице
    protected_response = session.get(protected_url)
    
    if protected_response.status_code == 200:
        print("Защищенная страница загружена успешно!")
        
        # Парсинг содержимого защищенной страницы с BeautifulSoup
        soup = BeautifulSoup(protected_response.text, 'html.parser')
        
        # Ваш код для извлечения данных из страницы
        # Например, извлечение всех заголовков
        for heading in soup.find_all('h1'):
            print(heading.get_text(strip=True))
    else:
        print(f"Ошибка при загрузке защищенной страницы: {protected_response.status_code}")
else:
    print("Ошибка авторизации.")

# Список URL страниц категорий, которые нужно парсить
urls_iphoriya = [
    'https://iphoriya.ru/product-category/iphone/iphone-15',
    'https://iphoriya.ru/product-category/iphone/iphone-15-pro',
]

urls_mad_store = [
    'https://madstore.ru/price-iphone-15',  # URL нового сайта
    'https://madstore.ru/price-iphone-15-pro',
]

urls_rapair_my_apple = [
    'https://repairmyapple.ru/buy/buy-apple/buy-iphone/buy-iphne-15',  # URL нового сайта
    'https://repairmyapple.ru/buy/buy-apple/buy-iphone/buy-iphne-15-pro',
]

# Функция для парсинга данных с iPhoriya
def parse_iphoriya(url, file):
    print(f'Парсинг iPhoriya: {url}')
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Страница загружена успешно!")
            soup = BeautifulSoup(response.text, 'html.parser')
            product_links = soup.find_all('a', class_='block font-bold leading-snug text-graphite-800 no-underline hover:text-graphite-800 sm:text-center')

            for product in product_links:
                product_url = product['href']
                title_element = product.get_text(strip=True)
                print(f'Название: {title_element}, URL: {product_url}')

                product_response = requests.get(product_url)
                if product_response.status_code == 200:
                    product_soup = BeautifulSoup(product_response.text, 'html.parser')
                    price_elements = product_soup.find_all('div', class_='text-2xl font-bold leading-dense sm:shrink-0 sm:text-3xl sm:leading-dense')

                    if price_elements:
                        price_text = price_elements[0].get_text(strip=True).replace('\xa0', '')
                        card_price_element = product_soup.find('div', class_='leading-dense line-through text-graphite-400 sm:text-xl')
                        card_price_text = card_price_element.get_text(strip=True).replace('\xa0', '') if card_price_element else 'Не найдена'

                        file.write(f'Название: {title_element}\nЦена без карты: {price_text}\nЦена по карте: {card_price_text}\nСсылка: {product_url}\n\n')
                    else:
                        print(f'Ошибка: Цена не найдена для продукта: {title_element}')
                else:
                    print(f'Ошибка при загрузке страницы продукта {product_url}: {product_response.status_code}')
        else:
            print(f'Ошибка при загрузке страницы {url}: {response.status_code}')
    except Exception as e:
        print(f'Произошла ошибка при обработке {url}: {e}')

# Функция для парсинга данных с другого сайта
def parse_mad_store(url, file):
    print(f'Парсинг Mad Store: {url}')
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Страница загружена успешно!")
            soup = BeautifulSoup(response.text, 'html.parser')
            product_links = soup.find_all('a', class_='js-store-prod-name js-product-name t-store__card__title t-typography__title t-name t-name_xs')  # Замените на актуальный селектор

            for product in product_links:
                product_url = product['href']
                title_element = product.get_text(strip=True)
                print(f'Название: {title_element}, URL: {product_url}')

                product_response = requests.get(product_url)
                if product_response.status_code == 200:
                    product_soup = BeautifulSoup(product_response.text, 'html.parser')
                    price_elements = product_soup.find_all('div', class_='js-store-price-wrapper t-store__card__price-wrapper t-store__card__price-wrapper_below-title')  # Замените на актуальный селектор

                    if price_elements:
                        price_text = price_elements[0].get_text(strip=True)
                        file.write(f'Название: {title_element}\nЦена: {price_text}\nСсылка: {product_url}\n\n')
                    else:
                        print(f'Ошибка: Цена не найдена для продукта: {title_element}')
                else:
                    print(f'Ошибка при загрузке страницы продукта {product_url}: {product_response.status_code}')
        else:
            print(f'Ошибка при загрузке страницы {url}: {response.status_code}')
    except Exception as e:
        print(f'Произошла ошибка при обработке {url}: {e}')

# Функция для парсинга данных с Repair My Apple
def parse_repair_my_apple(url, file):
    print(f'Парсинг Repair My Apple: {url}')
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Страница загружена успешно!")
            soup = BeautifulSoup(response.text, 'html.parser')
            product_links = soup.find_all('a', class_='product-title ellipsis')

            for product in product_links:
                product_url = product['href']
                title_element = product.get_text(strip=True)
                print(f'Название: {title_element}, URL: {product_url}')

                product_response = requests.get(product_url)
                if product_response.status_code == 200:
                    product_soup = BeautifulSoup(product_response.text, 'html.parser')
                    price_elements = product_soup.find_all('div', class_='current-price')

                    if price_elements:
                        price_text = price_elements[0].get_text(strip=True).replace('\xa0', '')
                        card_price_element = product_soup.find('div', class_='old-price')
                        card_price_text = card_price_element.get_text(strip=True).replace('\xa0', '') if card_price_element else 'Не найдена'

                        file.write(f'Название: {title_element}\nЦена без карты: {price_text}\nЦена по карте: {card_price_text}\nСсылка: {product_url}\n\n')
                    else:
                        print(f'Ошибка: Цена не найдена для продукта: {title_element}')
                else:
                    print(f'Ошибка при загрузке страницы продукта {product_url}: {product_response.status_code}')
        else:
            print(f'Ошибка при загрузке страницы {url}: {response.status_code}')
    except Exception as e:
        print(f'Произошла ошибка при обработке {url}: {e}')

# Основной процесс парсинга
with open('output.txt', 'w', encoding='utf-8') as f:  # 'w' - режим перезаписи
    for url in urls_iphoriya:
        parse_iphoriya(url, f)

    for url in urls_mad_store:
        parse_mad_store(url, f)

    for url in urls_rapair_my_apple:
        parse_repair_my_apple(url, f)
