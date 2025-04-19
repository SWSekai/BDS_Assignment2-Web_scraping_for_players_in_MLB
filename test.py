import requests
from bs4 import BeautifulSoup

def check_status_code(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        return True
    else:
        return False

def get_web_data(url):
    response = requests.get(url)
    response.encoding = "utf8"
    soup = BeautifulSoup(response.text, "lxml")
    return soup

def find_table(soup):
    table = soup.find(attrs={"class": "stats-body-table player"})
    if table:
        return table
    else:
        raise ValueError("No table found in the provided HTML content.")
    
if __name__ == "__main__":
    url = 'https://www.mlb.com/stats/pitching/2024'
    
    status = check_status_code(url)
    
    if status:
        print("URL is reachable")
        data = get_web_data(url)
        if data:
            print("Data captured successfully")
            tag_table = find_table(data)
            print(tag_table)
    else:
        print("URL is not reachable")