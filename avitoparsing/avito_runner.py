# Ресурс: avito.ru/  Раздел: недвижимость квартиры продать. Ваша задача обойти все объявления, извлечь след данные:
# Заголовок
# цена
# Список параметров объекта
# Все полученные данные сохранить в коллекцию MongoDB. Парсинг осуществлять с помощью scrapy

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from avitoparse import settings
from avitoparse.spiders.avito import AvitoSpider

if __name__ == '__main__':
    scr_settings = Settings()
    scr_settings.setmodule(settings)
    process = CrawlerProcess(settings=scr_settings)
    process.crawl(AvitoSpider)
    process.start()