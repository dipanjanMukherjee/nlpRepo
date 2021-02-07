import os
import pandas as pd

os.chdir()
from nlg_build_commentary import *

def preprocess_data(nlg_df):
    nlg_df = nlg_df.set_index(['AccountCOde'], drop =false)
    nlg_df['variance'] = nlg_df['currentamount'] - nlg_df['comparisonamount']
    nlg_df['varianceP'] = (nlg_df['currentamount'] - nlg_df['comparisonamount'])/nlg_df['currentamount']
    nlg_df['variance_formatted'] = nlg_df['levellobname'].astype(str) + " " + "(" + nlg_df['variance'].astype(str) + "m" + ")"
    nlg_df['accountcode'] = nlg_df['accountcode'].astype(str)
    nlg_df['total_variance'] = nlg_df.groupby(['accountcode'])['variance'].sum()
    nlg_df['variance_formatted'] = nlg_df['variance_formatted'].astype(str)
    nlg_df['flag'] = nlg_df['variance'].apply(lambda x: "P" if x >0 else "N")
    DF = nlg_df.set_index(['accountcode', 'flag'], drop = False)
    DF['variance_formatted_rollup'] = nlg_df.groupby(['accountcode', 'flag'])['variance_formatted'].apply(list)
    return DF

if __name__ == '__main__':
    nlg_df = pd.read_csv("filtervar.csv")
    nlg_df= (pd.read_csv("filtervar.csv").query('Region == ["US,"Europe"] & lelvellobname == ["GMNS","GCS"]'))
    processed_df = preprocess_data(nlg_df)
    processed_df["c1"] = ""
    processed_df["c2"] = ""
    processed_df["c3"] = ""
    processed_df["c4"] = ""
    for i in range(1, len(processed_df)):
        variance_roll_up = processed_df.variance_formatted_rollup[i]
        processed_df.variance_formatted_rollup[i] = ''.join(map(lambda x: x+' ,', variance_roll_up[0:-1]))[:-1]+ " and " + variance_roll_up[-1]
        processed_df.c1[i], processed_df.c2[i], processed_df.c3[i] = build_comments(processed_df.accountcode[i], processed_df.flag[i], processed_df.total_variance[i], processed_df.variance_formatted_rollup[i])
        processed_df['c4'] = processed_df[['c1', 'c2', 'c3']].apply(lambda x: ''.join(x), axis =1 )