import re 
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
import preprocess
import pandas as pd
from ast import literal_eval
import eblue2 as eblue
import dfer

def eblue_init(fpath):

    #creating DataFrame
    dfer.dfer_main(fpath)

    # Data Reading
    df= pd.read_pickle('dataframes/dataset.pickle')

    #cleaning dtatset
    for ans_df in df.DF:
        ans_df.dropna(inplace=True)
        ans_df.reset_index(drop=True,inplace=True)
        #print(ans_df)
            
    #preprocessing dataset
    for ans_dfs in df.DF:
        for i in range(len(ans_dfs.Answer)):
            ans_dfs.Answer[i]=preprocess.normalize(ans_dfs.Answer[i])

    # Ehnaced Bleu Method 
    total_answer=0
    corect_match=0
    final_marks_List=[]
    final_marks_List.clear()
    print("len of kist is:  " ,len(final_marks_List))
    for j in range(len(df)):
        matches=[]
        #q=df.Question[j]
        #a=df.Model_Ans[j]
        dfs=df.DF[j]
        # displaying in proper format
        #print("Question : ",q)
        #print("Model Answer : ",a)
        #print("Actual Score\tCalculated Score")

        for i in range(len(dfs.Answer)):
            matches.append(eblue.process(dfs.Answer[i],df.Model_Ans[j]))
            total_answer+=1
        matches=eblue.matches_to_marks(matches)
        final_marks_List.append(matches)
        
    
    return final_marks_List
    

def eblue_init2(main,answers):
    total_answer=0
    fanswers = [preprocess.normalize(x) for x in answers]
    for j in range(len(fanswers)):
        matches=[]
        #q=df.Question[j]
        #a=df.Model_Ans[j]
        # displaying in proper format
        #print("Question : ",q)
        #print("Model Answer : ",a)
        #print("Actual Score\tCalculated Score")

        for i in range(len(fanswers)):
            matches.append(eblue.process(fanswers[i],main))
            total_answer+=1
        matches=eblue.matches_to_marks(matches)
    return matches
