import scrapy

class CasesSpider(scrapy.Spider):
    name = "cases"
    start_urls = [
        'http://caselaw.findlaw.com/summary/search/?court=us-supreme-court&topic=cs_15&search=Search',
    ]

    def parse(self, response):

        table = response.css("table")
        rows = table[2].css("tr")
        for row in range(1, len(rows), 1):
            case = rows[row].css("td")[0].css("a::attr(href)").extract()[0]
            if case is not None:
                yield scrapy.Request(response.urljoin(case), callback=self.parse_main_page)


    def parse_main_page(self, response):
        case = response.css("div.searchable-content")
        ul_content = case.css("ul")
        yield {
            'title': case.css("h3::text").extract()[0],
            'judges': ul_content[2].css("li::text").extract(),
            'court': ul_content[3].css("li::text").extract(),
            'council': ul_content[4].css("li::text").extract(),
            'summary': case.css("p::text").extract()[1]
        }

        next_page_url = case.css("div.leaf_page > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_sub_page)


    def parse_sub_page(self, response):

        case = response.css("div.searchable-content")

        yield {
             'court': case.css("h2::text").extract()[0],

            }

