import requests
from bs4 import BeautifulSoup

# Список URL страниц категорий, которые нужно парсить
urls = [
    'https://iphoriya.ru/product-category/iphone/iphone-15',
    'https://iphoriya.ru/product-category/iphone/iphone-15-pro',
]

# Открытие текстового файла для добавления данных
with open('output.txt', 'a', encoding='utf-8') as f:
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
                product_links = soup.find_all('a', class_='block font-bold leading-snug text-graphite-800 no-underline hover:text-graphite-800 sm:text-center')

                for product in product_links:
                    # Извлечение ссылки на продукт
                    product_url = product['href']
                    
                    # Извлечение названия товара
                    title_element = product.get_text(strip=True)

                    # Печатаем информацию о продукте
                    print(f'Название: {title_element}, URL: {product_url}')

                    # Переход по ссылке карточки товара для получения дополнительной информации
                    product_response = requests.get(product_url)
                    if product_response.status_code == 200:
                        product_soup = BeautifulSoup(product_response.text, 'html.parser')

                        # Извлечение цены
                        price_element = product_soup.find('span', class_='price')
                        if price_element:
                            price_text = price_element.get_text(strip=True)

                            # Запись данных в файл
                            f.write(f'Название: {title_element}\nЦена: {price_text}\nСсылка: {product_url}\n\n')
                        else:
                            print(f'Цена не найдена для продукта: {title_element}')

                    else:
                        print(f'Ошибка при загрузке страницы продукта {product_url}: {product_response.status_code}')
            else:
                print(f'Ошибка при загрузке страницы {url}: {response.status_code}')
        except Exception as e:
            print(f'Произошла ошибка при обработке {url}: {e}')
