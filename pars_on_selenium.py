from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def get_product_links(url, link_selector):
    """Получает ссылки на продукты со страницы категории."""
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")  # Игнорировать ошибки сертификата
    chrome_options.add_argument("--allow-insecure-localhost")  # Разрешить небезопасные локальные соединения
    chrome_options.add_argument("--headless")  # Запуск в безголовом режиме (опционально)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(5)  # Ожидание загрузки страницы

    # Получение всех ссылок на продукты
    product_elements = driver.find_elements(By.CSS_SELECTOR, link_selector)
    product_links = [element.get_attribute('href') for element in product_elements]
    driver.quit()
    return product_links

def parse_product_details(url, title_selector, price_selector):
    """Получает название и цену продукта по ссылке."""
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")  # Игнорировать ошибки сертификата
    chrome_options.add_argument("--allow-insecure-localhost")  # Разрешить небезопасные локальные соединения
    chrome_options.add_argument("--headless")  # Запуск в безголовом режиме (опционально)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(3)  # Ожидание загрузки страницы

    # Получение названия продукта
    title = driver.find_element(By.CSS_SELECTOR, title_selector).text
    
    # Получение цены продукта
    price = driver.find_element(By.CSS_SELECTOR, price_selector).text
    driver.quit()
    
    return title, price

def main():
    # Словарь сайтов и их параметров
    sites = {
        'iPhoriya': {
            'category_url': 'https://iphoriya.ru/product-category/iphone/iphone-15-pro',
            'link_selector': 'a.block',
            'product_title_selector': '.font-bold',  # Исправленный селектор
            'product_price_selector': '.text-xl'  # Исправленный селектор
        },
        'Eldorado': {
            'category_url': 'https://www.eldorado.ru/c/smartfony/b/APPLE/',
            'link_selector': '.product-title a',  # Селектор для ссылки на продукт
            'product_title_selector': '.product-title',  # Селектор для названия продукта
            'product_price_selector': '.product-price'  # Селектор для цены продукта
        }
    }

    all_products = {}

    # Перебор всех сайтов
    for site_name, site_info in sites.items():
        print(f"Парсинг сайта: {site_name}")
        product_links = get_product_links(site_info['category_url'], site_info['link_selector'])
        
        site_products = []
        for link in product_links:
            try:
                title, price = parse_product_details(link, site_info['product_title_selector'], site_info['product_price_selector'])
                site_products.append({
                    'title': title,
                    'price': price,
                    'link': link
                })
            except Exception as e:
                print(f"Ошибка при парсинге товара по ссылке {link}: {e}")
        
        all_products[site_name] = site_products

    # Вывод информации о продукции
    for site, products in all_products.items():
        print(f"Продукты с {site}:")
        for product in products:
            print(f"- Название: {product['title']}, Цена: {product['price']}, Ссылка: {product['link']}")
        print()
        print(products)
if __name__ == '__main__':
    main()
