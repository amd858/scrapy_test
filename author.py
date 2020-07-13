import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'
    start_urls = ['http://quotes.toscrape.com']
    
    def parse(self, response):
        url = response.css('div.quote > span > a::attr(href)').extract()
        for url in url:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)
        
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
            
    def parse_details(self, response):
        yield {
            'author_name': response.css('h3.author-title::text').extract_first(),
            'author_birt_date': response.css('span.author-born-date::text').extract_first(),
        }