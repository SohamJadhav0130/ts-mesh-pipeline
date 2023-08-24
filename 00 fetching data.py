import requests
import json
import os
import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# in this method I have used BeautifulSoup and Selenium to do the scraping with ChromeWebDriver. 
# We can search the NASA Search Data by using keywords or any location
#Here I have scraped the first page then use the HTML element (next_page) for hovering upon the next page and then scraping it respectively. 
# Repeating this till the last page, I have added the result in a CSV file. 

class Web_Scraping:
    
    def __init__(self, location):
        self.location = location
        
    def selenium_webdriver(self):
        driver = webdriver.Chrome(executable_path=r"C:\Users\Lenovo\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
        base_url = f'https://earthdata.nasa.gov/search?keys={self.location}'
        driver.get(base_url)
        time.sleep(15)
        
        page_num = 0
        while True:
            print(f"Scraping data from page {page_num}")
            
            # Fetch the webpage and store in a variable.
            webpage = driver.page_source
            HTMLPage = BeautifulSoup(webpage, 'html.parser')
            
            # Scraping logic
            titles = []
            description = []
            links = []
    

            for search_result in HTMLPage.find_all(class_='mb-3 views-row'):
                title_elem = search_result.find(class_='search-title')
                description_elem = search_result.find(class_='search-description')
                link_elem = search_result.find(class_='views-field-url').find('a')

                if title_elem and description_elem and link_elem:
                    titles.append(title_elem.text.strip())
                    description.append(description_elem.text.strip())
                    links.append(link_elem['href'])

            # Create a DataFrame
            df = pd.DataFrame({
                'title': titles,
                'description': description,
                'link': links
            })

            # Append data to CSV
            if page_num == 0:
                df.to_csv('ws.csv', sep=',', index=False, header=True, mode='w')
            else:
                df.to_csv('ws.csv', sep=',', index=False, header=False, mode='a')
            time.sleep(15)

            # Check for next page link
            next_page_elem = HTMLPage.find('li', class_='pager__item--next')
            if next_page_elem:
                next_page_url = base_url + f'&page={page_num+1}'
                driver.get(next_page_url)
                page_num += 1
                time.sleep(10)
            else:
                break
        
        print('Web Scraping Successful!')
        driver.quit()
        
        self.generate_wordcloud(titles, description)

    def generate_wordcloud(self, titles, description):
        combined_text = ' '.join(titles + description)

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)

        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

location = input('Enter Location: ').lower()
ws = Web_Scraping(location)
ws.selenium_webdriver()
