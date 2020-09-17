from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

# chrome driver
def init_browser():

    executable_path = {"executable_path": "../chromedriver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Nasa News

    latest_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(latest_url) 

    html = browser.html

    nasa_soup = bs(html, 'html.parser')
        

    nasa_title = nasa_soup.find_all('div', class_='content_title')[1].text

    nasa_paragraph = nasa_soup.find_all('div', class_='article_teaser_body')[0].text

    # JPL MARS IMAGES

    JPL_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(JPL_url) 

    html = browser.html

    mars_image_soup = bs(html, 'html.parser')

    mars_image = mars_image_soup.find_all('img')[3] 
    mars_image = mars_image['src'] 

    new_JPL_URL = "https://www.jpl.nasa.gov" 

    featured_image_url = new_JPL_URL + mars_image
    featured_image_url

    # MARS FACTS

    mars_facts_url = "https://space-facts.com/mars/"

    browser.visit(mars_facts_url) 

    pd_mars_facts = pd.read_html(mars_facts_url)

    mars_facts_table = pd_mars_facts[0]

    mars_facts_df = mars_facts_table
    mars_facts_df.columns = ["Description", "Mars"]

    mars_facts_df.set_index('Description', inplace=True)

    mars_html_table = mars_facts_df.to_html()

    

    # MARS Hemispheres

    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(usgs_url) 

    hemisphere_image_urls = []

    for i in range(4):
    
        browser.find_by_tag('h3')[i].click()
        html = browser.html
        hemi_soup = bs(html, 'html.parser') 
        data = {
            "title": hemi_soup.find('h2').text,
            "url": hemi_soup.find('div', class_='downloads').a['href'],
        }
        hemisphere_image_urls.append(data) 
        
        browser.back() 
    
    browser.quit() 

    return{
        "nasa_title": nasa_title,
        "nasa_paragraph": nasa_paragraph,
        "featured_image_url": featured_image_url,
        "mars_html_table": mars_html_table,
        "hemisphere_image_urls": hemisphere_image_urls

    }



