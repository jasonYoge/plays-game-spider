import sys

from scrapy.crawler import CrawlerProcess

from spiders.image_spider import ImageSpider


def parse_args() -> dict[str, str | bool]:
    """解析命令行参数，例如 --url=xxx --dir=xxx"""
    args = sys.argv[1:]
    arg_dict: dict[str, str | bool] = {}
    for arg in args:
        if arg.startswith("--"):
            if "=" in arg:
                key, value = arg[2:].split("=", 1)
                arg_dict[key] = value
            else:
                arg_dict[arg[2:]] = True
    return arg_dict


def main() -> None:
    args = parse_args()
    # 默认URL
    start_urls = ["https://plays.org/game/super-pix/data.json"]
    # 默认下载目录
    download_dir = "download/images"
    # 如果有传入--url参数，则替换默认URL
    if "url" in args and isinstance(args["url"], str):
        start_urls = [args["url"]]
    # 如果有传入--dir参数，则替换默认下载目录
    if "dir" in args and isinstance(args["dir"], str):
        download_dir = args["dir"]

    process = CrawlerProcess(
        {
            "USER_AGENT": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }
    )

    # 将download_dir作为参数传递给ImageSpider
    process.crawl(ImageSpider, start_urls=start_urls, download_dir=download_dir)
    process.start()


if __name__ == "__main__":
    main()
