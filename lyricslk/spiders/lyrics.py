# -*- coding: utf-8 -*-
from scrapy.spiders import SitemapSpider
import scrapy


class LyricsSpider(SitemapSpider):
    name = "lyrics"

    sitemap_urls = ["http://lyricslk.com/sitemap.xml"]
    sitemap_rules = [("/lyrics/artist/", "parse_artist"), ("/lyrics/", "parse_lyrics")]
    sitemap_follow = ["^/((?!artist).)*$"]

    def parse_lyrics(self, response):
        print("take: " + response.url)
        yield {
            "title": response.xpath('//*[@id="lyricsViewer"]/div[6]/span[2]/text()')
            .extract_first()
            .strip(": "),
            "author": response.xpath('//*[@id="lyricsViewer"]/div[6]/span[4]/text()')
            .extract_first()
            .strip(": "),
            "singer": response.xpath('//*[@id="lyricsViewer"]/div[6]/span[6]/text()')
            .extract_first()
            .strip(": "),
            "lyrics": "\n".join(
                map(
                    lambda s: s.strip(),
                    response.xpath('//*[@id="lyricsBody"]/text()').extract(),
                )
            ),
        }

    def parse_artist(self, response):
        print("skip: " + response.url)
        yield None
