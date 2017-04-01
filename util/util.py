import datetime
import os
import smtplib
import subprocess

from email.utils import COMMASPACE, formatdate
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(send_from, send_to, subject, text):
  assert isinstance(send_to, list)
  msg = MIMEMultipart()
  msg["From"] = send_from
  msg["To"] = COMMASPACE.join(send_to)
  msg["Date"] = formatdate(localtime=True)
  msg["Subject"] = subject
  msg.attach(MIMEText(text, "html"))
  smtp = smtplib.SMTP(os.environ["SMTP_ENDPOINT"], int(os.environ["SMTP_PORT"]))
  smtp.starttls()
  smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
  smtp.sendmail(send_from, send_to, msg.as_string())
  smtp.close()

def launch_spider(spider_name, season, month, project_dir, data_dir, today=""):
  if today:
    name = spider_name + "_" + today + ".json"
  else:
    name = str(season) + "_" + month + ".json"
  subprocess.call(["scrapy", "crawl", spider_name,
    "-a", "season=%s" % season, 
    "-a", "month=%s" % month,
    "-a" , "today=%s" % today,
    "--set", "FEED_URI=%s%s%s" % (project_dir, data_dir, name),
    "--set", "FEED_FORMAT=jsonlines"],
    cwd=project_dir + "scrapers/" + spider_name +"/")

def prepare_dates(date):
  try:
    datetime.datetime.strptime(date, "%Y%m%d")
  except ValueError:
    print "Improper datetime format: %s. Expected: YYYYMMDD." % date
  today = datetime.datetime.strptime(date, "%Y%m%d")
  season = today.year if today.month in range(1, 7) else now.year + 1
  month = today.strftime("%B").lower()
  return today.strftime("%Y%m%d"), month, season