from setuptools import setup

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name = 'scrapy-rss-exporter',
    version = '0.1',
    author = 'Lukasz Janyst',
    author_email = 'xyz@jany.st',
    url = 'https://github.com/ljanyst/scrapy-rss-exporter',
    description = 'An RSS Exporter for Scrapy',
    long_description = long_description,
    license = 'BSD License',
    packages = ['scrapy_rss_exporter'],
    classifiers = [
        'Framework :: Scrapy',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires = ['scrapy>=1.4.0']
)
