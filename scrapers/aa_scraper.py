import csv
import pandas as pd
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def selenium_driver(scroll_count=10):
    """Creates a selenium driver in headless mode and scrolls down the page to load more content.

    Args:
        scroll_count (int, optional): Number of times to scroll down the page. Defaults to 10.

    Returns:
        _type_: expanded page content
    """
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    url = "https://www.aa.com.tr/tr/gundem"
    driver.get(url)

    for _ in tqdm(range(scroll_count)):
        button_locator = (By.CSS_SELECTOR, ".button-daha.text-center")

        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(button_locator))
        driver.execute_script("arguments[0].scrollIntoView();", button)

        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "overlay-id")))

        driver.execute_script("arguments[0].click();", button)

        driver.implicitly_wait(3)

    expanded_page_content = driver.page_source

    driver.quit()
    return expanded_page_content

    
def get_urls(expanded_page_content) -> None:
    """Extracts and saves URLs from the expanded page content.
    Args:    
        expanded_page_content (_type_): the expanded page content obtained using selenium_driver()
    """
    print('Getting urls...')
    soup = BeautifulSoup(expanded_page_content, 'html.parser')

    for script in soup.find_all('script'):
        script.extract()

    for style in soup.find_all('style'):
        style.extract()

    div = soup.find('div', id='dvOtherContent')

    prettified_html = soup.prettify()

    a_tags = div.find_all('a', href=True, class_=False)

    links = []  

    for a_tag in a_tags:
        links.append(a_tag['href']) 

    os.makedirs('data', exist_ok=True)
    file_path = 'data/links.csv'

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Links'])
        writer.writerows([[link] for link in links])

def get_article_contents() -> list:
    """ Scrapes the content of articles from the saved URLs and stores the data.

    Returns:
        list: returns [link, content] pairs
    """
    print('Getting article contents...')
    links = pd.read_csv('data/links.csv')['Links'].tolist()

    data = []

    for link in links:
        user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(link, headers=user_agent, timeout=15)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        detay_icerik_div = soup.find('div', class_='detay-icerik')
        detay_icerik_texts = detay_icerik_div.find_all(text=True)
        # clean the texts
        detay_icerik_texts = [text.strip() for text in detay_icerik_texts if text.strip() != '']
        detay_icerik_texts = [text for text in detay_icerik_texts if 'svg' not in text]
        detay_icerik_texts = [text for text in detay_icerik_texts if 'Bu haberi paylaşın' not in text]
        detay_icerik_texts = " ".join(detay_icerik_texts)
        
        # Remove the content after the specified string
        end_index = detay_icerik_texts.find('Anadolu Ajansı web sitesinde, AA Haber Akış Sistemi (HAS) üzerinden abonelere sunulan haberler, özetlenerek yayımlanmaktadır.')
        if end_index != -1:
            detay_icerik_texts = detay_icerik_texts[:end_index]
        
        data.append([link, detay_icerik_texts])

    return data

def save_data(data):
    """Saves the scraped article content data to a CSV file.
    Args:
        data (list): a list of lists containing article links and content
    """
    data_folder_path = './data'
    os.makedirs(data_folder_path, exist_ok=True)
    csv_file_path = os.path.join(data_folder_path, 'aa_news.csv')
    
    df = pd.DataFrame(data, columns=['Link', 'Content'])
    df.to_csv(csv_file_path, index=False)
    
def scrape():
    expanded_page_content = selenium_driver()
    get_urls(expanded_page_content)
    data = get_article_contents()
    df = pd.DataFrame(data, columns=['Link', 'Content'])
    save_data(data)
    return df
    
    
if __name__ == '__main__':
    expanded_page_content = selenium_driver()
    get_urls(expanded_page_content)
    data = get_article_contents()
    save_data(data)