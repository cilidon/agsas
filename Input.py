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
def dff(filename):
	df.clear()
	dfq.clear()
	i=-1
	with open(filename,encoding="utf8") as f:
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
#data = [['Alex',10],['Bob',12],['Clarke',13]]
#df = pd.DataFrame(data,columns=['Name','Age'])
#print df
