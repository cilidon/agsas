import nltk
from collections import Counter
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import *
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

import pandas as pd
import re
import string
p=""
pm=""
pmans=""
pid=""
pans=""
df=[]
dfq=[]
stemmer = PorterStemmer()

def intuitive(filename):
	df.clear()
	dfq.clear()
	i=-1
	with open(filename, errors="ignore") as f:
		for line in f:
			import re
			if re.search("^#+", line):
				i=i+1
				if i>0:
					temp=[p,pmans]
					dfq.append(temp)
				df.append( pd.DataFrame(columns = [ 'sid','marks','answer']) )
			elif re.search("Question:", line):
				p = re.sub("Question:",'', line)
				p = re.sub(' +'," ",p).strip()
			elif re.search("Answer:", line):
				pmans = re.sub("Answer:",'', line)
				pmans = re.sub(' +'," ",pmans).strip()
			elif re.search("^\d", line):
				ps = re.split("\t", line)
				pm = ps[0]
				pid =  ps[1]
				pans= ps[2]
				exclist = string.punctuation #removes [!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~]
				table_ = pid.maketrans('', '', exclist)
				pid = pid.translate(table_)
				if len(pid)==1:
					pid = '0'+pid
				data = [pid,pm,pans.lower()]
				df[i].loc[len(df[i].index)] = data
		temp=[p,pmans]
		dfq.append(temp)
		df.append( pd.DataFrame(columns = [ 'sid','marks','answer']) )
	x=stopwords.words('english')
	scoreint =[]
	stop_words = set(x) 
	top=list()
	ftsi= list()
	count= list()
	score= list()
	di={}
	scoreint.clear()
	top.clear()
	ftsi.clear()
	count.clear()
	score.clear()
	di.clear()
	for i in range(0,len(dfq)):
		tsi=[]
		for j in range(0,len(df[i].index)):
			t= df[i].at[j,'answer']
			tokenizer = nltk.RegexpTokenizer(r"\w+")
			ti = tokenizer.tokenize(t)
			tii = nltk.pos_tag(ti)
			for gram in tii:
				if len(gram)>=2:
					if gram[1]=="NNP" :
						di[gram[0]] = 3
					elif gram[1]=="VB" or gram[1]=="NN" :
						di[gram[0]] = 2
					elif gram[1]=="CD" :
						di[gram[0]] = 2
			tsi.append([ x for x in ti if not x.lower() in stop_words])
			
		ftsi.append([tsi])
	for i in range(0,len(dfq)):
		count = Counter()
		for h in ftsi[i][0] :
			for hi in h:
				hi=hi.upper()
				count[hi] += 1
			temp=[seq[0] for seq in count.most_common(20)]
		top.append(temp)
	for i in range(0,len(dfq)):
		ss=[]
		cc=[stemmer.stem(word) for word in top[i]]
		for j in range(0,len(df[i].index)):
			temp=[]
			for ii in ftsi[i][0][j]:
				t = ii.upper()
				temp.append(stemmer.stem(t))
			c= list(set(cc).intersection(temp))
			count=len(c)
			for key in c:
				if key in di.keys():
					count=count + (di[key]-1)
			ss.append(count)
			
		score.append(ss)
		
	for i in range(0,len(dfq)):
		ss=[]
		for j in score[i]:
			if j>15:
				ss.append(5)
			elif j>10:
				ss.append(4.5)
			elif j>8:
				ss.append(4.0)
			elif j>5:
				ss.append(3.5)
			elif j>3:
				ss.append(2.5)
			elif j>0:
				ss.append(2)
			elif j==0:
				ss.append(0)
			
		scoreint.append(ss)
	return scoreint

#print(intuitive("assign1.txt"))
