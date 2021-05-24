from fuzzywuzzy import fuzz
import preprocess
from nltk.corpus import wordnet
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer

def exact_match(student_ans,ref_ans):
    #compares the entire string similarity, in order
    s1=fuzz.ratio(student_ans,ref_ans)
    #compares partial string similarity
    s2=fuzz.partial_ratio(student_ans,ref_ans)
    # ignores word order
    s3=fuzz.token_sort_ratio(student_ans,ref_ans)
    #ignores duplicated words. It is similar with token sort ratio, but a little bit more flexible
    s4=fuzz.token_set_ratio(student_ans,ref_ans)
    listt=[s1,s2,s3,s4]
    return max(listt)

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
    x=1.5
    y=1
    z=1
    return (x*match1+y*match2+z*match3)/3