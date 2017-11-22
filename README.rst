===================
scrapy-rss-exporter
===================

.. image:: https://img.shields.io/pypi/v/scrapy-rss-exporter.svg
   :target: https://pypi.python.org/pypi/scrapy-rss-exporter
   :alt: PyPI Version

Generate an RSS feed using the `Scrapy <https://scrapy.org/>`_ framework.

Table of Contents
=================

* `Installation <#installation>`__
* `Usage <#usage>`__

  * `Feed Items <#feed-items>`__
  * `Global Exporter <#global-exporter>`__
  * `Per Spider Exporter <#per-spider-exporter>`__

Installation
============

* Install :code:`scrapy-rss-exporter` using :code:`pip`:

  .. code:: bash

       pip install scrapy-rss-exporter

* or using :code:`setuptools`:

  .. code:: bash

      python setup.py install

Usage
=====

Feed Items
----------

The most convenient way to use the exporter is to return the objects of
:code:`RssItem` class from your spiders. This class derives from
:code:`scrapy.Item`, so it will work with other exporters as well.

You will need to set the following keys:

.. code:: python

  from scrapy_rss_exporter.items import RssItem, Enclosure

  rss_item = RssItem()
  rss_item['title'] = 'Item title'
  rss_item['link'] = 'Item url'
  rss_item['guid'] = 'Item ID'
  rss_item['description'] = 'Item Description'
  rss_item['pub_date'] = None
  rss_item['enclosure'] = [Enclosure(url=img, type='image/jpeg')]

The :code:`pub_date` field should contain a date in the
`RFC882 <https://validator.w3.org/feed/docs/error/InvalidRFC2822Date.html>`_
format. If you use :code:`None`, the system will insert the current date
in the appropriate format. The :code:`enclosure` field is optional and should
contain a (possibly empty) list of :code:`Enclosure` objects.

Global Exporter
---------------

To set the exporter up globally, you need to declare it in the
:code:`FEED_EXPORTERS` dictionary in the :code:`settings.py` file:

.. code:: python

  FEED_EXPORTERS = {
    'rss': 'scrapy_rss_exporter.exporters.RssItemExporter'
  }

You can then use it as a :code:`FEED_FORMAT` and specify the output file in the
:code:`FEED_URI`:

.. code:: python

  FEED_FORMAT = 'rss'
  FEED_URI = 's3://my-feeds/my-feed.rss'

**Note:** Bear in mind that, if you use a local file as output, :code:`scrapy`
will append to an existing file resulting with an invalid RSS code. You should,
therefore, make sure to delete any existing output file before running the
spider. The :code:`s3` storage does not have this problem because
:code:`scrapy` uploads are using the :code:`S3 PutObject` method.

:code:`scrapy` does not seem to allow to push any configuration option to an
exporter. Therefore, if you want to customize the feed title and other metadata,
you need to create a subclass and update the :code:`FEED_EXPORTERS` dictionary
with the new class name:

.. code:: python

  class MyRssExporter(RssItemExporter):
      def __init__(self, *args, **kwargs):
          kwargs['title'] = 'My RSS'
          kwargs['link'] = 'https://www.mywebsite.com'
          kwargs['description'] = 'My RSS Items'
          super(MyRssExporter, self).__init__(*args, **kwargs)

Per Spider Exporter
-------------------

You can, of course, specify a different exporter with different settings for
each spider. Just use the :code:`custom_settings` field to override the global
configuration fields:

.. code:: python

  class MySpider(scrapy.Spider):
      name = "my"
      start_urls = ['https://www.mywebsite.com']
      custom_settings = {
          'FEED_EXPORTERS': {'rss': 'project.spiders.my_spider.MyExporter'},
          'FEED_FORMAT': 'rss',
          'FEED_URI': 's3://my-feeds/my-feed.rss',
      }

      def parse(self, response):
          pass
