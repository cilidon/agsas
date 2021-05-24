import preprocess
from fuzzywuzzy import fuzz
from nltk.corpus import wordnet
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pandas as pd
from scipy import spatial
import scipy.stats
from nltk.sentiment import SentimentIntensityAnalyzer

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" 
model = hub.load(module_url)
print ("module %s loaded" % module_url)

def exact_match(student_ans,ref_ans):
    query_vec = model([ref_ans])[0]
    analyzr=SentimentIntensityAnalyzer()
    sim = 1-spatial.distance.cosine(query_vec, model([student_ans])[0])
    sen_score=analyzr.polarity_scores(student_ans)
    #print("Sentence = ", student_ans, "; similarity = ", sim,"; sentiment = ",sen_score['compound'])
    return sim

def stem_match(student_ans,ref_ans):
    student_ans=preprocess.porter_stem_words(student_ans)
    ref_ans=preprocess.porter_stem_words(ref_ans)
    s1=fuzz.ratio(student_ans,ref_ans)
    s2=fuzz.partial_ratio(student_ans,ref_ans)
    s3=fuzz.token_sort_ratio(student_ans,ref_ans)
    s4=fuzz.token_set_ratio(student_ans,ref_ans)
    listt=[s1,s2,s3,s4]
    return max(listt)

def heuristic_match(student_ans,ref_ans):
    # WordNet synonym match
    syn_matches=0
    for word in student_ans:
        seet=[]
        syns=wordnet.synsets(word)
        for syn in syns:
            for i in syn.lemmas():
                seet.append(i.name())
        for ref_word in ref_ans:
            if ref_word in seet: syn_matches+=1
    # Numeric value match
    num_macthes=0

    """   
    words=''
    words=nltk.word_tokenize(student_ans)
    words=preprocess.replace_numbers(words)
    student_ans=TreebankWordDetokenizer().detokenize(words)

    words=nltk.word_tokenize(ref_ans)
    words=preprocess.replace_numbers(words)
    ref_ans=TreebankWordDetokenizer().detokenize(words) """
    for word in student_ans:
        if word in ref_ans: num_macthes+=1
    # Acronym match
    # Derivational form match
    deri_matches=0
    for word in student_ans:
        seet=[]
        syns=wordnet.synsets(word)
        for syn in syns:
            for i in syn.lemmas():
                seet.append(i.name())
        seet=preprocess.lemmatize_words(seet)
        for ref_word in ref_ans:
            word=preprocess.lemmatize_words(ref_word)
            if ref_word in seet: deri_matches+=1
    
    # Country adjectival form / demonym match
    matches=max(syn_matches,deri_matches,num_macthes)
    return matches

# matches to marks
def matches_to_marks(matches):
    score=[]
    maxx=max(matches)
    for match in matches:
        if match <= (maxx/9):score.append(1)
        elif match > (maxx/9) and match <= 2*(maxx/9):score.append(1.5)
        elif match > 2*(maxx/9) and match <= 3*(maxx/9):score.append(2)
        elif match > 3*(maxx/9) and match <= 4*(maxx/9):score.append(2.5)
        elif match > 4*(maxx/9) and match <= 5*(maxx/9):score.append(3)
        elif match > 5*(maxx/9) and match <= 6*(maxx/9):score.append(3.5)
        elif match > 6*(maxx/9) and match <= 7*(maxx/9):score.append(4)
        elif match > 7*(maxx/9) and match <= 8*(maxx/9):score.append(4.5)
        elif match > 8*(maxx/9) :score.append(5)
    return score
# main function
    
def process(student_ans,ref_ans):
    match1=exact_match(student_ans,ref_ans)
    match2=stem_match(student_ans,ref_ans)
    match3=heuristic_match(student_ans,ref_ans)
    return max(match1,match2,match3)