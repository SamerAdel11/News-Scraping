import scrapy
import scrapy
import os
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import datetime
from ..utils import Save
from ..items import ArticleItem
class CnnarabicSpider(scrapy.Spider):
    name = "cnnarabic"
    allowed_domains = ["arabic.cnn.com"]
    base_url = "https://arabic.cnn.com"
    


    custom_settings = {
        "FEEDS": {f"{Save.save_location}/{datetime.datetime.now()}.json": {"format": "json", "overwrite": True}}
    }

    def __init__(self, keyword=None, *args, **kwargs):
        super(CnnarabicSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        print(f"Keyword is: {self.keyword}")


    def start_requests(self):
        """Start crawling based on the keyword."""
        if self.keyword:
            url = f"{self.base_url}/search?q={self.keyword}"
            yield scrapy.Request(url, callback=self.parse_search_page)

        else:
            url = self.base_url
            yield scrapy.Request(self.base_url,callback=self.parse_home_page)
    
    def parse_home_page(self,response):
        """ Parse Home Page """

        # Assigning set to remove reduntant values
        a_tags=list(set(response.css("div.clearfix a:first-of-type::attr(href)").getall()))

        # Select the articles has /article/ in their link
        cleaned_tags=[tag for tag in a_tags if '/article/' in tag]

        # Save <a> tags 
        # Save.empty_folder()
        # Save.text("cnn",a_tags)
        print("original a tags passed")
        # Save.text("cnn_cleaned",cleaned_tags)
        yield from (response.follow(tag,callback=self.parse_article) for tag in cleaned_tags)

    def parse_search_page(self, response):
        """Extracts links using Selenium and passes them to Scrapy."""
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(response.url)

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".node-story"))
            )

            # Extract all article links
            a_tags = [a.get_attribute("href") for a in driver.find_elements(By.CSS_SELECTOR, "h3 a")]
            cleaned_links = [link for link in a_tags if "/article/" in link]
            
            """ Save <a> tags """
            Save.empty_folder()
            Save.text(f"Cnn_{self.keyword}",a_tags)
            Save.text(f"Cnn_{self.keyword}__cleaned",cleaned_links)

            # Pass links to Scrapy for further processing
            for link in cleaned_links:
                yield scrapy.Request(url=link, callback=self.parse_article)

        except Exception as e:
            self.logger.error(f"Error in parse_search_page: {e}")

        finally:
            driver.quit()  # Always quit WebDriver


    def parse_article(self, response):
        """Extracts data from article pages."""
        print(f"Scraping article: {response.url}")

        article_object = ArticleItem()
        article_object["title"] = response.css("h1.flipboard-title::text").get()
        article_object["url"] = response.url
        article_object["category"] = response.css("a[rel='category']::text").get()
        article_object['content'] = response.xpath('//*[@id="body-text"]//*[not(ancestor::div[contains(@class, "browsi-skip")])]/text()').getall()
        # article_object['content_html']= " ".join(response.css("#body-text *").getall())
        article_object["tags"] = response.css("ul.browsi-skip a[rel='tag']::text").getall()
        article_object["published_at"] = response.css("header.article-header time::attr(datetime)").get()

        yield article_object
