#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-01-02 07:02:17
# Project: segmentfault_blog

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

    @every(minutes=24 * 60, seconds=0)
    def on_start(self):
        self.crawl('http://segmentfault.com/blogs/newest?page=1', callback=self.index_page)

    @config(age=12 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('HTML>BODY.blog-index>DIV.wrap>DIV.container>DIV.row>DIV.col-xs-12.col-md-9.main>DIV.main__board>DIV.stream-list.blog-stream>SECTION.stream-list__item>DIV.summary>H2.title>A[href^="http://segmentfault.com/blog/"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        for each in response.doc('HTML>BODY.blog-index>DIV.wrap>DIV.container>DIV.row>DIV.col-xs-12.col-md-9.main>DIV.main__board>DIV.text-center>UL.pagination>LI.next>A[href]').items():
            self.crawl(each.attr.href, callback=self.index_page)

    @config(age=12 * 60 * 60)
    def detail_page(self, response):
        recommend = response.doc('HTML>BODY.blog-post>DIV.wrap>DIV.post-topheader>DIV.container>DIV.row>DIV.col-md-3>UL.widget-action--ver.list-unstyled>LI>STRONG#sideLiked').text()
        mark = response.doc('HTML>BODY.blog-post>DIV.wrap>DIV.post-topheader>DIV.container>DIV.row>DIV.col-md-3>UL.widget-action--ver.list-unstyled>LI>STRONG#sideBookmarked').text()
        view = response.doc('HTML>BODY.blog-post>DIV.wrap>DIV.post-topheader>DIV.container>DIV.row>DIV.col-md-3>UL.widget-action--ver.list-unstyled>LI>STRONG.no-stress').text()
        if 'k' in recommend:
            recommend = int(float(recommend[:-1])*1000)
        else:
            recommend = int(recommend)
        if 'k' in mark:
            mark = int(float(mark[:-1])*1000)
        else:
            mark = int(mark)
        if 'k' in view:
            view = int(float(view[:-1])*1000)
        else:
            view = int(view)
        return {
            "url": response.url,
            "title": response.doc('HTML>BODY.blog-post>DIV.wrap>DIV.post-topheader>DIV.container>DIV.row>DIV.col-md-9>H1#articleTitle>A').text(),
            "author": response.doc('HTML>BODY.blog-post>DIV.wrap>DIV.post-topheader>DIV.container>DIV.row>DIV.col-md-9>DIV.author>A.mr5>STRONG').text(),
            "recommend": recommend,
            "mark": mark,
            "view": view,
        }
