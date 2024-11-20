#Proiect LP/Iosif Patricia/Ionescu Alexia/anul II B, subgrupa 2.2
#importam modulele necesare
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import json

#importam link-ul catre site
class BooksScraper:
    def __init__(self):
        self.url = 'https://www.elefant.ro/search?SearchTerm=python'
#transformam rezultatul generat in html
    def get_page_html(self) -> str:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.url)
        wait = WebDriverWait(driver, 10)
        wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "product-search-result")))
        source = driver.page_source
        driver.close()
        return source
#analizam documentul html creat
    def scrape_books_info(self):
        soup = BeautifulSoup(self.get_page_html(), 'html.parser') #stocam doc html in variabila soup
        books = {} #cream dictionarul in care vom stoca informatiile
        for idx, book in enumerate(soup.find_all('div', attrs={'class': re.compile(r"product-list-item*")})):
            book_info = list(book.stripped_strings)
            if len(book_info) > 1 not in book_info:
                if 'Stoc epuizat!' in book_info:
                    books[str(idx)] = {'titlu': book_info[2], 'autor': ''.join(book_info[1]),  'pret': ''.join(book_info[-3:-1])} #pentru fiecare carte regasita, salvam in dictionar titlul,autorul si pretul

        return books
#salvam informatiile gasite in fisier json
    def save_to_json(self):
        books_dict = self.scrape_books_info()
        with open('books.json', 'w') as file_out:
            file_out.write(json.dumps(books_dict))


if __name__ == 'main':
    bs = BooksScraper()
    bs.save_to_json()
