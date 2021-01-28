from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

class PriceComparison():
    
    def __init__(self):
        options = Options()
        #options.add_argument('--headless')
        options.add_argument('--lang=en_US') 
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
        
    def search_amazon(self, item_name):
        self.driver.get('https://www.amazon.in/')
        print('Connecting to Amazon')
        print('---------------------------')
        self.driver.find_element_by_xpath('//input[@name = "field-keywords"]')\
            .send_keys(item_name)
        self.driver.find_element_by_xpath('//input[@type = "submit"]').click()
        sleep(2)
        item = self.driver.find_element_by_xpath('//a[@class="a-link-normal a-text-normal"]')
        check = item_name.split(' ')
        count = 0
        for i in range(len(check)):
            if check[i] not in item.text.lower():
                count += 1
        if count != 0:
            print('Item not found with that keyword. Nearest match is as follows:')
            #return 
        item.click()
        print('\nTop result: ', item.text)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        try:
            price = self.driver.find_element_by_xpath('//*[@id="priceblock_ourprice"]').text
        except:
            try:
                price = self.driver.find_element_by_xpath('//*[@id="priceblock_saleprice"]').text
            except:
                try:
                    price = self.driver.find_element_by_xpath('//*[@id="soldByThirdParty"]/span').text
                except:
                    print('Something went wrong.')
                    return
        price = price.strip('₹')
        price = price.strip()
        #print(price)
        price = price.replace(',','')
        #print(price)
        price = price.split('.')
        #print(price)
        price = int(price[0])
        print('\nPrice of said item: ', price)
        print('\nAll prices shown are in INR.\n---------------------------')

        
    def search_flipkart(self, item_name):
        self.driver.get('https://www.flipkart.com/')
        sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[2]/div/div/button').click()
        print('\nConnecting to Flipkart')
        print('---------------------------')
        self.driver.find_element_by_xpath('//input[@type = "text"]')\
            .send_keys(item_name)
        self.driver.find_element_by_xpath('//button[@type = "submit"]').click()
        sleep(3)
        try:
            item = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div/div/a/div[2]/div[1]/div[1]')
        except:
            try:
                item = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div')
            except:
                print('Something went wrong.')
        check = item_name.split(' ')
        count = 0
        for i in range(len(check)):
            if check[i] not in item.text.lower():
                count += 1
        if count != 0:
            print('Item not found with that keyword. Nearest match is as follows:')
            #return 
        item.click()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        sleep(2)
        try:
            item_actual_name = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[1]/h1/span').text
        except:
            try:
                item_actual_name = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span').text
            except:
                print('Something went wrong.')
                return
        print('\nTop result: ', item_actual_name)
        try:
            price = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[1]').text
        except:
            try:
                price = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div').text
            except:
                try:
                    price = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[1]').text
                except:
                    print('Something went wrong.')
                    return
        price = price.strip('₹')
        price = price.strip()
        #print(price)
        price = price.replace(',','')
        #print(price)
        price = price.split('.')
        #print(price)
        price = int(price[0])
        print('\nPrice of said item: ', price)
        print('\nAll prices shown are in INR.\n---------------------------')
        
bot = PriceComparison()
bot.search_amazon('ukulele')
bot.search_flipkart('ukulele')
