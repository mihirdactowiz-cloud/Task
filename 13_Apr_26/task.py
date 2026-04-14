import requests
from lxml import html
import mysql.connector
from urllib.parse import urljoin
import time
time.sleep(1)

mydatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="books"
)

mydb = mydatabase.cursor()

mydb.execute("""
CREATE TABLE IF NOT EXISTS Categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255),
    category_url VARCHAR(255)
)
""")

mydb.execute("""
CREATE TABLE IF NOT EXISTS Books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_title VARCHAR(255),
    book_url VARCHAR(255)
)
""")

mydb.execute("""
CREATE TABLE IF NOT EXISTS Books_category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_title VARCHAR(255),
    book_url VARCHAR(255),
    category_name VARCHAR(255)
)
""")

# Start a session to handle the scraping
session = requests.Session()

base_url = "https://books.toscrape.com/catalogue/"
url = "https://books.toscrape.com/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
tree = html.fromstring(response.content)

category_links = []
categories = tree.xpath('//ul[@class="nav nav-list"]/li/ul/li/a')

# Collect all categories and their URLs
for category in categories:
    category_name = category.text.strip()
    category_url = category.get('href')
    category_links.append((category_name, category_url))

# Insert the categories into the database
for name, link in category_links:
    mydb.execute("INSERT INTO Categories (category_name, category_url) VALUES (%s, %s)", (name, link))
print(f"{len(category_links)} categories inserted")

# Books pagination logic
total_str = tree.xpath('//ul[@class="pager"]/li[@class="current"]/text()')
total = int(str(total_str[0]).strip().split("of")[1])
book_links = []

# Collect book links from the first page
for i in range(1, total + 1):
    newurl = base_url + f"page-{i}.html"
    data = requests.get(newurl)
    tree1 = html.fromstring(data.text)

    bookNames = tree1.xpath('//article[@class="product_pod"]/h3/a/@title')
    bookLinks = tree1.xpath('//article[@class="product_pod"]/h3/a/@href')
    for i in range(len(bookNames)):
        new_url = base_url + bookLinks[i]
        book_links.append((bookNames[i], new_url))

# Insert the books into the database
for name, link in book_links:
    mydb.execute("INSERT INTO Books (book_title, book_url) VALUES (%s, %s)", (name, link))
print(f"{len(book_links)} books inserted")

# category-wise: Insert books with their categories into Books_category table

for category_name, link in category_links:
    category_page_url = urljoin(url, link)

    while category_page_url:
        # Scraping the category page
        response = requests.get(category_page_url, headers=headers)
        tree1 = html.fromstring(response.content)

        # Get all book titles and URLs for this category
        book_titles = tree1.xpath('//article[@class="product_pod"]/h3/a/@title')
        book_links_page = tree1.xpath('//article[@class="product_pod"]/h3/a/@href')

        # Insert each book from this category into Books_category
        for i in range(len(book_titles)):
            full_book_url = urljoin(category_page_url, book_links_page[i])
            mydb.execute(
                "INSERT INTO Books_category (book_title, book_url, category_name) VALUES (%s, %s, %s)",
                (book_titles[i], full_book_url, category_name)
            )

        # Check if there is a next page in the category
        next_page = tree1.xpath('//li[@class="next"]/a/@href')
        if next_page:
            category_page_url = urljoin(category_page_url, next_page[0])
            time.sleep(1)  
        else:
            category_page_url = None

mydatabase.commit()
print("All books with categories inserted!")

mydb.close()
mydatabase.close()