import json
import os
from typing import List
from urllib.parse import urljoin, urlparse

import scrapy


class ImageSpider(scrapy.Spider):
    name = "image_spider"
    start_urls: List[str] = []

    def __init__(
        self, start_urls=None, download_dir="download/images", *args, **kwargs
    ):
        super(ImageSpider, self).__init__(*args, **kwargs)
        if start_urls:
            self.start_urls = start_urls
        # 支持自定义下载目录
        self.download_dir = download_dir

    def parse(self, response):
        try:
            # 解析JSON数据
            data = json.loads(response.text)

            # 创建下载目录
            os.makedirs(self.download_dir, exist_ok=True)

            # 递归搜索所有可能的图片URL
            image_urls = self.find_image_urls(data)

            # 下载找到的所有图片
            for url in image_urls:
                # 处理相对路径
                if not url.startswith(("http://", "https://")):
                    url = urljoin(response.url, url)

                self.log(f"\033[34m发现图片: {url}\033[0m")

                yield scrapy.Request(
                    url,
                    callback=self.save_image,
                    errback=self.errback,
                    meta={"original_url": url},
                )
        except Exception as e:
            self.log(f"\033[31mJSON解析失败: {str(e)}\033[0m")

    def find_image_urls(self, obj, urls=None):
        """递归搜索JSON中的所有图片URL"""
        if urls is None:
            urls = set()

        if isinstance(obj, dict):
            for key, value in obj.items():
                # 检查值是否为URL字符串
                if isinstance(value, str):
                    if self.is_image_url(value):
                        urls.add(value)
                # 如果值是字典或列表，继续递归搜索
                elif isinstance(value, (dict, list)):
                    self.find_image_urls(value, urls)
                # 尝试解析嵌套的JSON字符串
                elif isinstance(value, str):
                    try:
                        nested_obj = json.loads(value)
                        self.find_image_urls(nested_obj, urls)
                    except json.JSONDecodeError:
                        pass

        elif isinstance(obj, list):
            for item in obj:
                # 对列表中的每个元素递归搜索
                if isinstance(item, (dict, list)):
                    self.find_image_urls(item, urls)
                # 尝试解析可能的JSON字符串
                elif isinstance(item, str):
                    try:
                        nested_obj = json.loads(item)
                        self.find_image_urls(nested_obj, urls)
                    except json.JSONDecodeError:
                        if self.is_image_url(item):
                            urls.add(item)

        return urls

    def is_image_url(self, url):
        """判断URL是否为图片资源"""
        image_extensions = (".png", ".jpg", ".jpeg", ".gif", ".webp")
        url_lower = url.lower()

        # 检查URL是否包含图片扩展名
        if any(url_lower.endswith(ext) for ext in image_extensions):
            return True

        # 检查是否为相对路径格式的图片
        if url_lower.startswith(("images/", "icons/", "img/")):
            return True

        # 检查URL路径中是否包含images或icons关键词
        if any(path in url_lower for path in ["/images/", "/img/", "/icons/"]):
            return True

        return False

    def save_image(self, response):
        try:
            # 从URL中提取文件名
            url = response.meta.get("original_url", response.url)
            filename = os.path.basename(urlparse(url).path)

            # 如果文件名为空或没有扩展名，使用URL的最后部分
            if not filename or "." not in filename:
                filename = url.split("/")[-1]
                if "." not in filename:
                    # 根据content-type判断扩展名
                    content_type = (
                        response.headers.get("content-type", b"").decode().lower()
                    )
                    if "png" in content_type:
                        filename += ".png"
                    elif "jpeg" in content_type or "jpg" in content_type:
                        filename += ".jpg"
                    else:
                        filename += ".unknown"

            filepath = os.path.join(self.download_dir, filename)

            # 保存图片文件
            with open(filepath, "wb") as f:
                f.write(response.body)
            self.log(f"\033[32m保存图片: {filepath}\033[0m")

        except Exception as e:
            self.log(f"\033[31m保存图片失败 {url}: {str(e)}\033[0m")

    def errback(self, failure):
        url = failure.request.meta.get("original_url", failure.request.url)
        self.log(f"\033[31m下载失败: {url}\033[0m")
