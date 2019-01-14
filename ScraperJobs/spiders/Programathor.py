# -*- coding: utf-8 -*-
import scrapy

class LovemondaysSpider(scrapy.Spider):
    name = 'Programathor'
    allowed_domains = ['programathor.com.br']
    start_urls = ['https://programathor.com.br/jobs/page/1']

    def parse(self, response):
        print(response)
        for job in response.xpath("/html/body/div[3]/div/div[2]/div[2]/div"):
            yield {
            'Vaga' : job.xpath("/a/div/div[2]/div/h3/text()").extract_first(),
            'Empresa' : job.xpath("/a/div/div[2]/div/div[1]/span[1]/text()").extract_first(),
            'Cidade' : job.xpath("/a/div/div[2]/div/div[1]/span[2]/text()").extract_first(),
            'data' : job.xpath("/a/div/div[2]/div/h3/span/text()").extract_first(),
            }
        url = response.url
        print(url)
        pagina = url.split('page/').pop(1)
        pagina = int(pagina)
        pagina = str(pagina +1)
        next_page='https://programathor.com.br/jobs/page/'+pagina
        
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            


