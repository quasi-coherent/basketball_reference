import datetime

from scrapy import Item, Field

class AdvancedBoxscoreItem(Item):
  date = Field(serializer=lambda d: datetime.datetime.strptime(d, "%I:%M %p, %B %d, %Y"))
  home_team = Field(serializer=str)
  home_score = Field(serializer=int)
  home_ts = Field(serializer=float) # true shooting percentage
  home_efg = Field(serializer=float) # effective field goal percentage
  home_3par = Field(serializer=float) # 3-point attempt rate
  home_ftr = Field(serializer=float) # free throw rate
  home_orb = Field(serializer=float) # offensive rebound rate
  home_drb = Field(serializer=float) # defensive rebound rate
  home_trb = Field(serializer=float) # total rebound percentage
  home_ast = Field(serializer=float) # assist percentage
  home_stl = Field(serializer=float) # steal percentage
  home_blk = Field(serializer=float) # block percentage
  home_tov = Field(serializer=float) # turnover rate
  home_ortg = Field(serializer=float) # offensive rating
  home_drtg = Field(serializer=float) # defensive rating
  away_team = Field(serializer=str)
  away_score = Field(serializer=int)
  away_ts = Field(serializer=float)
  away_efg = Field(serializer=float)
  away_3par = Field(serializer=float)
  away_ftr = Field(serializer=float)
  away_orb = Field(serializer=float)
  away_drb = Field(serializer=float)
  away_trb = Field(serializer=float)
  away_ast = Field(serializer=float)
  away_stl = Field(serializer=float)
  away_blk = Field(serializer=float)
  away_tov = Field(serializer=float)
  away_ortg = Field(serializer=float)
  away_drtg = Field(serializer=float)
  