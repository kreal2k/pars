from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import time

def get_product_links(url, link_selector):
    """Получает ссылки на продукты со страницы категории."""
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    print(f"Загрузка страницы: {url}")

    try:
        # Ожидание загрузки элементов с увеличением времени ожидания
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, link_selector)))
        print("Элементы загружены.")
    except Exception as e:
        print(f"Не удалось загрузить элементы с селектором {link_selector}: {e}")
        driver.quit()
        return []  # Возврат пустого списка, если элементы не найдены

    # Получение всех ссылок на продукты
    product_elements = driver.find_elements(By.CSS_SELECTOR, link_selector)
    product_links = [element.get_attribute('href') for element in product_elements]

    driver.quit()
    return product_links

def parse_product_details(link, title_selector, price_selector):
    """Получает название и цену продукта по ссылке."""
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")  # Игнорировать ошибки сертификата
    chrome_options.add_argument("--allow-insecure-localhost")  # Разрешить небезопасные локальные соединения
    chrome_options.add_argument("--headless")  # Запуск в безголовом режиме (опционально)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(link)

    # Ожидание загрузки названия и цены
    title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, title_selector))
    ).text

    price = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, price_selector))
    ).text

    driver.quit()
    return title, price

def main():
    # Словарь сайтов и их параметров
    sites = {
        'iPhoriya': {
            'category_url': 'https://iphoriya.ru/product-category/iphone/iphone-15-pro',
            'link_selector': 'a.block',
            'product_title_selector': '.leading-snug text-graphite-800',  # Замените на актуальный селектор
            'product_price_selector': '.font-bold'  # Замените на актуальный селектор
        },
        'Eldorado': {
            'category_url': 'https://www.eldorado.ru/c/smartfony/b/APPLE/',
            'link_selector': '.product-title a',  # Замените на актуальный селектор
            'product_title_selector': '.product-title',  # Замените на актуальный селектор
            'product_price_selector': '.product-price'  # Замените на актуальный селектор
        }
    }

    all_products = {}

    # Перебор всех сайтов
    for site_name, site_info in sites.items():
        print(f"Парсинг сайта: {site_name}")
        product_links = get_product_links(site_info['category_url'], site_info['link_selector'])

        site_products = []

        # Параллельный парсинг товаров
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(parse_product_details, link, site_info['product_title_selector'], site_info['product_price_selector']): link for link in product_links}
            for future in futures:
                try:
                    title, price = future.result()
                    site_products.append({
                        'title': title,
                        'price': price,
                        'link': futures[future]
                    })
                except Exception as e:
                    print(f"Ошибка при парсинге товара по ссылке {futures[future]}: {e}")

        all_products[site_name] = site_products

    # Запись информации о продукции в файл
    with open('parsed_products.txt', 'w', encoding='utf-8') as file:
        for site, products in all_products.items():
            file.write(f"Продукты с {site}:\n")
            for product in products:
                file.write(f"- Название: {product['title']}, Цена: {product['price']}, Ссылка: {product['link']}\n")
            file.write("\n")

    # Вывод информации о продукции в консоль
    for site, products in all_products.items():
        print(f"Продукты с {site}:")
        for product in products:
            print(f"- Название: {product['title']}, Цена: {product['price']}, Ссылка: {product['link']}")
        print()

if __name__ == '__main__':
    main()
