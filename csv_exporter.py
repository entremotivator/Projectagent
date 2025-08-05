import pandas as pd

def export_to_csv(dataframe, filename):
    dataframe.to_csv(filename, index=False)


