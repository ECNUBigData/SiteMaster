#-*- coding: utf-8 -*-
#@Time: 2024/3/12
#@File: findLoc.py

import csv
import pandas as pd

def findLoc(long_text: str):
    csv_filename = './locationDataset/Shanghai.csv'
    with open(csv_filename, 'r',encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        df = pd.DataFrame({})
        if "SiteMaster" not in long_text:
            for field_info in csv_reader:
                if field_info[0] in long_text:
                    df=df._append({'name': field_info[0], 'lon': float(field_info[1]), 'lat': float(field_info[2])}, ignore_index=True)

    return df
