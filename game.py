import bs4
import requests
from bs4 import BeautifulSoup
import fake_useragent
import xlsxwriter

user = fake_useragent.UserAgent().random
headers = {'user-agent': user}
main_url = 'https://re-store.ru/'
data = [['Наименование', 'Цена', 'Ссылка', 'Картинка']]


def get_soup(url):
    res = requests.get(url, headers)
    return bs4.BeautifulSoup(res.text, 'html.parser')


categories_page = get_soup(main_url + '/apple-iphone/')
categories = categories_page.find_all('div', class_="catalog__products")
for cat in categories:
    subcategories_page = get_soup(main_url + cat['href'])
    subcategories = subcategories_page.find_all('a', class_="product-card__link")
    for subcat in subcategories:
        iphones_page = get_soup(main_url + subcat['href'])
        iphones = iphones_page.find_all('div', class_="product-card__wrap")
        for iphone in iphones:
            title = iphone.find('div', class_="product-card__title").strip()
            price = iphone.find('div', class_="product-card__prices").find(text=True).strip()
            url = iphone.find('a'), ['href'].strip()
            img = iphone.find('div', class_='image')['style'].split('url(')[1].split(')')[0].replace('/tn/', '/source/')
            data.append([title, price, main_url + url, main_url + img])

with xlsxwriter.Workbook('iphones.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, info in enumerate(data):
        worksheet.write_row(row_num, 0, info)
