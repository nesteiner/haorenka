# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os, requests, logging, scrapy
class HaorenkaPipeline:
    count = 1
    headers = {
        'Referer': 'http://pic.netbian.com/4kmeinv/index.html',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        }

    def process_item(self, item, spider):
        self.path = "/home/steiner/下载/{}".format(spider.album_name)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        imageURLs = item['imageURLs']
        paths = map(lambda c: "{}/{}".format(self.path, c), range(self.count, self.count + len(imageURLs) + 1))
        self.count += len(item['imageURLs'])

        start = 1
        for (url, path) in zip(imageURLs, paths):
            logging.log(logging.INFO, "{}. downloading {} to {}".format(start, url, path))
            self.download(url, path)
            start += 1
        
        
    def download(self, url, path):
        resp = requests.get(url, headers=self.headers)
        with open(path, 'wb') as f:
            for chunk in resp.iter_content(10240):
                f.write(chunk)

        


# Async Download Demo
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
from scrapy.exceptions import DropItem

class AsyncPipeline(ImagesPipeline):
    # def file_path(self, request, response, info, *, item):
    #     return 'files/' + os.path.basename(urlparse(request.url).path)

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no Images')
        item['image_paths'] = image_paths
        return item