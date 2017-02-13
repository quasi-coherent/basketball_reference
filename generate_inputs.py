#!/usr/bin/env python

def main(seasons, months):
  with open("../resources/inputs.txt", "w") as f:
    for season in seasons:
      for month in months:
        f.write(season + " " + month + "\n")

if __name__ == "__main__":
  seasons = ["200" + str(i) for i in range(1, 10)] + ["20" + str(i) for i in range(10, 18)]
  months = ["october", "november", "december", "january", "february", "march", "april", "may", "june"]
  main(seasons, months)