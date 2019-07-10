import urllib.request
from bs4 import BeautifulSoup
import re
import csv


# Uncomment next string to use mongodb or mysql
# import pymongo
# import mysql.connector

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

URL = 'https://www.weblancer.net/jobs/'

# Recieve number of last page in list jobs
def get_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find('div', class_='row no-gutters')
    pre_last_page = pages.find('div', class_='col-1 col-sm-2 text-right')
    last_page = pre_last_page.find('a')
    last_page = last_page.get('href')
    last_page = (re.findall("\d\d+", last_page))
    last_page = int(last_page[-1])
    return last_page

# Uncomment next block of code to connect and use database (mongo or mysql) below
# Set mongodb connection and queries (uncomment if needed)
'''def pymongo_write(pm_title, pm_category, pm_price, pm_order):
    my_client = pymongo.MongoClient("mongodb://localhost:27017")
    my_db = my_client["test"]
    my_dict = my_db["customer"]
    my_list = [{'titles':pm_title, 'categories':pm_category, 'price':pm_price, 'order':pm_order}]
    my_dict.insert_many(my_list)
    return my_list'''

# or Set MySQL connection and queries (uncomment if needed)
'''def writer_mysql(m_title, m_category, m_price, m_order):
    query = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="dvaodin1233",
        database="my_database"
    )
    connect = query.cursor()
    #connect.execute("CREATE TABLE parse_table (title VARCHAR(255), categories VARCHAR(255), price  VARCHAR (255), ordery VARCHAR (255))")
    val = (m_title, m_category, m_price, m_order)
    sql = "INSERT INTO parse_table(title, categories, price, ordery) VALUES (%s, %s, %s, %s)"
    connect.execute(sql, val)
    #connect.execute("SELECT * FROM parse_table")
    #result = connect.fetchall()
    query.commit()'''

# Create functions to parse category
def pars_titles(html):
    soup = BeautifulSoup(html,  'html.parser')
    titles = []
    for title in soup.find_all('a', class_='text-bold show_visited'):
        titles.append({title.text.replace(",", " ")})
    return titles

def pars_category(html):
    soup = BeautifulSoup(html,  'html.parser')
    categories = []
    for category in soup.find_all('div', class_='col-sm-8 text-muted dot_divided'):
        categories.append({category.text.replace(",", " ")})
    return categories

def pars_price(html):
    soup = BeautifulSoup(html,  'html.parser')
    prices = []
    for price in soup.find_all('div', class_='float-right float-sm-none title amount indent-xs-b0'):
        for x in price:
            if not x:
                x = ' '
                return x
        prices.append({price.text.replace(",", " ")})
    return prices

def pars_order(html):
    soup = BeautifulSoup(html,  'html.parser')
    orders = []
    for order in soup.find_all('div', class_='float-left float-sm-none text_field'):
        orders.append({order.text.strip().replace(",", " ")})
    return orders

def save(row1, row2, row3, row4, path):
    with open(path, 'w', newline='', encoding="utf-8") as csvfile:
        my_list = []
        zipped_tuple = zip(row1, row2, row3, row4)
        for row in zipped_tuple:
            my_list.append(row)
        writer = csv.writer(csvfile)
        writer.writerow(('Project', 'Categories', 'Prices', 'Orders'))

        # Through cickle write in csv(type dictionary), MongoDB(type str), MySQL(type str)
        for x in my_list:
            my_dicts = dict({'project':x[0], 'categories': x[1], 'price': x[2], 'order': x[3]})
            writer.writerow((', '.join(my_dicts['project']),', '.join(my_dicts['categories']),', '.join(my_dicts['price']),', '.join(my_dicts['order'])))

            # Assign varibles value str-types (uncomment first line) and second or third line (to choose mongo or mysql)
            # my_str, my_str1, my_str2, my_str3 = str(x[0]),str(x[1]),str(x[2]),str(x[3])
            # writer_mysql(my_str[2:-2], my_str1[2:-2], my_str2[2:-2], my_str3[2:-2])
            # pymongo_write(my_str[2:-2], my_str1[2:-2], my_str2[2:-2], my_str3[2:-2])

def main():
    page_count = get_page(get_html(URL))
    print('All pages', page_count)

    my_titles = []
    my_categories = []
    my_prices = []
    my_orders = []

    for page in range(1, page_count):
        print(page)
        my_titles.extend(pars_titles(get_html(URL + str(page))))
        my_categories.extend(pars_category(get_html(URL + "page=%d" % page)))
        my_prices.extend(pars_price(get_html(URL + "page=%d" % page)))
        my_orders.extend(pars_order(get_html(URL + "page=%d" % page)))

    for x in my_titles, my_categories, my_prices, my_orders:
    	print(x)
    save(my_titles, my_categories, my_prices, my_orders,  'projects.csv')

if __name__ == '__main__':
    main()