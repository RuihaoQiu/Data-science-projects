## crawl profiles from website

import scrapy

## extract list of name

class ProfileSpider(scrapy.Spider):
  name = "profile"
#  start_urls = ['https://www.malt.fr/']
  start_urls = ['https://www.malt.fr/s?q=%20&f-fam=&f-cat=&location=Paris&city=Paris&lat=48.85661400000001&lon=2.3522219000000177']
#  payload = {
#	"email": "ruihqiu@gmail.com", 
#	"password": "8888888"}

#  def login(self, response):
#    return scrapy.FormRequest.from_response(
#        response,
#        formdata=payload,
#        callback=self.parse)

  def parse(self, response):
    profiles = response.css('div.profile-card-v3-footer .button.clear::attr(href)').extract()
    for p in profiles:
      yield response.follow(p, self.parse_profile)

  def parse_profile(self, response):
    yield { 'title': response.css('title::text').extract_first(),
			'description': response.css('div.markdown.secondary::text').extract()}



