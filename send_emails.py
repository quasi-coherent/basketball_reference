#!/usr/bin/env python
import datetime
import os
import sys
import pandas as pd

from util.util import send_email, prepare_dates

try:
  print sys.argv[1]
except IndexError:
  sys.stdout.write("Usage: python send_emails.py date")
  sys.exit(1)

today, _, _ = prepare_dates(sys.argv[1])

if not os.path.isfile("tmp/predictions_%s.csv" % today):
  sys.stdout.write("Predictions for %s haven't been made yet..." % today)
  sys.exit(1)

# read in and prepare prediction/metrics dfs
project_dir = os.environ["PROJECT_DIR"]
predictions = pd.read_csv(project_dir + "tmp/predictions_%s.csv" % today)
predictions["date"] = pd.to_datetime(predictions["date"])
predictions = predictions.sort_values(by="date").reset_index(drop=True)
metrics = pd.read_csv(project_dir + "data/metrics.csv")

# send email with predictions/historical metrics
send_from = "d.michael.donohue@gmail.com"
send_to = ["d.michael.donohue@gmail.com"]#, "jesse.prestwoodtaylor@gmail.com"]
subject = "NBA Predictions %s" % datetime.datetime.strptime(today, "%Y%m%d").strftime("%m-%d-%Y")
text = "Predictions for games happening on %s (all times Eastern): <br><br>" % datetime.datetime.strptime(today, "%Y%m%d").strftime("%m-%d-%Y")
text += predictions.to_html()
text += "<br> Notes:"
text += "<ul><li> Spread is from the perspective of the home team, e.g., -4 means the home team is predicted to lose by 4.</li>"
text += "<li> A '1' in the moneyline column means that the home team is predicted to win; '0' means they are predicted to lose.</li></ul>"
text += "10-fold cross validation scores:<br><br>"
text += metrics.to_html()
text += "<br>Disclaimers:"
text += "<ul><li>This doesn't take into account injuries, roster moves, or schedule oddities (e.g., back-to-back, long road trips, etc.).</li>"
text += "<li>Use this only as a rough guide and a supplement to personal research.</li></ul>"

send_email(send_from=send_from, send_to=send_to, subject=subject, text=text)
