import scrapy
from ..utils import Save
from ..items import ArticleItem
class CnnenglishSpider(scrapy.Spider):
    name = "cnnenglish"
    allowed_domains = ["edition.cnn.com"]
    start_urls = ["https://edition.cnn.com"]
    custom_settings = {
        "FEEDS": {f"{Save.save_location}/cnn_english.json": {"format": "json", "overwrite": True}}
    }

    def parse(self, response):
        a_tags=list(set(response.css("a::attr(href)").getall()))
        cleaned_tags=[link for link in a_tags if "/index.html" in link]
        Save.text("Cnn_english_original",a_tags)
        Save.text("Cnn_english_cleaned",cleaned_tags)
        for index,tag in enumerate(cleaned_tags[0:2]):
            yield response.follow(tag,callback=self.parse_article,meta={"index":index})

    def parse_article(self,response):
        article_object=ArticleItem()
        article_object['title']=response.css("h1.headline__text::text").get().strip()
        article_object['url']=response.url
        yield article_object