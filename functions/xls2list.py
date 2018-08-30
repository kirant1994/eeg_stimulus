import pandas as pd
import numpy as np

def xls2list(filename):
    df = pd.read_excel(filename)
    prompts = df.values
    lst = list()
    for i in range(len(prompts)):
        lst.append(prompts[i, :])
    return lst