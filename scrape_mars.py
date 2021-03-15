from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # Setup Splinter
    executable_path = {'executable path': ChromeDriverManager().install()}
    return Browser("chrome",executable_path= ChromeDriverManager().install, headless = False)

def scrape():
    browser = init_browser()

    # Mars Latest News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.html
    soup = bs(browser.html, 'html.parser')
    article_title = soup.find_all('div', class_='bottom_gradient')[0].find('h3').text
    paragraph_text = soup.find_all('div', class_='image_and_description_container')[0].find('div', class_="article_teaser_body").text


    # Mars featured image
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    browser.html
    soup = bs(browser.html, 'html.parser')

    find_image = soup.find('img', class_='headerimage fade-in')["src"]
    featured_image_url = url + find_image

    # Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ["Measurement", "Value"]
    # Convert to HTML
    html_table = df.to_html()
    # Clean up the table
    html_table = html_table.replace('\n', '')

    # Hemispheres
    base_url = 'https://astrogeology.usgs.gov/'
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    browser.html
    soup = bs(browser.html, 'html.parser')
    
    # main_page = soup.find('div', class_='collapsible results')
    main_page_items = soup.find_all('div', class_ = 'item')
    image_urls = []
    for item in main_page_items:
        hemisphere_titles = item.find('div', class_='description').h3.text
        hemisphere_page = item.find('div', class_='description').a['href']
        browser.visit(base_url + hemisphere_page)
        soup = bs(browser.html, 'html.parser')
    #     print(base_url + hemisphere_page)
        hemisphere_link = soup.find('div', class_='downloads')
        hemisphere_url = hemisphere_link.find('li').a["href"]
        
        images_dict = {}
        images_dict['Title'] = hemisphere_titles
        images_dict['Image Link'] = hemisphere_url
        
        image_urls.append(images_dict)

    mars_dict= {
        "news_title": article_title,
        "paragraph_text": paragraph_text,
        "featured_image": featured_image_url,
        "facts_table": html_table,
        "hemispheres": image_urls

    }

    return mars_dict




