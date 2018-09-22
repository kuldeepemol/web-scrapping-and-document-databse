# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_details = {}

    # NASA URL of page to be scraped
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, 'html.parser')

    # Get the latest news title and paragraph
    mars_details['news_title'] = nasa_soup.find('div', class_='content_title').text
    mars_details['news_para'] = nasa_soup.find('div', class_='article_teaser_body').text

    # JPL URL of page to be scraped
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    # create beautiful soup for the JPL html
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    # Extract the class with name primary_media_feature
    feature_media_section = jpl_soup.find('section', class_="primary_media_feature")
    background_image = feature_media_section.article['style']
    background_image_only = background_image.replace("background-image: url('", "").replace("');", "")
    mars_details['featured_image_url'] = "https://www.jpl.nasa.gov" + background_image_only

    # Mars weather using Twitter URL
    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_twitter_url)

    # create beautiful soup for the html
    mars_twitter_html = browser.html
    mars_twitter_soup = bs(mars_twitter_html, 'html.parser')

    # Extract the class with name js-tweet-text-container to get weather info
    mars_details['mars_weather'] = mars_twitter_soup.find('div', class_="js-tweet-text-container").text.strip()

    # Mars facts URL
    mars_fact_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_fact_url)

    # Convert tables to pandas dataframe
    df = tables[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description', inplace=True)

    mars_details['html_table'] = df.to_html()

    # Mars Hemisphere name and high resolution images
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemisphere_url)

    mars_hemisphere_html = browser.html
    mars_hemisphere_soup = bs(mars_hemisphere_html, 'html.parser')

    # Get all the hemisphere div elements
    all_hemispheres = mars_hemisphere_soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for hemisphere in all_hemispheres:
        title = hemisphere.find('h3').text

        # click on the link for each hemisphere and get the full image
        browser.click_link_by_partial_text(title)
        img_html = browser.html
        img_soup = bs(img_html, 'html.parser')
        img_url = img_soup.find('img', class_='wide-image')['src']
        final_img_url = 'https://astrogeology.usgs.gov/' + img_url

        hemisphere_info = {
            "title": title,
            "img_url": final_img_url
        }

        hemisphere_image_urls.append(hemisphere_info)

        # Go back on the browser
        browser.back()

    mars_details['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_details