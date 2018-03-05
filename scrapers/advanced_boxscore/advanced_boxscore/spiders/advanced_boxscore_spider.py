from scrapy import Spider, Request

from advanced_boxscore.items import AdvancedBoxscoreItem
from advanced_boxscore.constants import TEAM_TABLE

class AdvancedBoxscoreSpider(Spider):
  _root = "https://www.basketball-reference.com"
  name = "advanced_boxscore"

  def __init__(self, season, month, today="", *args, **kwargs):
    super(AdvancedBoxscoreSpider, self).__init__(*args, **kwargs)
    self.today = today
    self.start_urls = [AdvancedBoxscoreSpider._root + "/leagues/NBA_%s_games-%s.html" 
      % (season, month)]

  def parse(self, response):
    for boxscore_link in response.xpath('//*[@id="schedule"]/tbody//td[6]/a/@href').extract():
      if (self.today and self.today in boxscore_link) or not self.today:
        yield Request(AdvancedBoxscoreSpider._root + boxscore_link, callback=self.parse_boxscore)
      else:
        continue

  def parse_boxscore(self, response):
    item = AdvancedBoxscoreItem()
    item["date"] = response.xpath('//*[@id="content"]/div[2]/div[3]/div[1]/text()').extract_first()
    item["home_team"] = response.xpath('//*[@id="content"]/div[2]/div[2]/div[1]/strong/a/text()').extract_first()
    item["away_team"] = response.xpath('//*[@id="content"]/div[2]/div[1]/div[1]/strong/a/text()').extract_first()
    # Two Charlotte Hornets teams have different table IDs
    if item["home_team"] == "Charlotte Hornets" and int(item["date"][-4:]) <= 2003:
      ht = "chh"
    else:
      ht = TEAM_TABLE[item["home_team"]]
    if item["away_team"] == "Charlotte Hornets" and int(item["date"][-4:]) <= 2003:
      at = "chh"
    else:
      at = TEAM_TABLE[item["away_team"]]
    item["home_score"] = response.xpath('//*[@id="content"]/div[2]/div[2]/div[2]/text()').extract_first()
    item["away_score"] = response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/text()').extract_first()
    _, _, item["home_ts"], item["home_efg"], item["home_3par"], item["home_ftr"], item["home_orb"], \
    item["home_drb"], item["home_trb"], item["home_ast"], item["home_stl"], item["home_blk"], item["home_tov"], _, \
    item["home_ortg"], item["home_drtg"] = response.xpath('//*[@id="box_%s_advanced"]/tfoot/tr//text()' % ht).extract()
    _, _, item["away_ts"], item["away_efg"], item["away_3par"], item["away_ftr"], item["away_orb"], \
    item["away_drb"], item["away_trb"], item["away_ast"], item["away_stl"], item["away_blk"], item["away_tov"], _, \
    item["away_ortg"], item["away_drtg"] = response.xpath('//*[@id="box_%s_advanced"]/tfoot/tr//text()' % at).extract()
    yield item