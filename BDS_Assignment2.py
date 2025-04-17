from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from bs4 import BeautifulSoup
import time
import pandas as pd

class WebScrapper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
        self.driver.get(url)

    def cookieAccept(self):
        """
        等待cookie確認頁面加載並點擊確認按鈕
        """
        self.driver.implicitly_wait(10) # 等待cookie確認頁面加載
        
        try:
            # 使用XPATH查找按鈕元素，根據按鈕的文本內容查找
            __cookie_button__ = self.driver.find_element(By.XPATH, '//button[text()="OK"]')
            __cookie_button__.click()
            print("Cookie確認按鈕已點擊")
        except:
            print("未找到cookie確認按鈕")
            
    def getPageSource(self):
        """
        獲取當前頁面的HTML源碼
        """
        print("獲取當前頁面的HTML源碼")
        return self.driver.page_source
    
    def findAndClickExpandButton(self):
        """
        查找按鈕元素
        """
        try:
            # 使用XPATH查找按鈕元素，根據按鈕的文本內容查找
            __expand_button__ = self.driver.find_element(By.XPATH, '/html/body/main/div[2]/section/section/div[1]/div[2]/div/div[1]/div/div[2]/button')
            self.driver.execute_script("arguments[0].click();", __expand_button__)
            print("找到按鈕，並點擊")
        except:
            print("未找到按鈕")

if __name__ == "__main__":
    url = "https://www.mlb.com/stats/pitching/2003"
    
    scraper = WebScrapper(url)
    
    scraper.cookieAccept()
    
    time.sleep(2) # 等待2秒以確保頁面加載完成
    
    page_source = scraper.getPageSource() # 獲取當前頁面的HTML源碼
    
    # 解析HTML頁面
    s_soup = BeautifulSoup(page_source, 'html.parser') 
    if s_soup is None:
        print("無法解析HTML頁面")
        
    scraper.findAndClickExpandButton() # 查找按鈕元素
    scraper.driver.implicitly_wait(10) # 等待按鈕點擊後頁面加載
    time.sleep(5) # 等待5秒以確保頁面加載完成

    scraper.driver.quit()