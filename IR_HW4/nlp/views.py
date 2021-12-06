from nltk.util import pr
import nlp
from nlp.models import PubMed, withoutPuncTokens
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
import pickle
import nltk
import string
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
stemmer = PorterStemmer()
import numpy as np
import pandas as pd


allDocs = pd.read_csv('files/all.csv').iloc[: , 1:]



# Create your views here.
def home(request):      
    return render(request, 'nlp/index.html')


def get_tokens(text):
  lower = text.lower()
  remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
  no_punctuation = lower.translate(remove_punctuation_map)
  tokens = nltk.word_tokenize(no_punctuation)
  filtered_tokens = [word for word in tokens if not word in stopwords.words('english')]
   
  return filtered_tokens

def words_cnt(text):
  lower = text.lower()
  remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
  no_punctuation = lower.translate(remove_punctuation_map)
  tokens = nltk.word_tokenize(no_punctuation)
  
  return len(tokens)

def search_tfidf_vec(Type, tf_fm, search_sentence, tfidf_res, idf):
  search_sentence_tokens = get_tokens(search_sentence)
  search_df = pd.DataFrame(0, index=np.arange(1), columns=tfidf_res.columns)
  
  word_cnt = 0
  for token, pos in nltk.pos_tag(search_sentence_tokens):
    stem_word = stemmer.stem(token)
    if(Type == 'tfidf'):
      search_df[stem_word] += 1
      word_cnt+=1
    if(Type == 'tfidf + pos'):
      if(pos.startswith('N') or pos.startswith('V')): 
        search_df[stem_word] += 5
        word_cnt+=5
      elif(pos.startswith('J') or pos.startswith('RB')):
        search_df[stem_word] += 4
        word_cnt+=4
      else:
        search_df[stem_word] += 1
        word_cnt+=1


  if(tf_fm == 1):
    search_df /= word_cnt
  elif(tf_fm == 2):
    search_df = search_df.apply(lambda x: np.log10(1+x))

  search_df = search_df.mul(idf, axis=1)
  search_sentence_vec = search_df.iloc[0]
  return search_sentence_vec

def cos_sim_sort(Type, tf_fm, search_sentence, tfidf_res, idf):
  dot_res = []
  search_sentence_vec = search_tfidf_vec(Type, tf_fm, search_sentence, tfidf_res, idf)

  for idx, doc_vec in tfidf_res.iterrows():
    cos_sim = np.dot(doc_vec, search_sentence_vec)/(np.linalg.norm(doc_vec)*np.linalg.norm(search_sentence_vec))
    dot_res.append((round(cos_sim, 2), idx, allDocs.iloc[int(idx[1:])]['title'], allDocs.iloc[int(idx[1:])]['abstract'],  words_cnt(allDocs.iloc[int(idx[1:])]['abstract'])))

  return sorted(dot_res, key = lambda s: s[0], reverse = True)[:10]



@csrf_exempt
def search_docs(request):
    tf_fm = request.POST['TF']
    idf_fm = request.POST['IDF']
    print(tf_fm)
    print(idf_fm)
    tf_idf = pickle.load(open("files/tf-"+ tf_fm + "_idf-" + idf_fm + ".pickle", "rb"))
    return HttpResponse(json.dumps(cos_sim_sort('tfidf', 1, request.POST['search_str'], tf_idf[0], tf_idf[1])))

@csrf_exempt
def handle_content(request):
    return HttpResponse(allDocs.iloc[int(request.POST['id'][1:])]['abstract'])

# print(cos_sim_sort('tfidf', 1, search_sentence, tf_idf[0], tf_idf[1]))
# print(tf_idf)