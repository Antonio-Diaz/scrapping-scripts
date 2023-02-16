import csv
import logging
from typing import List

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from locators import CategoriesPageLocators, ProductCatalogPageLocators
from settings import WAIT_TIME


logging.basicConfig(filename="test.log", level=logging.DEBUG)
class BasePage(object):
    
    def __init__(self, driver):
        self.driver = driver
    
    def get_element(self, locator_type, locator_string):
        try:
            element = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.presence_of_element_located((locator_type, locator_string))
        )
            return element
        except NoSuchElementException as e:
            logging.ERROR(f'Element with {locator_type} of {locator_string} not found', e)
            
              
    def get_elements(self, locator_type, locator_string):
        try:
            elements = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.presence_of_all_elements_located((locator_type, locator_string))
        )
            return elements
        except NoSuchElementException as e:
            logging.ERROR(f'Element with {locator_type} of {locator_string} not found', e)
            
    
    def get_text(self, locator_type, locator_string):
        element = self.get_element(locator_type, locator_string)
        return element.text
    
    def get_text_element(self, element):
        return element.text
    
    def click_button(self, locator_type, locator_string):
        self.get_element(locator_type, locator_string).click()

    def get_page_title(self):
        return self.driver.title

class CategoriesPage(BasePage):
    
    def click_category(self):
        self.click_button(*CategoriesPageLocators.CATEGORY_ANCHOR)
        
class ProductPage(BasePage):
    
    def get_button_allow_notice_privacy(self):
        try:
            notice_privacy = self.get_element(*ProductCatalogPageLocators.NOTICE_PRIVACY)
            button = notice_privacy.find_element(*ProductCatalogPageLocators.BUTTON_NOTICE_PRIVACY_ALLOW)
            return button
        except NoSuchElementException as e:
            logging.ERROR(f'Element not found', e)

    def get_products(self):
        return self.get_elements(*ProductCatalogPageLocators.PRODUCT_CARD)
    
    def get_price(self, product):
        try:
            price = product.find_element(*ProductCatalogPageLocators.PRODUCT_NORMAL_PRICE)
        except NoSuchElementException:
            price = product.find_element(*ProductCatalogPageLocators.PRODUCT_OFFER_PRICE)
        return price.text[:-4]
    
    def get_product_data(self, product: WebElement):
        name_element = product.find_element(*ProductCatalogPageLocators.PRODUCT_NAME)
        price_text = self.get_price(product)
        return [name_element.text, price_text]
    
    def get_button_next(self):
        try:
            pagination = self.get_element(*ProductCatalogPageLocators.PAGINATION)
            for link in pagination.find_elements(*ProductCatalogPageLocators.ANCHOR_PAGINATION):
                if self.get_text_element(link) == "Siguiente":
                    return link
        except NoSuchElementException as e:
            logging.ERROR(f'Element with {locator_type} of {locator_string} not found', e)

    def write_csv_data(self, data: List[List[str]], output_file: str):
        """Make .csv

        Args:
            data (List[List[str]]): Data
            output_file (str): name of file
        """
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'price'])
            writer.writerows(data)
