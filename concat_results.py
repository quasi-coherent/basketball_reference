#!/usr/bin/env python
import pandas as pd
import glob

files = glob.glob("tmp/*.json")
dfs = [pd.read_json(file, lines=True) for file in files]
dfs_concat = pd.concat(dfs)
all_boxscores = pd.read_json("data/all_boxscores_2001-2018.json", lines=True)
result = pd.concat([all_boxscores, dfs_concat]).drop_duplicates()
result.to_json("all_boxscores_2001-2018_tmp.json", lines=True, orient="records")
