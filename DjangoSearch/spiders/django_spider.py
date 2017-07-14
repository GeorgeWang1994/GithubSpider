from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy_splash import SplashRequest
from collections import defaultdict
from ..settings import SPIDER_SEARCH_CONTENT, SPIDER_SEARCH_GLOBAL_TYPE, SPIDER_SEARCH_DOMAIN
from ..settings import SEARCH_TYPE
from ..settings import USER_COOKIE, USER_HEADRE
from ..items import GitRepoItem, GitUserItem, GitTagItem, ITEMTYPE
from ..utils.select_result import list_first_str, list_str_at, list_first_item, list_item_at
import scrapy_splash


class SearchSpider(CrawlSpider):
    name = "SearchSpider"
    allowed_domains = ["github.com"]

    def start_requests(self):
        for search in SPIDER_SEARCH_CONTENT:
            if "type" not in search:
                url = SPIDER_SEARCH_DOMAIN + "/search?q=" + search[
                    "search"] + "&ref=simplesearch&type=Repositories&utf8=%E2%9C%93"
                yield SplashRequest(url=url, callback=self.parse_repos,
                                    args={
                                        # optional; parameters passed to Splash HTTP API
                                        'wait': 2,
                                        "headers": USER_HEADRE,
                                        # 'url' is prefilled from request url
                                        # 'http_method' is set to 'POST' for POST requests
                                        # 'body' is set to request body for POST requests
                                    },
                                    endpoint='render.json',  # optional; default is render.html
                                    # splash_url='<url>',  # optional; overrides SPLASH_URL
                                    slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                                    )
            elif search["type"] == SEARCH_TYPE.REPO:
                url = SPIDER_SEARCH_DOMAIN + "/search?q=" + search["search"] + "&ref=simplesearch&type=Repositories&utf8=%E2%9C%93"
                yield SplashRequest(url=url, callback=self.parse_repos,
                                    args={
                                        # optional; parameters passed to Splash HTTP API
                                        'wait': 2,
                                        "headers": USER_HEADRE,
                                        # 'url' is prefilled from request url
                                        # 'http_method' is set to 'POST' for POST requests
                                        # 'body' is set to request body for POST requests
                                    },
                                    endpoint='render.json',  # optional; default is render.html
                                    # splash_url='<url>',  # optional; overrides SPLASH_URL
                                    slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                                    )
            elif search["type"] == SEARCH_TYPE.USER:
                url = SPIDER_SEARCH_DOMAIN + "/search?q=" + search["search"] + "&ref=simplesearch&type=Users&utf8=%E2%9C%93"
                yield SplashRequest(url=url, callback=self.parse_users,
                                    args={
                                        # optional; parameters passed to Splash HTTP API
                                        'wait': 2,
                                        "headers": USER_HEADRE,
                                        # 'url' is prefilled from request url
                                        # 'http_method' is set to 'POST' for POST requests
                                        # 'body' is set to request body for POST requests
                                    },
                                    endpoint='render.json',  # optional; default is render.html
                                    # splash_url='<url>',  # optional; overrides SPLASH_URL
                                    slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                                    )

    def parse_repos(self, response):
        print(response.headers)
        selector = Selector(response).xpath('//ul[@class="repo-list js-repo-list"]').css('div.repo-list-item')

        for data in selector:
            repo = GitRepoItem()
            pre_data = data.xpath('div[@class="col-8 pr-3"]')
            repo["type"] = ITEMTYPE.GitRepoItem
            repo["name"] = list_first_str(pre_data.xpath('h3/a/@href').extract()).replace('/', '', 1)
            repo["url"] = SPIDER_SEARCH_DOMAIN + list_first_str(pre_data.xpath('h3/a/@href').extract())
            repo["summary"] = list_first_str(pre_data.xpath('p/text()').extract())
            tag_data = pre_data.xpath('div[@class="topics-row-container col-9 d-inline-flex flex-wrap flex-items-center f6 my-1"]').css('a.topic-tag')
            repo["tags"] = defaultdict(str)
            for d in tag_data:
                tag = GitTagItem()
                tag["type"] = ITEMTYPE.GitTagItem
                tag["url"] = SPIDER_SEARCH_DOMAIN + list_first_str(d.xpath('@href').extract())
                tag["name"] = list_first_str(d.xpath('text()').extract())
                repo["tags"][tag["name"]] = tag

                yield tag
            repo["lasttime"] = 'Updated ' + list_first_str(pre_data.xpath('//relative-time/text()').extract())
            repo["language"], repo["starnum"] = '', ''
            if len(data.xpath('div[@class="d-table-cell col-2 text-gray pt-2"]/text()').extract()) > 1:
                repo["language"] = list_str_at(data.xpath('div[@class="d-table-cell col-2 text-gray pt-2"]/text()').extract(), 1)
            if len(data.xpath('div[@class="col-2 text-right pt-1 pr-3 pt-2"]/a[@class="muted-link"]/text()').extract()) > 1:
                repo["starnum"] = list_str_at(data.xpath('div[@class="col-2 text-right pt-1 pr-3 pt-2"]/a[@class="muted-link"]/text()').extract(), 1)
            yield repo

        page_data = Selector(response).xpath('//div[@class="pagination"]')
        if list_first_item(page_data.xpath('.//a[@class="next_page"]')):
            url = SPIDER_SEARCH_DOMAIN + list_first_str(page_data.xpath('.//a[@class="next_page"]/@href').extract())
            yield SplashRequest(url=url, callback=self.parse_repos,
                                args={
                                    # optional; parameters passed to Splash HTTP API
                                    'wait': 2,
                                    "headers": USER_HEADRE,
                                    # 'url' is prefilled from request url
                                    # 'http_method' is set to 'POST' for POST requests
                                    # 'body' is set to request body for POST requests
                                },
                                endpoint='render.json',  # optional; default is render.html
                                # splash_url='<url>',  # optional; overrides SPLASH_URL
                                slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                                )

    def parse_users(self, response):
        print(response.headers)
        selector = Selector(response).xpath('//div[@class="user-list"]').css('div.user-list-item')
        self.user_count = Selector(response).xpath('//div[@class="d-flex flex-justify-between border-bottom pb-3"]/h3/text()').extract_first().strip()

        print("一共有" + self.user_count)

        for data in selector:
            user = GitUserItem()
            pre_data = data.xpath('div[@class="d-flex"]')
            user["type"] = ITEMTYPE.GitUserItem
            user["avatar"] = SPIDER_SEARCH_DOMAIN + list_first_str(pre_data.xpath('a/img/@src').extract())
            info_data = pre_data.xpath('div[@class="user-list-info ml-2"]')
            user["name"] = list_first_str(info_data.xpath('a/@href').extract()).replace('/', '', 1)
            user["url"] = SPIDER_SEARCH_DOMAIN + list_first_str(info_data.xpath('a/@href').extract())
            user["intro"] = list_first_str(info_data.xpath('p/text()').extract())
            down_data = info_data.xpath('ul//li')
            user["location"], user["email"] = '', ''
            for d in down_data:
                if list_first_item(d.xpath('svg[@class="octicon octicon-location"]').extract()):
                    user["location"] = list_str_at(d.xpath('text()').extract(), 1)
                elif list_first_item(d.xpath('svg[@class="octicon octicon-mail"]').extract()):
                    user["email"] = list_first_str(d.xpath('a/text()').extract())
            yield user

        page_data = Selector(response).xpath('//div[@class="pagination"]')
        if list_first_item(page_data.xpath('.//a[@class="next_page"]')):
            url = SPIDER_SEARCH_DOMAIN + list_first_str(page_data.xpath('.//a[@class="next_page"]/@href').extract())
            yield SplashRequest(url=url, callback=self.parse_users,
                                args={
                                    # optional; parameters passed to Splash HTTP API
                                    'wait': 2,
                                    "headers": USER_HEADRE,
                                    # 'url' is prefilled from request url
                                    # 'http_method' is set to 'POST' for POST requests
                                    # 'body' is set to request body for POST requests
                                },
                                endpoint='render.json',  # optional; default is render.html
                                # splash_url='<url>',  # optional; overrides SPLASH_URL
                                slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                                )
