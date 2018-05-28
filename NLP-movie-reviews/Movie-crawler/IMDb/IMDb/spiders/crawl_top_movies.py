## Scrape data of top rated movies in IMDb

import scrapy
from scrapy.http import Request, FormRequest
from scrapy.contrib.spiders.init import InitSpider
from time import sleep
from random import randint

## movie  spider 
class MovieSpider(scrapy.Spider):
  name = "movies"
  allowed_domains = ['imdb.com']
  start_urls = ['https://www.imdb.com/chart/top?ref_=nv_mv_250_6']

  def parse(self, response):
    for p in response.css("li.subnav_item_main a::attr(href)")[:1]:
#      yield {"links": p.css("a::attr(href)").extract_first()}
      yield response.follow(p, self.parse_movie)

  def parse_movie(self, response):
    for m in response.css("h3.lister-item-header a::attr(href)"):
      #yield {"links": m.css("a::attr(href)").extract_first()}
      yield response.follow(m, self.parse_movie_details)

  def parse_movie_details(self, response):
    yield {
      "title": response.css("div.title_wrapper h1::text").extract_first(),
      "rating": response.css("div.ratingValue strong span::text").extract_first()
}
# div.lister-item.mode-advanced div.lister-item-content 

"""
  def init_request(self):
    return Request(url=self.login_url, callback=self.login)

  def login(self, response):
    return FormRequest.from_response(
        response,
        formcss='form.sigin-new__signin-form',
        formdata={"j_username": "12345@abc.com", "j_password": "******"},
        callback=self.check_login)

  def check_login(self, response):
    if b"usename" in response.body:
      self.logger.error("Login succeed!")
      return self.initialized()
    else:
      self.logger.error("Login failed!")


  def parse(self, response):
    for p in response.css('div.profile-card-v3-footer .button.clear::attr(href)'):
      sleep(randint(2, 9))
      yield response.follow(p, self.parse_profile)
    
     
    for href in response.css('li a.results-pager__control::attr(href)'):
      sleep(randint(2, 9))
      yield response.follow(href, callback=self.parse)     
  
  def parse_profile(self, response):
    yield { 'title': response.css('title::text').extract_first(),
			'description': response.css('div.markdown.secondary::text').extract()}
"""
