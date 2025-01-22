import pandas as pd
import re
import json


df = pd.read_csv("/home/multi-sy-23/Downloads/merge_csv/Netball-Ball-Detection-20-01-2025-12-08-52.csv")

new = df.drop_duplicates(subset=['Source Url'])

new.to_csv("newdata.csv")

# df1 = pd.DataFrame({
#     'A': [1, 2, 3],
#     'B': ['a', 'b', 'c']
# })

# df2 = pd.DataFrame({
#     'A': [4, 2, 3],
#     'B': ['d', 'b', 'c']
# })

# # Merge DataFrames and remove duplicates
# merged_df = pd.merge(df1, df2, how='outer').drop_duplicates()
# print(merged_df)  