import re
import preprocess
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
import pandas as pd
qnas=[]
def seprate(start,end,fpath):
    
    qna=[]
    student_dt=[]
    f=open(fpath,encoding="utf-8")
    for pos,lines in enumerate(f):
        if pos==start:
            line=re.sub(r'Question\:','',lines)
            line=re.sub(r'^\s+','',line)
            qna.append(line)
        if pos==start+1:
            line=re.sub(r'Answer\:','',lines)
            line=re.sub(r'^\s+','',line)
            qna.append(line)
        lis=[]
        if pos in range(start+3,end-1) and lines!='':
        
            try:
                id=re.search(r"\[([A-Za-z0-9_ ]+)\]",lines).group(1)
            except:
                id =None
               
            try:
                marks=re.match(r'\d.\d|\d',lines).group()
            except:
                marks=None

            try:
                ans=re.search(r"\]\s.*|\].*",lines).group()
            except:
                ans="None"

            lis.append(id)
            lis.append(marks)
            lis.append(ans[2:])
            student_dt.append(lis)
    
    student_ans_df=pd.DataFrame(student_dt,columns=['ID','Marks','Answer'])
    #print(student_ans_df)
    qna.append(student_ans_df)
    #print(qna)
    qnas.append(qna)
    #print(qnas)
    return qnas

def dfer_main(fpath):
    qnas=[]
    
    ind=0
    inds=[]
    f=open(fpath,encoding="utf-8")
    for line in f:
        ind+=1
        if(re.match(r'#{5,}|#{2,}\s',line)):
            inds.append(ind)
    f.close()

    f=open(fpath,encoding="utf-8")
    allines = f.read().splitlines()
    inds.append(len(allines))
    f.close()
    f=open(fpath,encoding="utf-8")
    textt=""
    for text in f:
        words=nltk.word_tokenize(text)
        words=preprocess.remove_non_ascii(words)
        words=TreebankWordDetokenizer().detokenize(words)
        textt+=words+'\n'
    f.close()

    f=open("data/newassign.txt",mode='a+',encoding="utf-8")
    f.truncate(0)
    f.write(textt)
    f.close

    for _ in range(len(inds)):
        indices=zip(inds,inds[1:])

    for i in indices:
        qnas=seprate(i[0],i[1],"data/newassign.txt")

    questions=pd.DataFrame(qnas,columns=['Question','Model_Ans','DF'])
    #print(questions)
    #cleaning dtatset
    for ans_df in questions.DF:
        ans_df.dropna(inplace=True)
        ans_df.reset_index(drop=True,inplace=True)
        #for i in range(len(ans_df.Answer)):
            #ans_df.Answer[i]=preprocess.normalize(ans_df.Answer[i])
        #print(ans_df)
    
    questions.to_pickle('dataframes/dataset.pickle')
    questions.to_csv('dataframes/dataset.csv')

def dfer_result(result):
    df= pd.read_pickle('dataframes/dataset.pickle')
    for i in range(len(df)):
        sid=df.DF[i].ID
        cal1=result[0]
        cal2=result[1]
        cal3=result[2]
        cal4=result[3]
        cal5=result[4]
        cal6=result[5]
        cal7=result[6]
        clis=[]
        for j in range(len(sid)):
            lis=[sid[j],cal1[j],cal2[j],cal3[j],cal4[j],cal5[j],cal6[j],cal7[j]]
            clis.append(lis)  
    rdf=pd.DataFrame(clis,columns=['SID','Q1','Q2','Q3','Q4','Q5','Q6','Q7'])
    rdf['SID'] = rdf['SID'].str.zfill(2)
    rdf=rdf.sort_values('SID')
    print(rdf)
    rdf.to_excel(r'C:/Users/manda/Desktop/result.xlsx',index=False)
