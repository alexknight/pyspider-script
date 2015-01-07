#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Created on 2014-12-27 21:33:36

from pyspider.libs.base_handler import *
from urlparse import urljoin


class Handler(BaseHandler):
    def on_start(self):
        self.crawl('http://wap.jd.com/category/all.html', callback=self.all_page)

    @config(age=30 * 24 * 60 * 60)
    def all_page(self, response):
        for each in response.doc('a[href^="http://wap.jd.com/category/"]').items():
            self.crawl(urljoin(each.attr.href,'?=').replace('?=',''), callback=self.category_page)

    @config(age=30 * 24 * 60 * 60)
    def category_page(self, response):
        for each in response.doc('a[href^="http://wap.jd.com/products/"]').items():
            self.crawl(urljoin(each.attr.href,'?=').replace('?=',''), callback=self.in_page)

    @config(age=30 * 24 * 60 * 60)
    def in_page(self, response):
        for each in response.doc('a[href^="http://wap.jd.com/product/"]').items():
            self.crawl(urljoin(each.attr.href,'?=').replace('?=',''), callback=self.detail_page)
        for each in response.doc('HTML>BODY>DIV.page>A[href]').items():
            self.crawl(urljoin(each.attr.href,'?=').replace('?=',''), callback=self.in_page)

    def detail_page(self, response):
        return {
            "url": response.url,
            "category": response.doc('HTML>BODY>DIV.pro>A').text().replace(u'\u9996\u9875\u0020',''),
            "name": response.doc('title').text().replace(u'\u0020\u002d\u0020\u4EAC\u4E1C\u624B\u673A\u7248',''),
            "price": response.doc('HTML>BODY>DIV.content.content2>DIV.p-price>FONT').text().replace(u'\u00A5',''),
        }
