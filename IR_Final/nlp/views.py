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
nltk.download('wordnet')
stemmer = PorterStemmer()
import numpy as np
import pandas as pd
import math
import glob
from sklearn.cluster import KMeans
from nltk.stem import WordNetLemmatizer
from collections import Counter
from nltk.corpus import wordnet as wn
# from summarizer import Summarizer, TransformerSummarizer



reparse = pd.read_csv('files/reparse.csv').iloc[:, 1:]
# model = TransformerSummarizer(transformer_type="XLNet",transformer_model_key="xlnet-base-cased")


# Create your views here.
def home(request):      
    return render(request, 'nlp/index.html')


def GetSentenceSimilarity(sentence1, sentence2):
    wordList1 = sentence1.lower().split(' ')
    wordList2 = sentence2.lower().split(' ')
    score = []
    for word in wordList1:
        score.append(GetHighestWordSimilarity(word, wordList2))
    return sum(score)/len(score)    


def RemoveStopWord(sentence):
    newStopWord = stopwords.words('english')
    newStopWord.append('and')
    new_tokens = word_tokenize(sentence)
    new_tokens = [t.lower() for t in new_tokens]
    new_tokens =[t for t in new_tokens if t not in newStopWord]
    new_tokens = [t for t in new_tokens if t.isalpha()]
    lemmatizer = WordNetLemmatizer()
    new_tokens =[lemmatizer.lemmatize(t) for t in new_tokens]
    return ' '.join(new_tokens)

def GetSynSimilarity(wordSynset1, wordSynset2):
    similarity = 0
    subsumer = wordSynset1.lowest_common_hypernyms(wordSynset2, use_min_depth=True)
    if not subsumer:
        return similarity
    h = max(len(hyp_path) for hyp_path in subsumer[0].hypernym_paths()) + 1
    l = wordSynset1.shortest_path_distance(wordSynset2)
    alpha = 0.2
    beta = 0.45
    similarity = math.exp(-alpha*l)*(math.exp(beta*h) - math.exp(-beta*h))/(math.exp(beta*h) + math.exp(-beta*h))
    return similarity
def GetHighestWordSimilarity(word, wordList):
    similarity = 0
    if(not wordList):
        return similarity
    synList = wn.synsets(word)
    if(not synList):
        return similarity
    for syn in synList:
        for iword in wordList:
            iSynList = wn.synsets(iword)
            if(not iSynList):
                continue
            for iSyn in iSynList:
                iSimilarity = GetSynSimilarity(syn, iSyn)
                if(iSimilarity> similarity):
                    similarity = iSimilarity
    return similarity


def SearchInFolder(folderPath, searchText):
    text = RemoveStopWord(searchText)
    searchWords = word_tokenize(text)
    
    with open(folderPath+'description.txt', "r", encoding="utf-8") as f:
        description = f.readline()
        wordList = description.split(',')
        
    simList = []
    
    for sWord in searchWords:
        similarity = GetHighestWordSimilarity(sWord, wordList)
        
        simList.append(similarity)
    avgSearchScore = sum(simList)/len(simList)
    return avgSearchScore
    
def Search(rootPath, searchText, result):
    folderList = glob.glob("{}*/".format(rootPath), recursive = True)
    if not folderList:
        for file in glob.glob('{0}/PMC*.txt'.format(rootPath)):
            filelink = file.replace("\\","/")
            with open(filelink, "r", encoding="utf-8") as f:
                articleID = f.readline().replace('\n', '')
                PMID = int(articleID.split("|")[0])
                articleTags = f.readline()
                articleTags = articleTags.replace('}', '')
                articleTags = articleTags.replace('{', '')
                articleTags = articleTags.replace('\'', '')
                articleTags = articleTags.replace(' ', '')
                articleTags = articleTags.replace('\n', '')
                tagList = articleTags.split(',')
                articleContent = f.readline()
                articleScore = GetSentenceSimilarity(searchText, articleContent)
                result.append(["{:.2f}".format(articleScore),PMID, tagList])
    else:
        subfolderScoreList = []
        for folder in folderList:
            path = folder.replace("\\","/")
            folderScore = SearchInFolder(path, searchText)
            subfolderScoreList.append(folderScore)

        selectFolderIndex = np.argmax(subfolderScoreList)
        selectFolderPath = folderList[selectFolderIndex].replace("\\","/")
        Search(selectFolderPath, searchText, result)

@csrf_exempt
def search_docs(request):
    result = []        
    Search('files/Data/Categories/', request.POST['search_str'], result)
    result.sort(key=lambda x:x[0], reverse=True)

    for item in result:
      item.append(reparse.loc[reparse['PMID'] == item[1]]['title'].values[0])
      item.append(reparse.loc[reparse['PMID'] == item[1]]['abstract'].values[0])

    return HttpResponse(json.dumps(result))

@csrf_exempt
def handle_content(request):
    return HttpResponse(reparse.loc[reparse['PMID'] == int(request.POST['id'])]['abstract'].values[0].replace('\n', '<br />'))
