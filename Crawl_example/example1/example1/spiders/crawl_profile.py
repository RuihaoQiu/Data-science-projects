## crawl profiles from website

import scrapy
from scrapy.http import Request, FormRequest
from scrapy.contrib.spiders.init import InitSpider
from time import sleep
from random import randint

## extract list of name

class ProfileSpider(InitSpider):
  name = "profile"
  allowed_domains = ['malt.fr']
  login_url = 'https://www.malt.fr/signin'
  start_urls = ['https://www.malt.fr/s?q=%20&f-fam=&f-cat=&location=Paris&city=Paris&lat=48.85661400000001&lon=2.3522219000000177&p=7']

  def init_request(self):
    return Request(url=self.login_url, callback=self.login)

  def login(self, response):
    return FormRequest.from_response(
        response,
        formcss='form.sigin-new__signin-form',
        formdata={"j_username": "mangoboncourage@gmail.com", "j_password": "******"},
        callback=self.check_login)

  def check_login(self, response):
    if b"Mango" in response.body:
      self.logger.error("Login succeed!")
      return self.initialized()
    else:
      self.logger.error("Login failed!")


  def parse(self, response):
    for p in response.css('div.profile-card-v3-footer .button.clear::attr(href)'):
      sleep(randint(0, 9))
      yield response.follow(p, self.parse_profile)
     
    for href in response.css('li a.results-pager__control::attr(href)'):
      sleep(randint(0, 9))
      yield response.follow(href, callback=self.parse)     
  
  def parse_profile(self, response):
    yield { 'title': response.css('title::text').extract_first(),
			'description': response.css('div.markdown.secondary::text').extract()}

