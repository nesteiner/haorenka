import scrapy, os, logging
from urllib.parse import urljoin
# DONE 1. get the album name from page 
# DONE 2. pass the link though command line
# DONE 3. assign the `IMAGE_STORE` with album_name
# TODO 4. import static variable `IMGAE_STORE` from spider class, or global variable
class AlbumCrawl(scrapy.Spider):
    name = 'album'
    
    def __init__(self, album_url=None, *args, **kwargs):
        # STUB
        if album_url == None:
            raise Exception('usage: -a album_url=...')

        if not album_url.endswith("/"):
            album_url += "/"
        super(AlbumCrawl, self).__init__(*args, **kwargs)
        self.start_url = album_url
        self.initialized = False
        

    def start_requests(self):
        self.start_urls = self.generateURLS(self.start_url)
        requests = map(lambda url: scrapy.Request(url=url, callback=self.parse), self.start_urls)
        return list(requests)

    def parse(self, response):
        """
        ATTENTION 这里有一个假设，parse 会被依次调用解析每一个 Response
        """
        # TODO get the album name
        if not self.initialized:
            self.initialized = True
            self.getAlbumName(response)
            self.album_name = self.getAlbumName(response)

        # TODO parse one page
        selector = "div.entry-content p img::attr(data-src)"
        images = response.css(selector).extract()

        # TODO yield the output
        yield {
            'image_urls': images,
            'dirname': self.album_name
        }


    def generateURLS(self, start_url):
        count = 2
        lst = [self.start_url]
        while count <= 4:
            lst.append(urljoin(start_url, str(count)))
            count += 1
        return lst

    def getAlbumName(self, response):
        album_name = response.css('#primary-home > article > header > h1::text').extract_first()
        if album_name is None:
            raise 'fuck you, can\' resolve album name'

        return album_name