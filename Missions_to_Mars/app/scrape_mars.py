from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Scrape latest news title and paragraph
    browser.visit("https://redplanetscience.com/")

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find_all('div', class_='content_title')[0].get_text()
    paragraph = soup.find_all('div', class_='article_teaser_body')[0].get_text()
    

    # Scrape Mars image
    browser.visit("https://spaceimages-mars.com/")
    
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    img_search = soup.find_all('img', class_='headerimage fade-in')
    
    for i in img_search:
        img_path = i['src']

    featured_image_url = f'https://www.spaceimages-mars.com/{img_path}'
    
    # Scrape Mars facts
    table = pd.read_html("https://galaxyfacts-mars.com/")
    table_df = table[1]
    table_final = table_df.to_html(header=False,index=False)
    
    # Scrape hemisphere names and image links
    browser.visit("https://marshemispheres.com/")
    
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    
    ht = soup.find_all('div',class_='description')
    
    hemisphere_titles = []

    for i in ht:
        headers = i.find('h3')
        hemisphere_titles.append(headers.text)
    
    hi = soup.find_all('div',class_='item')    
    
    hemisphere_img_urls = []

    for i in hi:
        links = i.a['href']
        hemisphere_img_urls.append(f'https://marshemispheres.com/{links}')
    
    hemisphere_enhanced_img_urls = []

    for j in hemisphere_img_urls:

        browser.visit(j)

        html = browser.html
        soup = BeautifulSoup(html,'html.parser')

        enhanced_img = soup.find_all('img',class_='wide-image')
        enhanced_img_url = enhanced_img[0]['src']
    
        hemisphere_enhanced_img_urls.append(f'https://marshemispheres.com/{enhanced_img_url}')
    
    
    hemisphere_zip = zip(hemisphere_titles,hemisphere_enhanced_img_urls)
    hemisphere_final = []
    
    for a, b in hemisphere_zip:
        hemisphere_final_dict = {}
        hemisphere_final_dict['title'] = a
        hemisphere_final_dict['img_url'] = b
        hemisphere_final.append(hemisphere_final_dict)
    
    # Store data in a dictionary
    full_data = {
        'latest_news_title': title,
        'latest_news_paragraph': paragraph,
        'mars_image': featured_image_url,
        'mars_facts': table_final,
        'hemispheres': hemisphere_final
    }
    
    browser.quit()
    
    return full_data
    