import os
import pandas as pd
os.chdir("/paraphraser model")
from build_synonyms import *

"""generates the paraphrased sentences leveraging wordnet of nltk, however
paraphrased words are not in line with finance reporting vocabulary"""

def paraphraser_comments():

    comments = pd.read_csv("commentary.csv", header =0, encoding ='unicode_escape')
    commentary= pd.DataFrame()
    num_comments = comments["Comments"].size

    commentary["P_comments"] = ""
    paraphrased_comments = []

    for i in range (0, num_comments):
        paraphrased_comments = build_synonyms(comments["comments"][i])
        df1 = pd.DataFrame(list(paraphrased_comments))
        df1.columns = ['P_comments', 'Confidence']
        df1['O_comments'] = comments["comments"][i]
        commentary = commentary.append(df1)
        commentary.to_csv("commentary_output.csv")

if __name__ == '__main__':
    paraphraser_comments()