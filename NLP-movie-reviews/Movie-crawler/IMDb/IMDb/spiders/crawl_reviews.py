## Scrape reviews of top rated movies in IMDb

import scrapy
from scrapy.http import Request, FormRequest
from scrapy.contrib.spiders.init import InitSpider
from time import sleep
from random import randint

## review spider 
class MovieSpider(scrapy.Spider):
  name = "reviews"
  allowed_domains = ['imdb.com']
  start_urls = ['https://www.imdb.com/chart/moviemeter?ref_=nv_mv_mpm_8']

  def parse(self, response):
    for g in response.css("li.subnav_item_main a::attr(href)"):
      yield response.follow(g, self.parse_genre)

  def parse_genre(self, response):
    for p in response.css("div.lister-item-content h3.lister-item-header a::attr(href)"):
      yield response.follow(p, self.parse_reviews)

  def parse_reviews(self, response):
    for m in response.css("div.user-comments"):
      next_link = m.css("a::attr(href)").extract()[-1]
      yield response.follow(next_link, self.parse_review_details)

  def parse_review_details(self, response):
    for r in response.css("div.lister-item-content"):
      yield {
      "name": response.css("div.parent h3 a::text").extract(),
      "rating": r.css("span.rating-other-user-rating span::text").extract_first(),
      "title": r.css("div.title::text").extract(),
      "review": r.css("div.text.show-more__control::text").extract()
      }

