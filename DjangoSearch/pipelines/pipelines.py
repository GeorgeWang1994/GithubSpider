from pymongo import MongoClient
from ..settings import MONGODB_SERVER, MONGODB_PORT, MONGODB_DB
from ..utils.select_result import get_linkmd5id, generateRandomID
from ..items import ITEMTYPE
import logging


class DjangosearchPipeline(object):
    def __init__(self):
        try:
            self.client = MongoClient(MONGODB_SERVER, MONGODB_PORT)
            self.db = self.client[MONGODB_DB]
        except Exception as e:
            print("Exception:%s"%str(e))

    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('MONGODB_SERVER', 'localhost')
        cls.MONGODB_PORT = crawler.settings.getint('MONGODB_PORT', 27017)
        cls.MONGODB_DB = crawler.settings.get('MONGODB_DB', 'djangosearch')
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item["type"] == ITEMTYPE.GitRepoItem:
            self.process_repo_item(item)
        elif item["type"] == ITEMTYPE.GitTagItem:
            self.process_tag_item(item)
        elif item["type"] == ITEMTYPE.GitUserItem:
            self.process_user_item(item)

    def process_repo_item(self, item):
        if not item["name"] and self.db["repo"].find_one({'name': item["name"]}):
            return

        repo_detail = {
            'id': generateRandomID(),
            'url': item["url"],
            'name': item["name"],
            'summary': item["summary"],
            'tags': item["tags"],
            'lasttime': item["lasttime"],
            'language': item["language"],
            'starnum' : item["starnum"]
        }

        self.db["repo"].insert(repo_detail)
        logging.info('Repo ' + item.detail() + ' have added successfully')

    def process_user_item(self, item):
        if not item["name"] and self.db["user"].find_one({'name': item["name"]}):
            return

        user_detail = {
            'id': generateRandomID(),
            'url': item["url"],
            'name': item["name"],
            'intro': item["intro"],
            'avatar': item["avatar"],
            'location': item["location"],
            'email': item["email"]
        }
        self.db["user"].insert(user_detail)
        logging.info('User ' + item.detail() + ' have added successfully')

    def process_tag_item(self, item):
        if not item["name"] and self.db["tag"].find_one({'name': item["name"]}):
            return

        tag_detail = {
            'id': generateRandomID(),
            'url': item["url"],
            'name': item["name"],
        }
        self.db["tag"].insert(tag_detail)
        logging.info('Tag ' + item.detail() + ' have added successfully')