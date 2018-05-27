## crawl profiles from an website with login informations

import scrapy
from scrapy.http import Request, FormRequest
from scrapy.contrib.spiders.init import InitSpider
from time import sleep
from random import randint

## profile spider 
class ProfileSpider(InitSpider):
  name = "profile"
  allowed_domains = ['example.com']
  login_url = 'https://www.example.com/login'
  start_urls = ['https://www.eample.com']


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

