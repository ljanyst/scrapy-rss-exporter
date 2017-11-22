#-------------------------------------------------------------------------------
# Author: Lukasz Janyst <lukasz@jany.st>
# Date:   21.11.2017
# See the LICENSE file for the licensing details
#-------------------------------------------------------------------------------

import scrapy
from scrapy.exporters import XmlItemExporter
from datetime import datetime

#-------------------------------------------------------------------------------
class RssItemExporter(XmlItemExporter):
    #---------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        kwargs['root_element'] = 'rss'
        kwargs['item_element'] = 'item'
        self.channel_element = 'channel'
        self.item_element = 'item'

        now = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
        self.title = kwargs.pop('title', 'Dummy Channel')
        self.link = kwargs.pop('link', 'http://dummy.site')
        self.description = kwargs.pop('description', 'Dummy Description')
        self.language = kwargs.pop('language', 'en-us')
        self.build_date = kwargs.pop('pub_date', now)

        super(RssItemExporter, self).__init__(*args, **kwargs)
        self.indent = 2

    #---------------------------------------------------------------------------
    def start_exporting(self):
        self.xg.startDocument()
        self.xg.startElement(self.root_element, {'version': '2.0'})
        self._beautify_newline()
        self._beautify_indent(1)
        self.xg.startElement(self.channel_element, {})
        self._beautify_newline()

        self._export_xml_field('title', self.title, 2)
        self._export_xml_field('link', self.link, 2)
        self._export_xml_field('description', self.description, 2)
        self._export_xml_field('pubDate', self.build_date, 2)
        self._export_xml_field('lastBuildDate', self.build_date, 2)

    #---------------------------------------------------------------------------
    def export_item(self, item):
        self._beautify_indent(2)
        self.xg.startElement(self.item_element, {})
        self._beautify_newline()
        for k, v in self._get_serialized_fields(item):
            if k == 'enclosure':
                for enclosure in v:
                    attrs = dict(self._get_serialized_fields(enclosure))
                    self._beautify_indent(3)
                    self.xg.startElement('enclosure', attrs)
                    self.xg.endElement('enclosure')
                    self._beautify_newline()
            else:
                self._export_xml_field(k, v, 3)
        self._beautify_indent(2)
        self.xg.endElement(self.item_element)
        self._beautify_newline()

    #---------------------------------------------------------------------------
    def finish_exporting(self):
        self.xg.endElement(self.channel_element)
        self.xg.endElement(self.root_element)
        self.xg.endDocument()
