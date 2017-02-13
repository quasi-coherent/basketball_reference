import datetime

from scrapy import Item, Field

class UpcomingGamesItem(Item):
  date = Field(serializer=lambda d: datetime.datetime.strptime(d, "%a, %b %d, %Y %I:%M %p"))
  home_team = Field(serializer=str)
  away_team = Field(serializer=str)