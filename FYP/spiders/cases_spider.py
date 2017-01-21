import scrapy

class CasesSpider(scrapy.Spider):
    name = "cases"
    start_urls = [
        'http://caselaw.findlaw.com/summary/opinion/us-supreme-court/2017/01/18/278429.html',
    ]

    def parse(self, response):
        case = response.css("div.searchable-content")
        ul_content = case.css("ul")
        judges_list = ul_content[2].css("li::text").extract()
        yield {
            'title': case.css("h3::text").extract()[0],
            'introduction': case.css("p::text").extract()[1],
            'argued': ul_content[1].css("li::text").extract()[0],
            'submitted': (ul_content[1].css("li::text").extract()[1]),
            'decided': ul_content[1].css("li::text").extract()[2],
            'published': ul_content[1].css("li::text").extract()[3],
            'judges': ul_content[2].css("li::text").extract(),
            'court': ul_content[3].css("li::text").extract(),
            'council': ul_content[4].css("li::text").extract()
        }
        next_page_url = case.css("div.leaf_page > a::attr(href)").extract_first()
        print next_page_url


