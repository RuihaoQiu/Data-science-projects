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
  start_urls = ['https://www.imdb.com/search/title?genres=comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=75c37eae-37a7-4027-a7ca-3fd76067dd90&pf_rd_r=S72Y7FWWGA9WTGS5JE80&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_1']

  def parse(self, response):
    for p in response.css("div.lister-item-content h3.lister-item-header a::attr(href)"):
      #yield {"name": p.css("").extract_first()}
      yield response.follow(p, self.parse_reviews)

  def parse_reviews(self, response):
    for m in response.css("div.user-comments"):
      next_link = m.css("a::attr(href)").extract()[-1]
#yield {"links": m.css("a::text").extract()[-1]}
      yield response.follow(next_link, self.parse_review_details)

  def parse_review_details(self, response):
    for r in response.css("div.lister-item-content"):
      yield {
      "name": response.css("div.parent h3 a::text").extract(),
      "rating": r.css("span.rating-other-user-rating span::text").extract_first(),
      "title": r.css("div.title::text").extract(),
      "review": r.css("div.text.show-more__control::text").extract()
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
