import nltk,unicodedata,inflect,re#,contractions
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer,PorterStemmer, WordNetLemmatizer
from num2words import num2words
from nltk.tokenize.treebank import TreebankWordDetokenizer

'''def replace_contractions(text):
    #Replace contractions in string of text#
    return contractions.fix(text)
'''
def remove_non_ascii(words):
    #Remove non-ASCII characters from list of tokenized words
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

def cleanhtml(raw_html):
    #cleanr = re.compile('<.*?>')
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    new_words = re.sub(cleanr, '', raw_html)
    return new_words

def to_lowercase(words):
    #Convert all characters to lowercase from list of tokenized words#
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    #Remove punctuation from list of tokenized words#
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def replace_numbers(words):
    #Replace all interger occurrences in list of tokenized words with textual representation#
    new_words = []
    for word in words:
        new_word=word
        digit=''
        try:
            if(word==str(int(word))):
                new_word=num2words(word,lang='en',to='cardinal')
        except:
            for i in word:
                if i.isdigit():
                    digit+=i
                    new_word=num2words(digit,lang='en',to='ordinal')
        new_words.append(new_word)
    return new_words

def remove_stopwords(words):
    #Remove stop words from list of tokenized words#
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def stem_words(words):
    #Stem words in list of tokenized words#
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

def porter_stem_words(words):
    #Stem words in list of tokenized words#
    stemmer = PorterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

def lemmatize_verbs(words):
    #Lemmatize verbs in list of tokenized words#
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

def lemmatize_words(words):
    #Lemmatize verbs in list of tokenized words#
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word)
        lemmas.append(lemma)
    return lemmas

def normalize(text):
   # text=replace_contractions(text)
    text=cleanhtml(text)
    words=nltk.word_tokenize(text)
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    words = TreebankWordDetokenizer().detokenize(words)
    return words

