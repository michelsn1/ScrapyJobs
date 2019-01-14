import scrapy
from ScraperJobs.items import JobPost
#import urllib.parse
from datetime import datetime, timedelta


class InfojobsScraper(scrapy.Spider):
    name = "infojobs"
    start_urls = [
        'https://www.infojobs.com.br/empregos.aspx?Palabra=Desenvolvedor&Provincia=64',
        'https://www.infojobs.com.br/empregos.aspx?Palabra=Desenvolvedor&Provincia=182',
        'https://www.infojobs.com.br/empregos.aspx?Palabra=Desenvolvedor&Provincia=176',
        'https://www.infojobs.com.br/empregos.aspx?Palabra=Desenvolvedor&Provincia=170',
        'https://www.infojobs.com.br/empregos.aspx?Palabra=Desenvolvedor&Provincia=187',
    ]

    def parse(self, response):
        #current_query = urllib.parse.parse_qs(urllib.parse.urlparse(response.url).query)
        title = response.css('title::text').re(r'(Página [0-9]*|.*)(Vagas de Emprego de )(.*)( em )(.*)(, )(.*)( \| .*)')
        if len(title) > 2:
            carreira = title[2].title()
        else:
            carreira = None

        if len(title) > 6:
            local = title[4].title() + " - " + title[6].upper()
        else:
            local = None

        for vaga in response.css('div.element-vaga'):
            jobPost = JobPost()
            jobPost['title'] = vaga.css('div.vaga a.vagaTitle h2::text').extract_first()
            jobPost['company'] = vaga.css('div.container-vaga div.vaga-company a::text').extract_first()
            jobPost['url'] =  vaga.css('div.vaga a.vagaTitle::attr("href")').extract_first()
            jobPost['date'] = vaga.css('div.container-vaga div p.location2 span::text').extract_first()
            jobPost['date'] = jobPost['date'].replace("\r", "").replace("\n","")
            while "  " in jobPost['date']:
                jobPost['date'] = jobPost['date'].replace("  ", "")
            if "Ontem" in jobPost["date"]:
                post_date = datetime.now() - timedelta(days=1)
                jobPost['date'] = jobPost['date'].replace("Ontem", post_date.strftime("%d/%m"))
            elif "Hoje" in jobPost["date"]:
                post_date = datetime.now()
                jobPost['date'] = jobPost['date'].replace("Hoje", post_date.strftime("%d/%m"))
            jobPost['career'] = carreira
            jobPost['local'] = local
            jobPost['id'] = None
            yield jobPost

        next_page = response.css('div.pagination-highlight ul li a.lnkNext::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
