# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging, aiohttp, asyncio, os, requests
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

        for (url, path) in zip(imageURLs, paths):
            logging.log(logging.INFO, "downloading {} to {}".format(url, path))
            self.download(url, path)
        
        
    def download(self, url, path):
        resp = requests.get(url, headers=self.headers)
        with open(path, 'wb') as f:
            for chunk in resp.iter_content(10240):
                f.write(chunk)

        


# class AsyncDownloaderPipeline(object):
#     count = 1
#     path = ''
#     headers = {
#         'Referer': 'http://pic.netbian.com/4kmeinv/index.html',
#         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
#     }
#     loop = asyncio.get_event_loop()
#     # async def __del__(self):
#     #     self.loop.run_until_complete(self.tasks)
#     #     self.loop.close()

#     def process_item(self, item, spider):
#         self.path = "~/下载/{}".format(spider.album_name)
#         if not os.path.exists(self.path):
#             os.makedirs(self.path)
#         # item: pageContent
#         # iterate in item[imageURLs]
#         # download range: imageURLs, filename: self.count - count + len
#         imageURLs = item['imageURLs']
#         paths = map(lambda c: "{}/{}".format(self.path, c), range(self.count, self.count + len(imageURLs) + 1))
#         self.count += len(item['imageURLs'])
#         # await self.download(imageURLs, paths)
#         tasks = self.download(imageURLs, paths)
#         self.loop.run_until_complete(tasks)
        
#     async def download(self, urls, paths):
#         async with aiohttp.ClientSession() as session:
#             coros = map(lambda url, path: self.fetch(session, url, path), urls, paths)
#             await asyncio.wait(list(coros))
            
#     async def fetch(self, session, url, path):
#         async with session.get(url, headers=self.headers) as resp:
#             if resp.status != 200:
#                 logging.log(logging.CRITICAL, "Failing crawl page")
#                 return

#             logging.log(logging.INFO, "downloading {} to {}".format(url, path))
#             with open(path, 'wb') as f:
#                 while True:
#                     chunk = await resp.content.read(10240)
#                     if not chunk:
#                         break
#                     f.write(chunk)
                    