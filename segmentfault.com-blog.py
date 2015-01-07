#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Created on 2015-01-01 13:47:17

from pyspider.libs.base_handler import *

class Handler(BaseHandler):
    """
    A Sample Handler
    """
    crawl_config = {
        "headers": {
            "User-Agent": "BaiDuSpider",
        }
    }

    @every(minutes=12 * 60, seconds=0)
    def on_start(self):
        self.crawl('http://segmentfault.com/blogs/newest?page=1', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('HTML>BODY.blog-index>DIV.wrap>DIV.container>DIV.row>DIV.col-xs-12.col-md-9.main>DIV.main__board>DIV.stream-list.blog-stream>SECTION.stream-list__item>DIV.summary>H2.title>A[href^="http://segmentfault.com/blog/"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        for each in response.doc('HTML>BODY.blog-index>DIV.wrap>DIV.container>DIV.row>DIV.col-xs-12.col-md-9.main>DIV.main__board>DIV.text-center>UL.pagination>LI.next>A[href]').items():
            self.crawl(each.attr.href, callback=self.index_page)

    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('HTML>BODY.blog-post>DIV.wrap>DIV.post-topheader>DIV.container>DIV.row>DIV.col-md-9>H1#articleTitle>A').text(),
            "author": response.doc('HTML>BODY.blog-post>DIV.wrap>DIV.post-topheader>DIV.container>DIV.row>DIV.col-md-9>DIV.author>A.mr5>STRONG').text(),
            "recommend": int(response.doc('HTML>BODY.blog-post>DIV.wrap>DIV.post-topheader>DIV.container>DIV.row>DIV.col-md-3>UL.widget-action--ver.list-unstyled>LI>STRONG#sideLiked').text()),
            "mark": int(response.doc('HTML>BODY.blog-post>DIV.wrap>DIV.post-topheader>DIV.container>DIV.row>DIV.col-md-3>UL.widget-action--ver.list-unstyled>LI>STRONG#sideBookmarked').text()),
            "view": int(response.doc('HTML>BODY.blog-post>DIV.wrap>DIV.post-topheader>DIV.container>DIV.row>DIV.col-md-3>UL.widget-action--ver.list-unstyled>LI>STRONG.no-stress').text()),
        }
