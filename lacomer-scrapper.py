import csv
import time
from typing import List

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException

FIREFOX_PROFILE  = r'C:\Users\jaudiaz\AppData\Roaming\Mozilla\Firefox\Profiles\rnqztxhe.Selenium'
URL  = 'https://www.lacomer.com.mx/lacomer/#!/pasillos/287/1?succId=287&succFmt=100,'

def intialize_driver(profile):
    """Initializate the driver

    Args:
        profile (string): location of profile to use

    Returns:
        driver: An instance of Selenium webdriver
    """
    firefox_Profile = webdriver.FirefoxProfile(profile)
    return webdriver.Firefox(firefox_Profile)

def navigate_to_website(driver, url):
    """Navigate to website

    Args:
        driver (Instance): WebDriver
        url (str): url to navigate
    
    Returns:
        None.
    """
    driver.get(url)
    
def selenium_cooldown(driver, seconds):
    """Pause the driver for the specified number of seconds."""
    print(f"Cooldown for {seconds} seconds...")
    for i in range(seconds):
        try:
            driver.execute_script("window.scrollBy(0, 1)") # Perform a small action on the page to keep the driver active
        except WebDriverException:
            pass
        time.sleep(1) # Pause for 1 second at a time
    print("Cooldown complete.")
    
def find_element(driver, xpath):
    return driver.find_element_by_xpath(xpath)

def find_elements(driver, xpath):
    return driver.find_elements_by_xpath(xpath)

def get_button_next(driver):
    try:
        pagination = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'paginator-container'))
        )
        for link in pagination.find_elements_by_tag_name("a"):
            if link.text == "Siguiente":
                return link
    except:
        print('something')
      
def get_price(product):
   try:
        price = product.find_element_by_xpath(".//div[@class='li_prod_precio cgrid-price list-price']/div[@class='middle-cont']/div[@class='li_precios middle-in']/span")
   except NoSuchElementException:
       price = product.find_element_by_xpath(".//div[@class='li_prod_precio cgrid-price list-price']/div[@class='middle-cont']/div[@class='li_precios middle-in']/ng-template/span[@class='precio_normal ng-binding']")
   return price.text[:-4]
       
def get_product_data(product: WebElement) -> List[str]:
    """Get data for a single product element

    Args:
        product (WebElement): The product element

    Returns:
        List[str]: A list containing the name and price of the product
    """
    name_element = product.find_element_by_xpath(".//div[@class='li_producto']/div[@class='middle-cont']/div[@class='li_prod_nombre middle-in']/div[@class='text-center']/a/strong")
    price = get_price(product)
    return [name_element.text, price]

def scrape_products(driver: WebDriver) -> List[List[str]]:
    """Scrape data from products by page

    Args:
        driver (WebDriver): Instance of selenium class

    Returns:
        List[List[str]]: List of products
    """
    products_data = []
    while True:
        try:
            button_next = get_button_next(driver)
            selenium_cooldown(driver, 3)
            products = find_elements(driver, "//div[@class='li_prod_picture ng-scope']")
            selenium_cooldown(driver, 3)
            for product in products:
                product_data = get_product_data(product)
                products_data.append(product_data)
            selenium_cooldown(driver, 3)
            if button_next is None:
                print("No more pages to scrape.")
                break
            button_next.send_keys(Keys.ENTER)
            selenium_cooldown(driver, 3)
        except NoSuchElementException:
            print("No more next button.")
            break
    return products_data

def write_csv_data(data: List[List[str]], output_file: str):
    """Make .csv

    Args:
        data (List[List[str]]): Data
        output_file (str): name of file
    """
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'price'])
        writer.writerows(data)

def main():
    data = []
    
    driver = intialize_driver(FIREFOX_PROFILE)
    navigate_to_website(driver, URL)
    selenium_cooldown(driver, 3)

    element = find_element(driver, "//a[contains(@class, 'depto_link ng-binding') and contains(text(), 'Dolor')]")
    href = element.get_attribute('href')
    navigate_to_website(driver, href)
    selenium_cooldown(driver, 3)

    products_data = scrape_products(driver)
    data.extend(products_data)

    write_csv_data(data, 'output2.csv')

    driver.quit()
    
if __name__ == "__main__":
    main()
    
# depto_link ng-binding --> Link class
# li_prod_picture ng-scope --> Product Card
#@ //a[@class='btn btn-primary ng-scope' and @text()='Siguiente'] 