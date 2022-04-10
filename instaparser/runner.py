from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instaparser.spiders.instagram import InstaSpider
from instaparser import settings


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaSpider)

    process.start()


'''
1) Написать приложение, которое будет проходиться по указанному списку двух и/или более пользователей и собирать данные об их 
    - подписчиках и 
    - подписках.
2) По каждому пользователю, который является подписчиком или на которого подписан исследуемый объект нужно извлечь 
    - имя, 
    - id, 
    - фото
    - (остальные данные по желанию). 
    - Фото можно дополнительно скачать.

4) Собранные данные необходимо сложить в базу данных. Структуру данных нужно заранее продумать, чтобы:
    5) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
    6) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь

Для выполнения данной работы необходимо делать запросы в апи инстаграм с указанием заголовка User-Agent : 'Instagram 155.0.0.37.107'
'''