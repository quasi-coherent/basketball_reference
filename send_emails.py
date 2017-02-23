#!/usr/bin/env python
import datetime
import os
import smtplib
import sys
import pandas as pd
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

if __name__ == "__main__":
  # inputs
  project_dir = os.getcwd() + "/"
  now = datetime.datetime.now()
  if len(sys.argv) > 1:
    today = sys.argv[1]
  else:
    today = now.strftime("%Y%m%d")

  # read in and prepare prediction/metrics dfs
  sys.stdout.write("Reading in predictions/metrics...\n")
  sys.stdout.flush()
  predictions = pd.read_csv(project_dir + "resources/predictions_%s.csv" % today)
  if predictions.shape[0] == 0:
    sys.stdout.write("No games today...\n")
    sys.stdout.flush()
    sys.exit(0)
  predictions["date"] = pd.to_datetime(predictions["date"])
  predictions = predictions.sort_values(by="date").reset_index()
  metrics = pd.read_csv(project_dir + "data/metrics.csv")

  # send email with predictions/historical metrics
  send_from = "d.michael.donohue@gmail.com"
  send_to = ["d.michael.donohue@gmail.com"]
  subject = "NBA Predictions %s" % datetime.datetime.strptime(today, "%Y%m%d").strftime("%m-%d-%Y")
  text = "Predictions for games happening on %s (all times Eastern): <br><br>" % datetime.datetime.strptime(today, "%Y%m%d").strftime("%m-%d-%Y")
  text += predictions.to_html()
  text += "<br> Notes:"
  text += "<ul><li> Spread is from the perspective of the home team, e.g., -4 means the home team is predicted to lose by 4.</li>"
  text += "<li> A '1' in the moneyline column means that the home team is predicted to win; '0' means they are predicted to lose.</li></ul>"
  text += "Historical model metrics:<br><br>"
  text += metrics.to_html()
  text += "<br>Disclaimers:"
  text += "<ul><li>This doesn't take into account injuries, schedule oddities (e.g., back-to-back, long road trips, etc.).</li>"
  text += "<li>Use this only as a rough guide and a supplement to personal research.</li></ul>"

  send_email(send_from=send_from, send_to=send_to, subject=subject, text=text)
  sys.stdout.write("Emails sent...\n")
  sys.stdout.flush()