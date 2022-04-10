# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.instaparser

    def process_item(self, item, spider):
        # item['_id'] = str(item['user_id']) + '_' + str(item['follow_id'])
        # collection = self.mongobase[spider.name]
        collection_name = item['username'].replace('.', '_')  # на всякий случай заменим точку
        collection = self.mongobase[collection_name]
        collection.insert_one(item)

        return item


class InstaPhotosPipeline(ImagesPipeline):
    # IMPORTANT TIPS:   - INSTALL the PILLOW package
    #                   - SET the IMAGES_STORE sitting in settings.py

    # нижеследующие методы мы просто переопределяем, а не создаем заново
    def get_media_requests(self, item, info):  # точка входа класса ImagesPipeline
        print()
        if item['photo']:
            try:
                print()
                yield scrapy.Request(item['photo'])  # создание новой сессии (в отличие от response в методе parse паука), аналогичный метод работает при начальном запросе в файле паука
            except Exception as e:
                print(e)

    # def item_completed(self, results, item, info):
    #     print()
    #     # item['photo'] = [itm[1] for itm in results if itm[0]]
    #
    #     return item

    def file_path(self, request, response=None, info=None, *, item=None):
        path_standard = super().file_path(request, response, info, item=item)   # return f'full/{image_guid}.jpg'
        print()

        dir_path = '/'.join([item['username'].replace('.', '_'), item['follow_type']])
        path_new = '/'.join([dir_path, path_standard[5:]])
        print(path_new)
        print()
        return path_new
