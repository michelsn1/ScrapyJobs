# -*- coding: utf-8 -*-
import scrapy

class LovemondaysSpider(scrapy.Spider):
    name = 'LoveMondaysv3'
    allowed_domains = ['lovemondays.com.br']
    start_urls = ['https://www.lovemondays.com.br/pesquisa/vaga/pagina/1?external_job_city_id=&external_job_city_name=&q=Desenvolvedor']

    def parse(self, response):
        print(response)
        for job in response.xpath("/html/body/main/div/div/div/div/ul/li"):
            yield {
            'Vaga' : job.xpath("a/div[2]/p[1]/text()").extract(),
            'Empresa' : job.xpath("a/div[2]/p[2]/text()").extract_first(),
            'Cidade' : job.xpath("a/div[2]/p[2]/text()")[1].extract(),
            'data' : job.xpath("a/span/time/@datetime")[0].extract(),
            }
        url = response.url
        print(url)
        pagina = url.split('?').pop(0)
        pagina = int(pagina.split('/').pop())
        pagina = str(pagina +1)
        next_page='https://www.lovemondays.com.br/pesquisa/vaga/pagina/'+pagina+'?external_job_city_id=&external_job_city_name=&q=Desenvolvedor'
        
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            
            
