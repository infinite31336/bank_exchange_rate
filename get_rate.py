from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pprint

# 不顯示 Google Chorme 視窗的設定
chrome_options = Options()
chrome_options.add_argument("--headless")

# 開啟網頁
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.implicitly_wait(10)
driver.get('https://rate.bot.com.tw/xrt?Lang=zh-TW')
currencies_dict = dict()

try:
    # 取得匯率元素
    currency_elements  = driver.find_elements(By.XPATH, "//table[@class='table table-striped table-bordered table-condensed table-hover']//tbody/tr")
    for element in currency_elements:
        currency = element.find_element(By.XPATH, ".//td[@data-table='幣別']/div/div[@class='hidden-phone print_show xrt-cur-indent']").text  # 幣別
        cash_buy_rate = element.find_element(By.XPATH, ".//td[@data-table='本行現金買入']")
        cash_sale_rate = element.find_element(By.XPATH, ".//td[@data-table='本行現金賣出']")
        spot_buy_rate = element.find_element(By.XPATH, ".//td[@data-table='本行即期買入']")
        spot_sale_rate = element.find_element(By.XPATH, ".//td[@data-table='本行即期賣出']")
        currencies_dict[currency] = {
            '現金匯率':{
                '本行買入': cash_buy_rate.text,
                '本行賣出': cash_sale_rate.text
            },
            '即期匯率':{
                '本行買入': spot_buy_rate.text,
                '本行賣出': spot_sale_rate.text
            }
        }
    pprint.pprint(currencies_dict)
except NoSuchElementException:
    print('無法定位')
driver.quit()