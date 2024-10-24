import requests
from bs4 import BeautifulSoup

# Список URL страниц, которые нужно парсить
urls = [
    'https://iphoriya.ru/product-category/iphone/iphone-15',
    'https://iphoriya.ru/product-category/iphone/iphone-15-pro',
]

# Открытие текстового файла для добавления данных
with open('output.txt', 'a', encoding='utf-8') as f:  # 'a' - режим добавления
    for url in urls:
        print(f'Парсинг: {url}')
        
    try:
        # Отправка GET-запроса к странице
        response = requests.get(url)

        # Проверка статуса ответа
        if response.status_code == 200:
            # Создание объекта BeautifulSoup для парсинга
            soup = BeautifulSoup(response.text, 'html.parser')

            # Поиск всех карточек товара
            products = soup.find_all('div', class_='grow space-y-3')  # Замените на актуальный класс для карточек продуктов

            for product in products:
                title = product.find('table', class_='woocommerce-product-attributes shop_attributes')  # Замените на актуальный класс для названия
                price = product.find('span', class_='shrink-0 text-xl text-graphite-800 font-bold xl:text-lg')  # Замените на актуальный класс для цены

                # Проверка, что название и цена найдены
                if title and price:
                    title_text = title.get_text(strip=True)
                    price_text = price.get_text(strip=True)

                    # Запись данных в файл
                    f.write(f'Название: {title_text}\nЦена: {price_text}\n\n')

            print("Данные успешно добавлены в output.txt")
        else:
            print(f'Ошибка при загрузке страницы {url}: {response.status_code}')
    except Exception as e:
            print(f'Произошла ошибка при обработке {url}: {e}')