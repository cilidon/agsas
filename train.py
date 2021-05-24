import nltk
from collections import Counter
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize, word_tokenize
from fuzzywuzzy import process
import pandas as pd
import re
from scipy.stats import pearsonr
import string
from nltk.stem.porter import *
import Input as intu
import eblue_main as blue
stemmer = PorterStemmer()
p=""
pm=""
pmans=""
pid=""
pans=""
df=[]
dfq=[]
def intui(fres):
	x=stopwords.words('english')
	ss =[]
	stop_words = set(x) 
	top=list()
	ftsi= list()
	count= list()
	score= list()
	di={}
	ss.clear()
	top.clear()
	ftsi.clear()
	count.clear()
	score.clear()
	di.clear()
	for i in fres:
		
		t= i[0]
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
		ftsi.append([ x for x in ti if not x in stop_words])
		
	#print(ftsi)
	count = Counter()
	for h in ftsi:
		for hi in h:
			hi=hi.upper()
			count[hi] += 1
		top=[seq[0] for seq in count.most_common(20)]

	for j in ftsi:
		aa=[stemmer.stem(word) for word in top]
		temp=[]
		for ii in j:
			t = ii.upper()
			temp.append(stemmer.stem(t))
		c= list(set(aa).intersection(temp))
		count=len(c)
		for key in c:
			if key in di.keys():
				count=count + (di[key]-1)
		score.append(count)
	
	for j in score:
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
	return ss
	
	
	
	
def train(filename,filename2):
	
	df.clear()
	dfq.clear()
	intu.dff(filename2)
	i=-1
	with open(filename,errors="ignore") as f:
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
	qtrain=[]
	qmain=[]
	
	for i in dfq:
		qtrain.append(i[0])
	for i in intu.dfq:
		qmain.append(i[0])
	print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",len(qmain))
	falphal=[]	
	#scoreblue =[[4, 3.5, 3.5, 5, 4.5, 2, 3, 3, 4, 3, 3], [2, 3, 2.5, 2.5, 1.5, 3.5, 5, 2.5, 3.5, 2.5, 4.5], [5, 4.5, 3, 4.5, 3, 3.5, 3, 3.5, 2.5, 2.5, 5], [5, 5, 4, 5, 5, 4.5, 4, 3.5, 5, 5, 4.5], [3.5, 5, 4, 5, 5, 3.5, 5, 4.5, 3.5, 3.5, 4], [2.5, 2, 4.5, 3, 2.5, 2.5, 3.5, 3, 2.5, 2.5, 5]]
	scoreblue =[[4, 3, 3.5, 5, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2.5, 4, 2, 3, 3, 2.5], [2.5, 4, 4, 5, 3, 5, 3, 3.5, 4, 4.5, 2, 3.5, 4.5, 5], [3.5, 5, 4, 4.5, 3, 5, 2.5, 3, 3.5, 2.5, 2.5, 3, 3, 3.5, 4, 3.5], [4, 3.5, 4, 4.5, 3.5, 3, 2.5, 3.5, 2.5, 3, 5], [2.5, 5, 2.5, 2, 2, 2, 1.5, 2, 2, 2, 1.5, 1.5], [3.5, 3.5, 4.5, 1, 5, 5, 4, 3.5, 4, 4, 3.5, 3.5, 3, 3, 3, 3, 2.5, 3.5, 3]]
	ind=0
	ccc=0
	for q in qmain:
		ratio = process.extractOne(q,qtrain,score_cutoff = 100)
		ccc=ccc+1
		if ratio is not None:
			
			overall=[]
			position = qtrain.index(ratio[0])
			position1 = qmain.index(ratio[0])
			print('''
			quss
	
		''',ccc)
			#print(df[position].answer)
			for n in intu.df[position1].answer:
				result=process.extractOne(n,df[position].answer,score_cutoff = 90)
				#print(df[position].answer)
				#print(n)
				if result is not None:
					
					
					first =df[position].index[df[position]["answer"] == result[0]].tolist()
					res=[result[0] , df[position].at[first[0],'marks']]
					overall.append(res)
			fres = []
			for i in overall:
				if i not in fres:
					fres.append(i)
			

			print(len(fres))
			ffres=[x[0] for x in fres]
			print(dfq[position][1])
			print(len(ffres))
			if len(fres) !=0:
				score = intui(fres)
				score2= blue.eblue_init2(dfq[position][1],ffres)
				print(score2)
				#score2=scoreblue[ind]
			#	print(scoreblue[ind])
				ind = ind + 1
				alphal=[]
				al=[]
				
				for j in range(0,11,1):
					print('''
			
			ind
			''',ind)
					alpha = j/10
					fscore=[score[x]*alpha + score2[x]*(1-alpha) for x in range (len (score)) ]
				
					print(fscore)
					tscore=[float(fres[x][1]) for x in range(len(fres))]
					print(tscore)
					corr, _ = pearsonr(fscore, tscore)
					alphal.append(corr)
					print(corr)
					al.append(alpha)
				#print(alphal)

				falpha=alphal.index(max(alphal))
				#print(alphal)
				falpha=al[falpha]
				#falpha = (falpha+1)/10
			else:
				falpha=0.4
		else:
			falpha=0.4
		falphal.append(falpha)
	return falphal

