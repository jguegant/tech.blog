#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jean Guegant'
SITENAME = u"Jean Guegant's Blog"
SITETITLE = AUTHOR
SITESUBTITLE = u'Software Engineer - C++, security, game development and random thoughts.'
SITEURL = 'http://localhost:8000'
SITELOGO = SITEURL + '/images/myself.png'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
        # ('You can modify those links in your config file', '#'),
        )

# Social widget
SOCIAL = (('linkedin', 'https://se.linkedin.com/in/jguegant'),
          ('github', 'https://github.com/Jiwan'),) 

# Menu
USE_FOLDER_AS_CATEGORY = True
MAIN_MENU = True
MENUITEMS = (('Archives', SITEURL + '/archives.html'),
             ('Categories', SITEURL + '/categories.html'),
             ('Tags', SITEURL + '/tags.html'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# THEME
THEME = "../Flex"

# Copyright License.
CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike',
    'version': '4.0',
    'slug': 'by-sa'
}

COPYRIGHT_YEAR = 2015

# Robots.
ROBOTS = u'index, follow'

# Sitemap for robots.
PLUGIN_PATHS = ['../plugins']
PLUGINS = ['sitemap']

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.6,
        'indexes': 0.6,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# Static folders.
STATIC_PATHS = ['images',]