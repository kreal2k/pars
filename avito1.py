from avito1 import AvitoAPI

def main():
    # Инициализация API
    api = AvitoAPI()

    # Поиск автомобилей
    search_results = api.search('автомобили', category='Автомобили', region='Москва')

    # Вывод информации о ценах
    for item in search_results['items']:
        title = item['title']
        price = item['price']
        link = item['link']
        print(f"Название: {title}, Цена: {price}, Ссылка: {link}")

if __name__ == '__main__':
    main()