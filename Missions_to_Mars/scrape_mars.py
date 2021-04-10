from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

    # Red planet site URL
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    
    # Get html
    html = browser.html

    # BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # News title lists
    latest_news = soup.find_all('div', class_="list_text")

    # Latest news  
    news = latest_news[0]

    # News title and paragraph
    news_title = news.find('div', class_="content_title").text
    news_p = news.find('div', class_="article_teaser_body").text

    # Data dictionary
    news_title = str(news_title)
    news_p = str(news_p)
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    # Space Images URL
    featured_img_url = 'https://spaceimages-mars.com'
    browser.visit(featured_img_url)
    print('-----------featured image code-----------')

    # Get html
    img_html = browser.html

    # BeautifulSoup
    soup = BeautifulSoup(img_html, 'html.parser')
    featured_image_url  = soup.find("img", class_="headerimage fade-in")["src"]
    featured_image_url = 'https://www.spaceimages-mars.com/' + featured_image_url
    print(featured_image_url)

    # Data dictionary
    featured_image_url = str(featured_image_url)
    mars_data["featured_image_url"] = featured_image_url

    mars_facts_url = 'https://galaxyfacts-mars.com/'
    facts_tables = pd.read_html(mars_facts_url)
    facts_tables

    # Dataframe 
    facts_df = facts_tables[0]
    facts_df.columns = ['Description', 'Mars', 'Earth']

    # Index 
    facts_df.set_index('Description', inplace=True)

    # Push dataframe to html
    html_table = facts_df.to_html()
    html_table = (html_table)
    mars_data["facts_table"] = html_table


    # Mars hemispheres
    mars_hemis_url = 'https://marshemispheres.com'
    browser.visit(mars_hemis_url)
    xpath = '//div//a[@class="itemLink product-item"]/img'
    results = browser.find_by_xpath(xpath)
    hemisphere_image_urls = []

    # For loop
    for i in range(len(results)):
        img = results[i]      
        img.click()
        mars_usgs_html = browser.html
        soup = BeautifulSoup(mars_usgs_html, 'html.parser')
        partial_img_url = soup.find("img", class_="wide-image")["src"]
        img_url = 'https://marshemispheres.com/' + partial_img_url
        img_title = soup.find('h2', class_="title").text
        
        # Data dictionary
        img_url = str(img_url)
        img_title = str(img_title)
        img_dict = {'img_url': img_url,
                    'img_title': img_title
                   }
        
        hemisphere_image_urls.append(img_dict)
        browser.back()
        results = browser.find_by_xpath(xpath)
        i = i + 1

    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return mars_data