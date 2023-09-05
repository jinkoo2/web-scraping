# coding: utf-8

#this script is about the latest news of MENA region
#we scrape different influential media websites, or so-called fake news, lol
#and send only updates to the mailbox for daily newsletter
#in order to do that, we need a db to store all the historical content of websites
#and all the scraping techniques from html parse tree to regular expression
#over time, i also discovered the issue of information overload in daily newsletter
#hence, i invented a graph theory based algorithm to extract key information
#a part of this algo will also be featured in this script to solve info redundancy
#as u can see, this is the most advanced script in web scraping repository
#it contains almost every technique we have introduced so far
#make sure you have gone through all the other scripts before moving onto this one

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import os
import time
os.chdir('c:/')

def main():
    tr=scrape('https://www.reuters.com/news/archive/businessNews',reuters)    
    
#thompson reuters etl
def reuters(page):
    title,link,image=[],[],[]
    df=pd.DataFrame()
    
    prefix='https://www.reuters.com'
        
    for i in page.find('div', class_='news-headline-list').find_all('h3'):
        temp=i.text.replace('								','')
        title.append(temp.replace('\n',''))
    
    for j in page.find('div', class_='news-headline-list').find_all('a'):
        link.append(prefix+j.get('href'))
    link=link[0::2]
        
    for k in page.find('div', class_='news-headline-list').find_all('img'):
        if k.get('org-src'):
            image.append(k.get('org-src'))
        else:
            image.append('')

    
    df['title']=title
    df['link']=link
    df['image']=image
    df['text']=get_text_of_div(link, 'article-body__content__17Yit')
    
    return df

def get_text_of_div(url, div_class):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = bs(response.text, 'html.parser')
        
        # Find the HTML element that contains the article content
        # This may vary depending on the specific website structure
        article_content = soup.find('div', class_=div_class)  # Modify this based on the site structure
        
        # Extract the text content of the article
        if article_content:
            article_text = article_content.get_text()
            print(article_text)
        else:
            print("Article content not found on the page.")
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)



#scraping webpages and do some etl
def scrape(url,method):
    
    print('scraping webpage effortlessly')
    time.sleep(5)
    
    session=requests.Session()
    response = session.get(url,headers={'User-Agent': 'Mozilla/5.0'})      
    page=bs(response.content,'html.parser',from_encoding='utf_8_sig')
    
    df=method(page) 
#    out=database(df)
    
    print(df['link'][0])
    reuters_get_article(df['link'][0])

    return df   


if __name__ == "__main__":
    main()