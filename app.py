import tkinter as tk
from tkinter import ttk
from tkinter import * 
import tkinter.scrolledtext as scrolledtext
from PIL import ImageTk, Image
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep

def start():
    # this is a function to get the user input from the text input box
    def getInputBoxValue():
    	userInput = item_name.get()
    	return userInput
    
    # this is a function to check the status of the checkbox (1 means checked, and 0 means unchecked)
    def getCheckboxValue_Amazon():
    	checkedOrNot = cb_amazon.get()
    	return checkedOrNot
    
    # this is a function to check the status of the checkbox (1 means checked, and 0 means unchecked)
    def getCheckboxValue_Flipkart():
    	checkedOrNot = cb_flipkart.get()
    	return checkedOrNot
    
    # this is the function called when the button is clicked
    def btnClickFunction():
        amazon_result_box.delete('1.0', END)
        flipkart_result_box.delete('1.0', END)
        if getCheckboxValue_Amazon() == 1:
            try:
                amz_dict, flag_amz = search_amazon(driver, getInputBoxValue())
            except:
                print('ERROR btnClickFunction_Amazon')
                amazon_result_box.insert(END, 'Something went wrong.')
        if getCheckboxValue_Flipkart() == 1:
            try:
                flip_dict, flag_flip = search_flipkart(driver, getInputBoxValue())
            except:
                flipkart_result_box.insert(END, 'Something went wrong.')
        if getCheckboxValue_Amazon() == 1 and getCheckboxValue_Flipkart() == 1:
            try:
                print_text_box(amz_dict, flip_dict, flag_amz, flag_flip)
            except:
                amazon_result_box.insert(END, 'Something went wrong. Try again.')
                flipkart_result_box.insert(END, 'Something went wrong. Try again.')
        elif getCheckboxValue_Amazon() == 1:
            try:
                print_text_box_amz(amz_dict, flag_amz)
            except:
                amazon_result_box.insert(END, 'Something went wrong. Try again.')
        else:
            try:
                print_text_box_flip(flip_dict, flag_flip)
            except:

                flipkart_result_box.insert(END, 'Something went wrong. Try again.')
        Label(root, text='ALL PRICES ARE SHOWN IN INR', bg='RoyalBlue1', 
          font=('verdana', 12, 'normal')).place(x=200, y=430)
        b2.config(state = NORMAL)
            
    def switch():
        if getCheckboxValue_Amazon() == 1 or getCheckboxValue_Flipkart() == 1:
            if getInputBoxValue() != '':
                b1.config(state = NORMAL)
        else:
            b1.config(state = DISABLED)
        
    def print_text_box(amazon_dictionary, flipkart_dictionary, amazon_flag, flipkart_flag):
        if amazon_flag == False:
            amazon_result_box.insert(END, 'Item not found. Closest match is as follows:\n\n')
        for key in amazon_dictionary:
            amazon_result_box.insert(END, '{} {}\n\n'.format(key, amazon_dictionary[key]))
        if flipkart_flag == False:
            flipkart_result_box.insert(END, 'Item not found. Closest match is as follows:\n')
        for key in flipkart_dictionary:
            flipkart_result_box.insert(END, '{} {}\n\n'.format(key, flipkart_dictionary[key]))
        b1.config(state = DISABLED)
    
    def print_text_box_amz(amazon_dictionary, amazon_flag):
        if amazon_flag == False:
            amazon_result_box.insert(END, 'Item not found. Closest match is as follows:\n\n')
        for key in amazon_dictionary:
            amazon_result_box.insert(END, '{} {}\n'.format(key, amazon_dictionary[key]))
        b1.config(state = DISABLED)
            
    def print_text_box_flip(flipkart_dictionary, flipkart_flag):
        if flipkart_flag == False:
            flipkart_result_box.insert(END, 'Item not found. Closest match is as follows:\n')
        for key in flipkart_dictionary:
            flipkart_result_box.insert(END, '{} {}\n'.format(key, flipkart_dictionary[key]))
        b1.config(state = DISABLED)
            
    def initialize():
        options = Options()
        #options.add_argument('--headless')
        options.add_argument('--lang=en_US') 
        driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
        return driver
            
    def search_amazon(driver, item_name):
        amazon_dict = {}
        item_found = True
        driver.get('https://www.amazon.in/')
        driver.find_element_by_xpath('//input[@name = "field-keywords"]')\
            .send_keys(item_name)
        driver.find_element_by_xpath('//input[@type = "submit"]').click()
        sleep(2)
        item = driver.find_element_by_xpath('//a[@class="a-link-normal a-text-normal"]')
        check = item_name.split(' ')
        count = 0
        for i in range(len(check)):
            if check[i] not in item.text.lower():
                count += 1
        if count != 0:
            print('Item not found with that keyword. Nearest match is as follows:')
            item_found = False
            #return 
        item.click()
        print('\nTop result: ', item.text)
        amazon_dict['Item name: '] = item.text
        driver.switch_to.window(driver.window_handles[-1])
        try:
            price = driver.find_element_by_xpath('//*[@id="priceblock_ourprice"]').text
        except:
            try:
                price = driver.find_element_by_xpath('//*[@id="priceblock_saleprice"]').text
            except:
                try:
                    price = driver.find_element_by_xpath('//*[@id="soldByThirdParty"]/span').text
                except:
                    amazon_result_box.insert(END, 'Something went wrong.')
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
        amazon_dict['Price: '] = price
        return amazon_dict, item_found
        
    def search_flipkart(driver, item_name):
        flipkart_dict = {}
        item_found = True
        driver.get('https://www.flipkart.com/')
        sleep(1)
        driver.find_element_by_xpath('/html/body/div[2]/div/div/button').click()
        driver.find_element_by_xpath('//input[@type = "text"]')\
            .send_keys(item_name)
        driver.find_element_by_xpath('//button[@type = "submit"]').click()
        sleep(3)
        try:
            item = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div/div/a/div[2]/div[1]/div[1]')
        except:
            try:
                item = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div')
            except:
                print('Something went wrong.')
        check = item_name.split(' ')
        count = 0
        for i in range(len(check)):
            if check[i] not in item.text.lower():
                count += 1
        if count != 0:
            print('Item not found with that keyword. Nearest match is as follows:')
            item_found = False
            #return 
        item.click()
        driver.switch_to.window(driver.window_handles[-1])
        sleep(2)
        try:
            item_actual_name = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[1]/h1/span').text
        except:
            try:
                item_actual_name = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span').text
            except:
                flipkart_result_box.insert(END, 'Something went wrong.')
                return
        print('\nTop result: ', item_actual_name)
        flipkart_dict['Item name: '] = item_actual_name
        try:
            price = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[1]').text
        except:
            try:
                price = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div').text
            except:
                try:
                    price = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[1]').text
                except:
                    flipkart_result_box.insert(END, 'Something went wrong.')
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
        flipkart_dict['Price: '] = price
        return flipkart_dict, item_found
    
    global root
    root = Tk()
    #this is the declaration of the variable associated with the checkbox
    cb_amazon = tk.IntVar()
    
    #this is the declaration of the variable associated with the checkbox
    cb_flipkart = tk.IntVar()
    
    # This is the section of code which creates the main window
    root.geometry('650x525')
    root.configure(background='RoyalBlue1')
    #image1= tk.PhotoImage(file = 'pawel-czerwinski-BP2RioglKXk-unsplash.png')
    #label_for_image= Label(root, image=image1)
    #label_for_image.pack()
    root.title('Price Comparison')
    
    
    # This is the section of code which creates a text input box
    item_name=Entry(root)
    item_name.place(x=300, y=90)
    
    
    # This is the section of code which creates the a label
    Label(root, text='Item Name', bg='RoyalBlue1', font=('verdana', 12, 'normal')).place(x=195, y=88)
    
    
    # This is the section of code which creates a checkbox
    CheckBoxAmazon=Checkbutton(root, text='Amazon', variable=cb_amazon, bg='RoyalBlue1', 
                               font=('verdana', 12, 'normal'), command = switch)
    CheckBoxAmazon.place(x=163, y=155)
    
    
    # This is the section of code which creates a checkbox
    CheckBoxFlipkart=Checkbutton(root, text='Flipkart', variable=cb_flipkart, bg='RoyalBlue1', 
                                 font=('verdana', 12, 'normal'), command = switch)
    CheckBoxFlipkart.place(x=390, y=155)
    
    # This is the section of code which creates a button
    b1 = Button(root, text='Submit', bg='wheat1', font=('verdana', 12, 'bold'), command=btnClickFunction, 
                state = tk.DISABLED)
    b1.place(x=285, y=210)
    initialize()
    
    amazon_result_box = scrolledtext.ScrolledText(root, height=7, width=30, wrap = tk.WORD)
    amazon_result_box.place(x=25, y=300)
    #amazon_result_box.config(state = tk.DISABLED)
    
    flipkart_result_box = scrolledtext.ScrolledText(root, height=7, width=30, wrap = tk.WORD)
    flipkart_result_box.place(x=370, y=300)
    #flipkart_result_box.config(state = tk.DISABLED)
    
    Label(root, text='Amazon', bg='RoyalBlue1', font=('verdana', 12, 'normal')).place(x=130, y=265)
    Label(root, text='Flipkart', bg='RoyalBlue1', font=('verdana', 12, 'normal')).place(x=460, y=265)
    b2 = Button(root, text='Search Again', bg='wheat1', font=('verdana', 12, 'bold'), command = restart,
                state = tk.DISABLED)
    b2.place(x=260, y=460)
    
    root.resizable(False, False)
    
    driver = initialize()
    
    """while True:
        root.mainloop()
        if b2['state'] == DISABLED:
            break"""
    root.mainloop()
    
if __name__ == '__main__':
    def restart():
        root.destroy()
        start()
    start()

