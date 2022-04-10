# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):

    username = scrapy.Field()
    user_id = scrapy.Field()
    follow_id = scrapy.Field()
    follow_name = scrapy.Field()
    follow_type = scrapy.Field()
    photo = scrapy.Field()
    # likes = scrapy.Field()
    post_data = scrapy.Field()
    _id = scrapy.Field()

    pass
