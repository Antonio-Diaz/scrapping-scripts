import os
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException

from page import CategoriesPage, ProductPage
from settings import CHROMEDRIVER_PATH, LACOMER_URL

class LacomerCategoriesPageClick(unittest.TestCase):
    
    def setUp(self):
        self.service = Service(executable_path=CHROMEDRIVER_PATH)
        self.driver = webdriver.Firefox(service=self.service)
        self.driver.get(LACOMER_URL)
        time.sleep(5)

    def test_get_products(self):
        data = []
        categories_page = CategoriesPage(self.driver)
        categories_page.click_category()
        time.sleep(5)
        products_page = ProductPage(self.driver)
        button_allow = products_page.get_button_allow_notice_privacy()
        if button_allow:
            button_allow.click()
        time.sleep(5)
        while True:
            try:
                next_button = products_page.get_button_next()
                products = products_page.get_products()
                time.sleep(5)
                for product in products:
                    product_data = products_page.get_product_data(product)
                    data.append(product_data)
                if next_button is None:
                    print("No more pages to scrape.")
                    break
                next_button.send_keys(Keys.ENTER)
            except NoSuchElementException:
                print("No more next button.")
                break
            
        time.sleep(5)
        products_page.write_csv_data(data, "products.csv")
        path = r'C:\Users\jaudiaz\workspace\scrapping\products.csv'
        time.sleep(5)
        self.assertTrue(os.path.exists(path))
        
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()