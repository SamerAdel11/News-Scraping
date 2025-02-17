# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    title=scrapy.Field()
    url=scrapy.Field()
    category=scrapy.Field()
    published_date=scrapy.Field()
    content=scrapy.Field()
    content_html=scrapy.Field()
    tags=scrapy.Field()
    published_at=scrapy.Field()
