import scrapy
import os
from urllib.parse import urlparse
from scrapy_playwright.page import PageMethod

class PlaywrightSpider(scrapy.Spider):
    name = 'mahjong_spider'
    # start_urls = ['https://games.crazygames.com/en_US/fruit-party/index.html']
    start_urls = ['https://dalgona-game.game-files.crazygames.com/dalgona-game/39/index.html?aaConfigcatTest=true&abconfigcatabhra=false']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                headers={'Referer': 'https://games.crazygames.com/'},
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("wait_for_selector", "script"),  # 等待script标签加载完成
                    ],
                ),
                errback=self.errback,
                callback=self.parse
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        try:
            # 获取所有资源请求
            resources = []
            async def handle_request(request):
                resources.append({
                    'url': request.url,
                    'resourceType': request.resource_type
                })
            
            # 监听所有资源请求
            page.on('request', handle_request)
            
            # 获取页面内容
            content = await page.content()
            
            # 处理收集到的资源
            for resource in resources:
                url = resource['url']
                if url.startswith('//'):
                    url = 'https:' + url
                
                # 获取相对路径
                relative_path = urlparse(url).path.lstrip('/')
                if not relative_path:
                    continue
                
                # 替换HTML中的链接为相对路径
                content = content.replace(url, relative_path)
                
                # 下载资源
                yield scrapy.Request(
                    url,
                    headers={'Referer': 'https://games.crazygames.com/'},
                    meta=dict(
                        playwright=True,
                        playwright_include_page=True,
                    ),
                    callback=self.save_file,
                    errback=self.errback,
                )
            
            # 保存修改后的HTML内容
            save_path = os.path.join('download', 'index.html')
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log(f'\033[32m保存文件: {save_path}\033[0m')

        finally:
            await page.close()

    async def save_file(self, response):
        page = response.meta["playwright_page"]
        try:
            # 获取资源内容
            content = await page.content()
            
            # 解析URL路径
            url_path = urlparse(response.url).path
            if url_path == '' or url_path == '/':
                relative_path = 'index.html'
            else:
                relative_path = url_path.lstrip('/')
            
            # 构建保存路径
            save_path = os.path.join('download', relative_path)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 保存文件
            with open(save_path, 'wb') as f:
                if response.headers.get('content-type', '').decode().startswith('text'):
                    f.write(content.encode('utf-8'))
                else:
                    f.write(await page.content_frame().content())
            
            self.log(f'\033[32m保存文件: {save_path}\033[0m')
        
        finally:
            await page.close()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
        self.log(f'\033[31m下载失败: {failure.request.url}\033[0m')