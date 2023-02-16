from selenium.webdriver.common.by import By

class CategoriesPageLocators(object):
    
    CATEGORY_ANCHOR = (By.XPATH, "//a[contains(@class, 'depto_link ng-binding') and contains(text(), 'Dolor')]")

class ProductCatalogPageLocators(object):
    
    PRODUCT_CARD = (By.XPATH, "//div[@class='li_prod_picture ng-scope']")
    PAGINATION = (By.CLASS_NAME, 'paginator-container')
    ANCHOR_PAGINATION = (By.TAG_NAME, "a")
    PRODUCT_NAME = (By.XPATH, ".//div[@class='li_producto']/div[@class='middle-cont']/div[@class='li_prod_nombre middle-in']/div[@class='text-center']/a/strong")
    PRODUCT_NORMAL_PRICE = (By.XPATH, ".//div[@class='li_prod_precio cgrid-price list-price']/div[@class='middle-cont']/div[@class='li_precios middle-in']/span")
    PRODUCT_OFFER_PRICE = (By.XPATH, ".//div[@class='li_prod_precio cgrid-price list-price']/div[@class='middle-cont']/div[@class='li_precios middle-in']/ng-template/span[@class='precio_normal ng-binding']")
    NOTICE_PRIVACY = (By.ID, "noticePrivacy")
    BUTTON_NOTICE_PRIVACY_ALLOW = (By.XPATH, ".//div[@class='container']/div[@class='row']/div[@class='col-md-12']/button")