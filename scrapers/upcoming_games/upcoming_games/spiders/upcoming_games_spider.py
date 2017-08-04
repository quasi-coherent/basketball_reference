from scrapy import Spider, Request

from datetime import datetime
from bs4 import BeautifulSoup

from upcoming_games.items import UpcomingGamesItem

class UpcomingGamesSpider(Spider):
  _root = "http://www.basketball-reference.com"
  name = "upcoming_games"

  def __init__(self, season, month, today, *args, **kwargs):
    super(UpcomingGamesSpider, self).__init__(*args, **kwargs)
    self.today = today
    self.start_urls = [UpcomingGamesSpider._root + "/leagues/NBA_%s_games-%s.html" 
      % (season, month)]

  def parse(self, response):
    for game in response.xpath('//*[@id="schedule"]/tbody//tr').extract():
      soup = BeautifulSoup(game, "html.parser")
      date = soup.th.text
      try:
        dt = datetime.strptime(date, "%a, %b %d, %Y")
      except ValueError: # skip rows that are headers
        continue
      if dt == datetime.strptime(self.today, "%Y%m%d"):
        item = UpcomingGamesItem()
        time = soup.find("td", attrs={"data-stat": "game_start_time"}).text
        date_time = " ".join([date, time])
        item["date"] = date_time
        item["home_team"] = soup.find("td", attrs={"data-stat": "home_team_name"}).text
        item["away_team"] = soup.find("td", attrs={"data-stat": "visitor_team_name"}).text
        yield item
      else:
        continue