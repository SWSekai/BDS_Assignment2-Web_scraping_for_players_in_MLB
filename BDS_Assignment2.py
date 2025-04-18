from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from bs4 import BeautifulSoup
import time
import pandas as pd

class WebScrapper:
    __max_year = 2023 # 最大年份
    __max_column = 39 # 最大列數
    __current_year = 2003 # 當前年份，由遠到近
    __current_page = 1 # 當前頁碼
    
    def __init__(self, url):
        self.url = url
        self.service = Service(EdgeChromiumDriverManager().install()) # 安裝Edge驅動
        
        self.options = webdriver.EdgeOptions()
        self.options.add_experimental_option("detach", True) # 保持瀏覽器打開
        
        self.driver = webdriver.Edge(service=self.service, options=self.options) # 初始化瀏覽器
        
        self.driver.get(url)

    def cookieAccept(self):
        """
        等待cookie確認頁面加載並點擊確認按鈕
        """
        self.driver.implicitly_wait(10) # 等待cookie確認頁面加載
        
        try:
            # 使用XPATH查找按鈕元素，根據按鈕的文本內容查找
            __cookie_button = self.driver.find_element(By.XPATH, '//button[text()="OK"]')
            __cookie_button.click()
            print("Cookie確認按鈕已點擊")
        except:
            print("未找到cookie確認按鈕")
            
    def getPageSource(self):
        """
        獲取當前頁面的HTML源碼
        """
        __page_source = self.driver.page_source
        
        if __page_source is None:
            print("無法獲取當前頁面的HTML源碼")
            return None
        else:
            print("獲取當前頁面的HTML源碼成功")
        return __page_source
    
    def findAndClickExpandButton(self):
        """
        查找按鈕元素
        """
        try:
            # 使用XPATH查找按鈕元素，根據按鈕的文本內容查找
            __expand_button = self.driver.find_element(By.XPATH, '/html/body/main/div[2]/section/section/div[1]/div[2]/div/div[1]/div/div[2]/button')
            self.driver.execute_script("arguments[0].click();", __expand_button)
            print("找到按鈕，並點擊")
        except:
            print("未找到按鈕")
    
    def getTableData(self, soup): # 修改修改
        """
        獲取表格數據
        """
        __table = soup.find('table')
        if __table is None:
            print("未找到表格")
            return None
    
    def findAndClickNextButton(self):
        """
        查找下一頁按鈕元素
        """
        try:
            # 使用XPATH查找按鈕元素，根據按鈕的文本內容查找
            __next_button = self.driver.find_element(By.XPATH, '/html/body/main/div[2]/section/section/div[4]/div[2]/div/div/div[2]/button')
            self.driver.execute_script("arguments[0].click();", __next_button)
            print("找到下一頁按鈕，並點擊")
        except:
            print("未找到下一頁按鈕，將跳至下一年")
            self.url = "https://www.mlb.com/stats/pitching/" + str(self.__current_year) # 更新網址

if __name__ == "__main__":
    url = "https://www.mlb.com/stats/pitching/2003"
    
    scraper = WebScrapper(url)
    
    scraper.cookieAccept()
    
    time.sleep(2) # 等待2秒以確保頁面加載完成

    s_soup = BeautifulSoup(scraper.getPageSource(), 'html.parser') # 獲取當前頁面的HTML源碼
    
    scraper.findAndClickExpandButton() # 查找按鈕元素
    
    scraper.driver.implicitly_wait(10) # 等待按鈕點擊後頁面加載
    time.sleep(5) # Optional，等待5秒以確保頁面加載完成
    
    e_soup = BeautifulSoup(scraper.getPageSource(), 'html.parser') # 獲取當前頁面的HTML源碼
    
    scraper.findAndClickNextButton() # 查找下一頁按鈕元素

    scraper.driver.quit()