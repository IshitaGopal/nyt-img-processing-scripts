import os
import pandas as pd

# Read in all the json
years = [2000, 2010, 2011, 2012]
dfs = []
for year in years:
    counter = 0
    dir = os.path.join("data/json/", str(year))
    fnames = os.listdir(dir)
    num_files = len(fnames)
    print(num_files)
    for fname in fnames:
        print(fname)
        data = pd.read_json(os.path.join(dir, fname))
        print(counter)
        print(
            f"{(counter+1)/num_files:.3f} proportion of files processed for year {year}"
        )
        counter += 1
        dfs.append(data)

# Concatenate all the dataframes
df = pd.concat(dfs, ignore_index=True)
df.columns
df.shape

# Save data
df.to_csv("data/processed/articles.csv", index=False)
