#-------------------------------------------------------------------------------
# Author: Lukasz Janyst <lukasz@jany.st>
# Date:   21.11.2017
# See the LICENSE file for the licensing details
#-------------------------------------------------------------------------------

import scrapy
from datetime import datetime

#-------------------------------------------------------------------------------
def date_serializer(date=None):
    format = '%a, %d %b %Y %H:%M:%S %z'
    if date is None:
        return datetime.now().strftime(format)
    if isinstance(date, datetime):
        return date.strftime(format)
    return str(date)

#-------------------------------------------------------------------------------
class Enclosure(scrapy.Item):
    url = scrapy.Field()
    type = scrapy.Field()

#-------------------------------------------------------------------------------
class RssItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    guid = scrapy.Field()
    description = scrapy.Field()
    pub_date = scrapy.Field(serializer=date_serializer)
    enclosure = scrapy.Field()
    content = scrapy.Field()
