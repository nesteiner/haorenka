import scrapy
from haorenka.items import PageContent

class AlbumCrawl(scrapy.Spider):
    name = 'album'
    start_url = 'https://zhaisiji.net/20210702.html'
    album_name = '福利周刊20210702：时光隧道'
    
    def start_requests(self):
        self.start_urls = self.generateURLS(self.start_url)
        requests = map(lambda url: scrapy.Request(url=url, callback=self.parse), self.start_urls)
        return list(requests)

    def parse(self, response):
        """
        ATTENTION 这里有一个假设，parse 会被依次调用解析每一个 Response
        """
        # TODO parse one page
        selector = "div.entry-content p img::attr(data-src)"
        images = response.css(selector).extract()
        # TODO yield the output
        yield {
            'image_urls': images,
            'images': '',
            'image_paths': ''
        }


    def generateURLS(self, start_url):
        count = 2
        lst = [self.start_url]
        while count <= 4:
            lst.append(start_url + '/' + str(count))
            count += 1
        return lst