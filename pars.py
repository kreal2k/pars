import requests
from bs4 import BeautifulSoup

# Список URL страниц категорий, которые нужно парсить
urls = [
    'https://iphoriya.ru/product-category/iphone/iphone-15',
    'https://iphoriya.ru/product-category/iphone/iphone-15-pro',
]

# Открытие текстового файла для перезаписи данных
with open('output.txt', 'w', encoding='utf-8') as f:  # 'w' - режим перезаписи
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

                        # Извлечение первой цены
                        price_elements = product_soup.find_all('div', class_='text-2xl font-bold leading-dense sm:shrink-0 sm:text-3xl sm:leading-dense')

                        # Проверка найденных элементов
                        if price_elements:
                            for i, price_element in enumerate(price_elements):
                                print(f'Цена без карты: {price_element.get_text(strip=True)}')  # Для отладки
                            
                            # Первая цена (основная цена)
                            price_text = price_elements[0].get_text(strip=True).replace('\xa0', '')  # Удаляем &nbsp;

                            # Попробуем извлечь вторую цену (например, с другим классом)
                            # Замените 'price-class-for-card' на фактический класс для цены по карте
                            card_price_element = product_soup.find('div', class_='leading-dense line-through text-graphite-400 sm:text-xl')  
                            if card_price_element:
                                card_price_text = card_price_element.get_text(strip=True).replace('\xa0', '')
                                print(f'Цена по карте: {card_price_text}')  # Для отладки
                            else:
                                card_price_text = 'Не найдена'

                            # Запись данных в файл
                            f.write(f'Название: {title_element}\nЦена без карты: {price_text}\nЦена по карте: {card_price_text}\nСсылка: {product_url}\n\n')
                        else:
                            print(f'Ошибка: Цена не найдена для продукта: {title_element}')

                    else:
                        print(f'Ошибка при загрузке страницы продукта {product_url}: {product_response.status_code}')

            else:
                print(f'Ошибка при загрузке страницы {url}: {response.status_code}')
        except Exception as e:
            print(f'Произошла ошибка при обработке {url}: {e}')
